import requests
import bs4
import random
import string
import discord
from requests_html import HTMLSession
import json
from .import cc_commons
import re
## Generate a hash for user verfication
def getUserNameHash():
	length = 10
	result_str = ''.join(random.choice(string.ascii_uppercase) for i in range(length))
	return result_str


## Fetch user data like stars, raing, name, and profile picture
def fetchUserData(username):
	try:
		page = cc_commons.getWebpage('https://www.codechef.com/users/{}'.format(username))
		soup = bs4.BeautifulSoup(page, 'html.parser')
		rating = int(soup.find('div', class_='rating-number').text)
		stars = "1★"
		try:
			stars = soup.find('span', class_='rating').text
		except:
			print("Unrated User")
		header_containers = soup.find_all('header')
		name = header_containers[1].find('h2').text
		image = "https://s3.amazonaws.com/codechef_shared"+soup.findAll('img',{"width":"70px"})[0].attrs['src']
		return {'status':0,'rating':rating,'stars':stars,'name':name,'profilePicture':image}
	except Exception as e:
		print(e)
		return {'status':1}



## Get a user's rating history
def getRatingHistory(handle):
	temp = "https://www.codechef.com/users/{}".format(handle)
	session = HTMLSession()
	r = session.get(temp)
	r = r.content
	r = str(r)
	idx = r.find("date_versus_rating")
	new_r = r[idx-1:]
	idx = new_r.find("}]")
	new_r = new_r[:-(len(new_r)-idx)-1]
	new_r = "{" + new_r + "\"}]}}"
	new_r.replace("null","\"null\"")
	new_r = new_r.replace("\\",'')
	new_r = new_r.replace("\'",'')
	data = json.loads(new_r)
	return data


## Get a user recent submissions
def getSubmission(username):
	url = "https://www.codechef.com/recent/user?page=0&user_handle={}".format(username)
	data = json.loads(cc_commons.getWebpage(url))
	if data['max_page'] == 0:
		return None
	data = data['content']
	data = bs4.BeautifulSoup(data)
	subs = data.findAll('a')[:-2]
	subs = [x.text for x in subs]
	imgs = data.findAll('img')[:-2]
	pts = data.findAll('span')
	imgs = ["https://s3.amazonaws.com/codechef_shared"+x.attrs['src'] for x in imgs]
	return_data = []
	for i in range(min(len(imgs),5)):
		verd = cc_commons.verdict_img_to_verdict(imgs[i])
		pts2 = re.findall("\[.*\]",pts[i].text)
		if len(pts2)==0:
			pts2 = cc_commons.verdict_img_to_full(verd)
		else:
			pts2="{}".format(pts2[0])
		em = '\N{EN SPACE}'
		desc = f'`{em}{verd}{em}| {em}{pts2}{em}`'
		return_data.append([subs[i],desc])
	return return_data

