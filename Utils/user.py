import requests
import bs4
import random
import string
import discord

def getStars(rating):
	if rating <1400:
		return "1★"
	elif rating <1600:
		return "2★"
	elif rating <1800:
		return "3★"
	elif rating <2000:
		return "4★"
	elif rating <2200:
		return "5★"
	elif rating <2500:
		return "6★"
	else:
		return "7★"
def getUserNameHash():
	length = 10
	result_str = ''.join(random.choice(string.ascii_uppercase) for i in range(length))
	return result_str

def getUserData(username,member):
	try:
		url = 'https://www.codechef.com/users/{}'.format(username)
		page = requests.get(url)
		soup = bs4.BeautifulSoup(page.text, 'html.parser')
		rating = int(soup.find('div', class_='rating-number').text)
		stars = soup.find('span', class_='rating').text
		header_containers = soup.find_all('header')
		name = header_containers[1].find('h2').text
		image = "https://s3.amazonaws.com/codechef_shared"+soup.findAll('img',{"width":"70px"})[0].attrs['src']
		desc = "**Handle for <@{}> succesfully set to {}**".format(member.id,username)
		colour = discord.Colour.light_gray()
		if rating >=2500:
			colour = discord.Colour.red()
		elif rating >=2200:
			colour = discord.Colour.orange()
		elif rating >=2000:
			colour = discord.Colour(0xffff00)
		elif rating >= 1800:
			colour = discord.Colour.purple()
		elif rating >= 1600:
			colour = discord.Colour.blue()
		elif rating >=1200:
			colour = discord.Colour.green()
	    
		embed = discord.Embed(description=desc, color=colour)
		embed.add_field(name='Rating', value=rating, inline=True)
		embed.add_field(name='Stars', value=stars, inline=True)
		embed.set_thumbnail(url=image)
		return { "Status":0, "Name":name, "Rating":rating, "Stars": stars, "embed":embed }
	except:
		return { "Status":1 }


def updateData(username):
	try:
		url = 'https://www.codechef.com/users/{}'.format(username)
		page = requests.get(url)
		soup = bs4.BeautifulSoup(page.text, 'html.parser')
		rating = int(soup.find('div', class_='rating-number').text)
		stars = soup.find('span', class_='rating').text
		colour = discord.Colour.light_gray()
		if rating >=2500:
			colour = discord.Colour.red()
		elif rating >=2200:
			colour = discord.Colour.orange()
		elif rating >=2000:
			colour = discord.Colour(0xffff00)
		elif rating >= 1800:
			colour = discord.Colour.purple()
		elif rating >= 1600:
			colour = discord.Colour.blue()
		elif rating >=1200:
			colour = discord.Colour.green()
	    
		return { "Status":0, "Rating":rating, "Stars": stars}
	except:
		return { "Status":1 }