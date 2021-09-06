import psycopg2
from . import constants
import time
import urllib.parse as urlparse
import os



class DB:
	def __init__(self):
		self.con=""
		if constants.DEBUG != True:
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
		# cur.execute("""
		# 	CREATE TABLE IF NOT EXISTS bot_data(
		# 	id SERIAL PRIMARY KEY,
		# 	access_token VARCHAR (255) NOT NULL,
		# 	expires_after VARCHAR (255) NOT NULL
		# 	);
		# 	""")
		cur.execute("""
			CREATE TABLE IF NOT EXISTS users(
				userid VARCHAR (200) NOT NULL,
				guildid VARCHAR (200) NOT NULL,
				cchandle VARCHAR (100) NOT NULL,
				active int DEFAULT 1
			);
			""")
		cur.execute("""
			CREATE TABLE IF NOT EXISTS cc_user_data(
				handle VARCHAR (200) PRIMARY KEY,
				name VARCHAR (200) ,
				profile_pic VARCHAR (200),
				rating INT DEFAULT 1500 ,
				ratinghistory TEXT NOT NULL,
				solved_problems TEXT NOT NULL,
				submission_stats TEXT NOT NULL,
				lastupdated VARCHAR (255) NOT NULL
			);
			""")
		cur.close()
		self.con.commit()


	def add_cc_user(self,handle,name,profile_pic,rating,ratinghistory,solved_problems,submission_stats):
		cur = self.con.cursor()
		lastupdated = str(int(time.time()))
		cur.execute(f"INSERT INTO cc_user_data(handle,name,profile_pic,rating,ratinghistory,solved_problems,submission_stats,lastupdated) VALUES('{handle}','{name}','{profile_pic}',{rating},'{ratinghistory}','{solved_problems}','{submission_stats}','{lastupdated}')")
		self.con.commit()
		cur.close()

	def fetch_cc_user(self,handle):
		cur = self.con.cursor()
		cur.execute(f"SELECT * FROM cc_user_data WHERE handle='{handle}'")
		data = cur.fetchall()
		if(len(data)==0):
			data=None
		else:
			data=data[0]
			print(data)
			data = {
				"name":data[1],
				"profile_pic" : data[2],
				"rating" : data[3],
				"rating_data": data[4],
				"solved_problems":data[5],
				"submission_stats": data[6],
				"lastupdated": data[7]
        	}
		return data
		cur.close()

	def update_cc_user(self,handle,name,profile_pic,rating,ratinghistory,solved_problems,submission_stats):
		cur = self.con.cursor()
		lastupdated = str(int(time.time()))
		cur.execute(f"UPDATE cc_user_data SET name=%s,profile_pic=%s,rating=%s,ratinghistory=%s,solved_problems=%s,submission_stats=%s,lastupdated=%s WHERE handle=%s",(name,profile_pic,rating,ratinghistory,solved_problems,submission_stats,lastupdated,handle))
		self.con.commit()
		cur.close()


	def add_user_to_guild(self,userid,guildid,cchandle):
		cur = self.con.cursor()
		lastupdated = str(int(time.time()))
		cur.execute(f"INSERT INTO users(userid,guildid,cchandle) VALUES('{userid}','{guildid}','{cchandle}')")
		self.con.commit()
		cur.close()

	def update_user_to_guild(self,userid,guildid,cchandle,active):
		cur = self.con.cursor()
		lastupdated = str(int(time.time()))
		cur.execute(f"UPDATE users SET cchandle=%s,active=%s WHERE userid=%s,guildid=%s",(cchandle,active,userid,guildid))
		self.con.commit()
		cur.close()

	def user_inactive_to_guild(self,userid,guildid):
		cur = self.con.cursor()
		lastupdated = str(int(time.time()))
		cur.execute(f"UPDATE users SET active=%s WHERE userid=%s AND guildid=%s",(0,userid,guildid))
		self.con.commit()
		cur.close()
	
	def get_user_to_guild(self,userid,guildid):
		cur = self.con.cursor()
		cur.execute(f"SELECT * FROM users WHERE userid='{userid}' AND guildid='{guildid}'")
		data = cur.fetchall()
		if(len(data)==0):
			data=None
		else:
			data=data[0]
			data = {
				'user_id':data[0],
				'guild_id':data[1],
				'cchandle': data[2],
				'active':data[3],
			}
		return data

	def remove_user_to_guild(self,userid,guildid):
		cur = self.con.cursor()
		cur.execute(f"DELETE FROM users WHERE userid='{userid}' AND guildid='{guildid}'")
		self.con.commit()
		cur.close()

	def fetch_guild_users(self,guildid):
		cur = self.con.cursor()
		cur.execute(f"SELECT * FROM users WHERE guildid='{guildid}' AND active=1")
		data = cur.fetchall()
		if(len(data)==0):
			data=None
		else:
			res = []
			for x in data:
				cur = {
					'user_id':x[1],
					'guild_id':x[2],
					'cchandle': x[3],
				}
				res.append(cur)
		return res

	def fetch_distinct_active_handles(self):
		cur = self.con.cursor()
		cur.execute(f"SELECT DISTINCT cchandle FROM users WHERE active=1")
		data = cur.fetchall()
		if(len(data)==0):
			data=None
		else:
			res = [x[0] for x in data]
		return res
	

	def fetch_active_handles(self):
		cur = self.con.cursor()
		cur.execute(f"SELECT userid,guildid,cchandle FROM users WHERE active=1")
		data = cur.fetchall()
		if(len(data)==0):
			data=None
		else:
			res = [{'user_id':x[0],'guild_id':x[1],'username':x[2]} for x in data]
		return res


	def get_user_by_discord_id(self,user_id,guild_id):
		cur = self.con.cursor()
		cur.execute(f"SELECT cchandle FROM users WHERE active=1 AND userid='{user_id}' AND guildid='{guild_id}'")
		data = cur.fetchall()
		if(len(data)==0):
			data=None
		else:
			res = data[0][0]
		return res
