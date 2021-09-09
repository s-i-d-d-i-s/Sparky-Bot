import requests
import ujson
import json
import time

from . import constants,database


class CodechefAPI:
	def __init__(self,db):
		self.db = db
		self.data = self.db.fetch_api_data()
		self.token = self.data['access_token']
		self.expires_after = self.data['expires_after']
		
	def validate_token(self):
		if time.time()>self.expires_after:
			data = self.getAccessToken()
			self.token = data['access_token']
			self.expires_after = data['expires_after']
			self.db.update_api_data(self.token,self.expires_after)

	def getAccessToken(self):
		headers = {
			'content-Type': 'application/json',
		}
		
		data = "{" + '"grant_type":"client_credentials" , "scope":"public", "client_id":"{}","client_secret":"{}","redirect_uri":"{}"'.format(constants.CLIENT_ID,constants.CLIENT_SECRET,'') + "}"
		response = ujson.loads(requests.post('https://api.codechef.com/oauth/token', headers=headers, data=data).content)
		if response['status'] != 'OK':
			return {'status':0}
		return {'status':1,'access_token' : response['result']['data']['access_token'],'expires_after':(int(time.time())+3500)}
	

	def getRanklistContest(self,contest_code):	
		self.validate_token()
		def getRanklistPage(contest_code,page_no):
			headers = {
				'Accept': 'application/json',
				'Authorization': 'Bearer '+str(self.token),
			}

			offset = (page_no-1)*1500
			params = (
				('fields', 'rank, username, totalTime, penalty, rating, totalScore'),
				('offset', str(offset)),
			)
			response = requests.get(f'https://api.codechef.com/rankings/{contest_code}', headers=headers, params=params).content
			data = json.loads(response)
			# print(response['result']['data']['code'])
			return data
		print("TOKEN",self.token)
		print("Expiry",self.expires_after)
		res=[]
		for i in range(10):
			print("Page",i+1)
			data = getRanklistPage(contest_code,i+1)
			if data['status']!='error' and data['result']['data']['code'] == 9001:
				if len(data['result']['data']['content']) == 0:
					print(data)
				res.extend(data['result']['data']['content'])
			else:
				break
		return res
	
	# def getUserData(self,handle):
	# 	self.validate_token()
	# 	data = self.db.fetch_cc_user_data(handle)
	# 	if data!=None:
	# 		print(f"Using Cache for {handle} in getUserData ")
	# 		return ujson.loads(data[0])
	# 	headers = {
	# 		'Accept': 'application/json',
	# 		'Authorization': 'Bearer '+str(self.token),
	# 	}
	# 	params = (
	# 		('fields', 'username, fullname, country, state, city, rankings, ratings, occupation, language, organization, problemStats, submissionStats'),
	# 	)
	# 	response = ujson.loads(requests.get(f'https://api.codechef.com/users/{handle}', headers=headers, params=params).content)
	# 	image = "https://#"
	# 	try:
	# 		page = cc_commons.getWebpage('https://www.codechef.com/users/{}'.format(handle))
	# 		soup = bs4.BeautifulSoup(page, 'html.parser')
	# 		image = "https://s3.amazonaws.com/codechef_shared"+soup.findAll('img',{"width":"70px"})[0].attrs['src']
	# 	except:
	# 		print("Unable to parse profile image")
		
	# 	if response['status'] != 'OK':
	# 		raise TokenError
	# 	if response['result']['data']['code'] == 9003:            
	# 		raise HandleNotFoundError
	# 	response['result']['profile_image'] = image
	# 	self.db.update_cc_user_data_userdata(handle,ujson.dumps(response['result']))
	# 	return response['result']

	# def getSubmissions(self,username):
	# 	self.validate_token()
	# 	headers = {
	# 		'Accept': 'application/json',
	# 		'Authorization': 'Bearer '+str(self.token),
	# 	}
	# 	params = (
	# 		('result', 'AC'),
	# 		('username', username),
	# 		('limit', '20'),
	# 		('fields', 'id, date, username, problemCode, language, contestCode, result, time, memory'),
	# 	)
	# 	response = requests.get('https://api.codechef.com/submissions/', headers=headers, params=params)
	# 	response = ujson.loads(response.content)
	# 	return response


	# def getCollegeRanklist(self,collegeName):
	# 	self.validate_token()
	# 	headers = {
	# 		'Accept': 'application/json',
	# 		'Authorization': 'Bearer '+str(self.token),
	# 	}

	# 	params = (
	# 		('fields', 'username, globalRank, countryCode, countryRank, country, institution, institutionType, rating, diff'),
	# 		('institution', collegeName.strip()),
	# 		('limit',25),
	# 	)

	# 	response = requests.get('https://api.codechef.com/ratings/all', headers=headers, params=params)

	# 	data = ujson.loads(response.content)

	# 	if 'content' not in data['result']['data']:
	# 		return []
	# 	data = data['result']['data']['content']

	# 	idx = 1
	# 	res = []
	# 	for d in data:
	# 		fullname = d['fullname']
	# 		username = d['username']
	# 		countryRank = d['countryRank']
	# 		college_rank = idx
	# 		rating = d['rating']
	# 		res.append({'name':fullname,'handle':username,'IN_rank':countryRank,'college_rank':idx,'rating':rating})
	# 		idx+=1
	# 	return res
	
	# def getCollegeRanklistContest(self,collegeName,contest_code):
	# 	self.validate_token()
	# 	headers = {
	# 		'Accept': 'application/json',
	# 		'Authorization': 'Bearer '+str(self.token),
	# 	}

	# 	params = (
	# 		('fields', 'rank, username, totalTime, penalty, country, countryCode, institution, rating, institutionType, contestId, contestCode, totalScore, problemScore'),
	# 		('institution', collegeName),
	# 	)

	# 	response = requests.get('https://api.codechef.com/rankings/'+contest_code, headers=headers, params=params)
	# 	data = json.loads(response.content)
	# 	if data['status']!='OK':
	# 		return None
	# 	if 'content' not in data['result']['data']:
	# 		return None
	# 	data=data['result']['data']['content']
	# 	res = []
	# 	for d in data:
	# 		res.append({'rank':d['rank'],'username':d['username'],'cur_rating':d['rating'],'score':d['totalScore']})
	# 	return res