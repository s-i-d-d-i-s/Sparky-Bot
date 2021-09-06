import requests
import bs4
import time
import json
from . import constants

def getUserData(username):
	def getRatingData(page_source):
		try:
			r = str(page_source)
			idx = r.find("date_versus_rating")
			r = r[idx-1:]
			idx = r.find("}]")
			r = r[:-(len(r)-idx)-1]
			r = "{" + r + "\"}]}}"
			r.replace("null","\"null\"")
			r = r.replace("\\",'')
			r = r.replace("\'",'')
			rating_data = json.loads(r)
			return json.dumps(rating_data)
		except Exception as e:
			print("Exception in getRatingData: ",e)
			return '{"date_versus_rating": { "all": [] }}'
	def getSolvedCodes(handle,data):
		try:
			url = f"https://www.codechef.com/users/{handle}"
			data = data.findAll('section',{'class':'rating-data-section problems-solved'})[0]
			data = data.findAll('article')
			solved = {}
			for d in data[0].findAll('a'):
				solved[(d.text)]=True
			for d in data[1].findAll('a'):
				solved[(d.text)]=True
			return json.dumps(list(solved.keys()))
		except Exception as e:
			print("Exception in getSolvedCodes: ",e)
			return '[]'
	
	def getSubmissionStats(data):
		try:
			data=str(data)
			idx = data.find("colorByPoint")
			data = data[idx-1:]
			idx = data.find("}]")
			data = data[:-(len(data)-idx)-1]
			data = data.replace("\\n",'')
			data = data.replace("\\",'')
			data = data.replace("  ",'')
			data =  data[data.find("data")+5:].strip()
			data = data[1:-2].split('},{')
			retdata={}
			for d in data:
				retdata[d.split(',')[0].split(':')[1][1:-1]] = d.split(',')[1].split(':')[1]
			return json.dumps(retdata)
		except Exception as e:
			print("Exception in getSubmissionStats: ",e)
			return '{"solutions_partially_accepted": "0", "compile_error": "0", "runtime_error": "0", "time_limit_exceeded": "0", "wrong_answers": "0", "solutions_accepted": "0"}'
	try:
		profile_url = f"https://www.codechef.com/users/{username}"
		page_src= requests.get(profile_url).content
		data = bs4.BeautifulSoup(page_src)
		name = data.findAll('div',{'class':'user-details-container'})[0].findAll('h1')[0].text
		profile_picture = data.findAll('div',{'class':'user-details-container'})[0].findAll('header')[0].findAll('img')[0].attrs['src']
		rating = data.findAll('div',{'class':'rating-number'})[0].text
		rating_data = getRatingData(page_src)
		solved_problems = getSolvedCodes(username,data)
		submission_stats = getSubmissionStats(page_src)
		return {
			'status':True,
			"name":name,
			"profile_pic" : profile_picture,
			"rating" : rating,
			"rating_data": rating_data,
			"solved_problems": solved_problems,
			"submission_stats": submission_stats
		}
	except Exception as e:
		print("Exception in getUserData: ",e)
		return {
			'status':False
		}


def isUserRated(username):
	url = "https://www.codechef.com/recent/user?page=0&user_handle={}".format(username)
	data = json.loads(requests.get(url).content)
	if data['max_page'] != 0:
		return True
	return False



def getSolvedCodes(handle,apiObj):
	data = apiObj.getUserData(handle)
	problem_stats = data['data']['content']['problemStats']['solved']
	solved = {}
	for p in problem_stats:
		for code in problem_stats[p]:
			solved[code]=True
	return solved

def add_cc_user_easy(username,data,db):
	db.add_cc_user(username, data['name'], data['profile_pic'], data['rating'], data['rating_data'],data['solved_problems'],data['submission_stats'])

def update_cc_user_easy(username,data,db):
	db.update_cc_user(username, data['name'], data['profile_pic'], data['rating'], data['rating_data'],data['solved_problems'],data['submission_stats'])

def valid_username(username):
	return True


def getUserData_easy(username,db):
	data = db.fetch_cc_user(username)
	cur_time = int(time.time())
	if data==None or int(data['lastupdated']) +constants.USERDATA_UPDATE_COOLDOWN < cur_time:
		new_user = data==None
		data = getUserData(username)
		if new_user == False:
			update_cc_user_easy(username, data, db)
		else:
			add_cc_user_easy(username, data, db)
	return data