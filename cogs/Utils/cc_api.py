from discord.ext import commands
import requests
import json
import time
import bs4
from . import constants,database,cc_commons
import ujson

CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"
REDIRECT_URI = "https://www.codechef.com"

class CCApiError(commands.CommandError):
    def __init__(self, message=None):
        super().__init__(message or 'Codechef API error')

class TokenError(CCApiError):
    """An error caused by not able to get valid access token"""
    def __init__(self):
        super().__init__('Error getting a valid token from CC')

class HandleNotFoundError(CCApiError):
    """An error caused by invalid handle"""
    def __init__(self):
        super().__init__('User does not exist')


class CodechefAPI:
	def __init__(self):
		self.db = database.DB()
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
		
		data = "{" + '"grant_type":"client_credentials" , "scope":"public", "client_id":"{}","client_secret":"{}","redirect_uri":"{}"'.format(CLIENT_ID,CLIENT_SECRET,REDIRECT_URI) + "}"
		response = ujson.loads(requests.post('https://api.codechef.com/oauth/token', headers=headers, data=data).content)
		if response['status'] != 'OK':
			raise TokenError
		return {'access_token' : response['result']['data']['access_token'],'expires_after':(int(time.time())+3500)}
	
	def getUserData(self,handle):
		self.validate_token()
		data = self.db.fetch_cc_user_data(handle)
		if data!=None:
			print(f"Using Cache for {handle} in getUserData ")
			return ujson.loads(data[0])
		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer '+str(self.token),
		}
		params = (
			('fields', 'username, fullname, country, state, city, rankings, ratings, occupation, language, organization, problemStats, submissionStats'),
		)
		response = ujson.loads(requests.get(f'https://api.codechef.com/users/{handle}', headers=headers, params=params).content)
		image = "https://#"
		try:
			page = cc_commons.getWebpage('https://www.codechef.com/users/{}'.format(handle))
			soup = bs4.BeautifulSoup(page, 'html.parser')
			image = "https://s3.amazonaws.com/codechef_shared"+soup.findAll('img',{"width":"70px"})[0].attrs['src']
		except:
			print("Unable to parse profile image")
		
		if response['status'] != 'OK':
			raise TokenError
		if response['result']['data']['code'] == 9003:            
			raise HandleNotFoundError
		response['result']['profile_image'] = image
		self.db.update_cc_user_data_userdata(handle,ujson.dumps(response['result']))
		return response['result']

	def getSubmissions(self,username):
		self.validate_token()
		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer '+str(self.token),
		}
		params = (
			('result', 'AC'),
			('username', username),
			('limit', '20'),
			('fields', 'id, date, username, problemCode, language, contestCode, result, time, memory'),
		)
		response = requests.get('https://api.codechef.com/submissions/', headers=headers, params=params)
		response = ujson.loads(response.content)
		return response


	def getCollegeRanklist(self,collegeName):
		self.validate_token()
		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer '+str(self.token),
		}

		params = (
			('fields', 'username, globalRank, countryCode, countryRank, country, institution, institutionType, rating, diff'),
			('institution', collegeName.strip()),
			('limit',25),
		)

		response = requests.get('https://api.codechef.com/ratings/all', headers=headers, params=params)

		data = ujson.loads(response.content)

		if 'content' not in data['result']['data']:
			return []
		data = data['result']['data']['content']

		idx = 1
		res = []
		for d in data:
			fullname = d['fullname']
			username = d['username']
			countryRank = d['countryRank']
			college_rank = idx
			rating = d['rating']
			res.append({'name':fullname,'handle':username,'IN_rank':countryRank,'college_rank':idx,'rating':rating})
			idx+=1
		return res
	
	def getCollegeRanklistContest(self,collegeName,contest_code):
		self.validate_token()
		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer '+str(self.token),
		}

		params = (
			('fields', 'rank, username, totalTime, penalty, country, countryCode, institution, rating, institutionType, contestId, contestCode, totalScore, problemScore'),
			('institution', collegeName),
		)

		response = requests.get('https://api.codechef.com/rankings/'+contest_code, headers=headers, params=params)
		data = json.loads(response.content)
		if data['status']!='OK':
			return None
		if 'content' not in data['result']['data']:
			return None
		data=data['result']['data']['content']
		res = []
		for d in data:
			res.append({'rank':d['rank'],'username':d['username'],'cur_rating':d['rating'],'score':d['totalScore']})
		return res
    