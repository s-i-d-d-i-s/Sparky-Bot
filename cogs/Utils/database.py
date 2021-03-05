import psycopg2
from . import constants
import time
import urllib.parse as urlparse
import os



class DB:
	def __init__(self):
		self.con=""
		if constants.DEBUG != '1':
			url = urlparse.urlparse(os.environ['DATABASE_URL'])
			dbname = url.path[1:]
			user = url.username
			password = url.password
			host = url.hostname
			port = url.port
			self.con = con = psycopg2.connect(
				dbname=dbname,
				user=user,
				password=password,
				host=host,
				port=port
			)
		else:
			host = "localhost"
			dbname = "testing"
			user = "postgres"
			password = "admin"
			self.con = con = psycopg2.connect(
				host = host,
				dbname=dbname,
				user=user,
				password=password
			)

		self.create_tables()

	def __del__(self): 
		self.con.close()
		
	def create_tables(self):
		cur = self.con.cursor()
		cur.execute("""
			CREATE TABLE IF NOT EXISTS bot_data(
			id SERIAL PRIMARY KEY,
			access_token VARCHAR (255) NOT NULL,
			expires_after VARCHAR (255) NOT NULL
			);
			""")
		
		cur.execute("""
			CREATE TABLE IF NOT EXISTS users(
				id SERIAL PRIMARY KEY,
				userid VARCHAR (200) NOT NULL,
				guildid VARCHAR (200) NOT NULL,
				cchandle VARCHAR (100) NOT NULL,
				ccrating INTEGER 
			);
			""")
		cur.execute("""
			CREATE TABLE IF NOT EXISTS cc_user_data(
				id SERIAL PRIMARY KEY,
				handle VARCHAR (200) NOT NULL,
				userdata TEXT NOT NULL,
				subs TEXT NOT NULL,
				ratinghistory TEXT NOT NULL,
				lastupdated_userdata VARCHAR (255) NOT NULL,
				lastupdated_subs VARCHAR (255) NOT NULL,
				lastupdated_rating VARCHAR (255) NOT NULL
			);
			""")
		cur.execute("""
			CREATE TABLE IF NOT EXISTS college_ranklist(
				id SERIAL PRIMARY KEY,
				guild_id VARCHAR (200) NOT NULL,
				chan_id VARCHAR (200) NOT NULL,
				msg_id VARCHAR (200) NOT NULL,
				college_name VARCHAR (200) NOT NULL,
				ranklist TEXT NOT NULL,
				lastupdated VARCHAR (255) NOT NULL
			);
			""")
		cur.execute("""
			CREATE TABLE IF NOT EXISTS contest_cache(
				id SERIAL PRIMARY KEY,
				contest_code VARCHAR (200) NOT NULL,
				ranklist TEXT NOT NULL,
				lastupdated VARCHAR (255) NOT NULL
			);
			""")
		cur.close()
		self.con.commit()

	def update_api_data(self,access_token,expire_after):
		cur = self.con.cursor()
		cur.execute("SELECT * FROM bot_data")
		if(len(cur.fetchall())==0):
			cur.execute(f"INSERT INTO bot_data(access_token,expires_after) VALUES({access_token},{expire_after})")
		else:
			cur.execute(f"UPDATE bot_data SET access_token= '{access_token}',expires_after = '{expire_after}'")
		self.con.commit()
		cur.close()
		
	def fetch_api_data(self):
		cur = self.con.cursor()
		cur.execute("SELECT * FROM bot_data")
		data = cur.fetchall()
		if len(data)==0:
			cur = self.con.cursor()
			cur.execute(f"INSERT INTO bot_data(access_token,expires_after) VALUES('s59_60r',0)")
			self.con.commit()
			return {'access_token':"s59_60r",'expires_after':int(0)}
		data = data[0]
		cur.close()
		return {'access_token':data[1],'expires_after':int(data[2])}

	def add_user_data(self,userid,guildid,cchandle,ccrating):
		cur = self.con.cursor()
		cur.execute(f"INSERT INTO users(userid,guildid,cchandle,ccrating) VALUES('{userid}','{guildid}','{cchandle}',{ccrating})")
		self.con.commit()
		cur.close()
		
	def fetch_user_data(self,userid,guildid):
		cur = self.con.cursor()
		cur.execute(f"SELECT * FROM users where userid= '{userid}' AND guildid ='{guildid}'")
		data = cur.fetchall()
		self.con.commit()
		cur.close()
		return data

	def update_user_data(self,userid,guildid,cchandle,ccrating):
		cur = self.con.cursor()
		cur.execute(f"UPDATE users SET cchandle = '{cchandle}',ccrating = '{ccrating}' WHERE userid= '{userid}' AND guildid ='{guildid}'")
		self.con.commit()
		cur.close()

	def fetch_guild_users(self,guildid):
		cur = self.con.cursor()
		cur.execute(f"SELECT * FROM users where guildid ='{guildid}'")
		data = cur.fetchall()
		self.con.commit()
		cur.close()
		return data

	def update_cc_user_data_rating_hist(self,handle,ratinghist):
		cur = self.con.cursor()
		cur.execute(f"SELECT * FROM cc_user_data WHERE handle='{handle}'")
		if(len(cur.fetchall())==0):
			# New Handle
			cur.execute(f"INSERT INTO cc_user_data(handle,userdata,ratinghistory,lastupdated_userdata,lastupdated_rating,subs,lastupdated_subs) VALUES(%s,%s,%s,%s,%s,%s,%s)",(handle,"{}",ratinghist,str(0),str(int(time.time())),"{}",str(0)))
			self.con.commit()
			cur.close()
		else:
			cur.execute(f"UPDATE cc_user_data SET ratinghistory=%s,lastupdated_rating=%s WHERE handle = %s",(ratinghist,str(int(time.time())),handle))
			self.con.commit()
			cur.close()
		
	def update_cc_user_data_userdata(self,handle,userdata):
		cur = self.con.cursor()
		cur.execute(f"SELECT * FROM cc_user_data WHERE handle='{handle}'")
		if(len(cur.fetchall())==0):
			# New Handle
			cur.execute(f"INSERT INTO cc_user_data(handle,userdata,ratinghistory,lastupdated_userdata,lastupdated_rating,subs,lastupdated_subs) VALUES(%s,%s,%s,%s,%s,%s,%s)",(handle,userdata,"{}",str(int(time.time())),str(0),"{}",str(0)))
			self.con.commit()
			cur.close()
		else:
			cur.execute(f"UPDATE cc_user_data SET userdata=%s,lastupdated_userdata=%s WHERE handle=%s",(userdata,str(int(time.time())),handle))
			self.con.commit()
			cur.close()
			
	def update_cc_user_data_subs(self,handle,subs):
		cur = self.con.cursor()
		cur.execute(f"SELECT * FROM cc_user_data WHERE handle='{handle}'")
		if(len(cur.fetchall())==0):
			# New Handle
			cur.execute(f"INSERT INTO cc_user_data(handle,userdata,ratinghistory,lastupdated_userdata,lastupdated_rating,subs,lastupdated_subs) VALUES(%s,%s,%s,%s,%s,%s,%s)",(handle,"{}","{}",str(0),str(0),subs,str(int(time.time()))))
			self.con.commit()
			cur.close()
		else:
			cur.execute(f"UPDATE cc_user_data SET subs=%s,lastupdated_subs=%s WHERE handle=%s",(subs,str(int(time.time())),handle))
			self.con.commit()
			cur.close()
			
	def fetch_cc_user_data(self,handle):
		cur = self.con.cursor()
		cur.execute(f"SELECT userdata,lastupdated_userdata FROM cc_user_data WHERE handle='{handle}'")
		data = cur.fetchall()

		if(len(data)==0):
			data=None
		else:
			data=data[0]
			if(int(time.time())>constants.USERDATALIM+int(data[1])):
				data=None
		cur.close()
		return data

	def fetch_user_subs(self,handle):
		cur = self.con.cursor()
		cur.execute(f"SELECT subs,lastupdated_subs FROM cc_user_data WHERE handle='{handle}'")
		data = cur.fetchall()
		if(len(data)==0):
			data=None
		else:
			data=data[0]
			if(int(time.time())>constants.SUBLIM+int(data[1])):
				data=None
		cur.close()
		return data

	def fetch_user_rating_hist(self,handle):
		cur = self.con.cursor()
		cur.execute(f"SELECT ratinghistory,lastupdated_rating FROM cc_user_data WHERE handle='{handle}'")
		data = cur.fetchall()
		if(len(data)==0):
			data=None
		else:
			data=data[0]
			if(int(time.time())>constants.RATINGLIM+int(data[1])):
				data=None
		cur.close()
		return data

	def add_college_data(self,guild_id,msg_id,chan_id,college_name,ranklist):
		cur = self.con.cursor()
		cur.execute(f"INSERT INTO college_ranklist(guild_id,chan_id,msg_id,college_name,ranklist,lastupdated) VALUES('{guild_id}','{chan_id}','{msg_id}','{college_name}','{ranklist}','{int(time.time())}')")
		self.con.commit()
		cur.close()


	def fetch_college_data(self,guild_id):
		cur = self.con.cursor()
		cur.execute(f"SELECT * FROM college_ranklist where guild_id ='{guild_id}'")
		data = cur.fetchall()
		self.con.commit()
		cur.close()
		return data

	def update_college_data(self,guildid,chan_id,msg_id,college_name,ranklist):
		cur = self.con.cursor()
		cur.execute(f"UPDATE college_ranklist SET college_name = '{college_name}',ranklist = '{ranklist}',chan_id='{chan_id}',msg_id='{msg_id}',lastupdated='{int(time.time())}' WHERE guild_id= '{guildid}'")
		self.con.commit()
		cur.close()

	def add_contest_data(self,contest_code,ranklist):
		cur = self.con.cursor()
		cur.execute(f"INSERT INTO contest_cache(contest_code,ranklist,lastupdated) VALUES('{contest_code}','{ranklist}','{int(time.time())}')")
		self.con.commit()
		cur.close()

	def fetch_contest_data(self,contest_code):
		cur = self.con.cursor()
		cur.execute(f"SELECT * FROM contest_cache where contest_code ='{contest_code}'")
		data = cur.fetchall()
		self.con.commit()
		cur.close()
		return data