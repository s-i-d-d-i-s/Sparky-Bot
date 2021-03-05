import requests
import bs4
import random
import string
import discord
import json
import ujson
from .import cc_commons,database
import re
from datetime import datetime
## Generate a hash for user verfication
def getUserNameHash():
	length = 10
	result_str = ''.join(random.choice(string.ascii_uppercase) for i in range(length))
	return result_str

def rating_to_stars(rating):
	rating = int(rating)
	if rating < 1400:
		return "1★"
	elif rating < 1600:
		return "2★"
	elif rating < 1800:
		return "3★"
	elif rating < 2000:
		return "4★"
	elif rating < 2200:
		return "5★"
	elif rating < 2500:
		return "6★"
	else:
		return "7★"

## Fetch user data like stars, raing, name, and profile picture from API
def fetchUserData(username,apiObj=None):
    try:
        try:
            data = apiObj.getUserData(username)
        except Exception as e:
            print("Data Not Feteched",e)
            return {'status':1}

        rating = data['data']['content']['ratings']['allContest']
        stars = rating_to_stars(rating)
        name = data['data']['content']['fullname']
        image = data['profile_image']
        long_rating = data['data']['content']['ratings']['long']
        short_rating = data['data']['content']['ratings']['short']
        ltime_rating = data['data']['content']['ratings']['lTime']
        
        return {
            'status':0,
            'rating':rating,'stars':stars,
            'name':name,'profilePicture':image,
            'long_rating':long_rating,'short_rating':short_rating,
            'ltime_rating':ltime_rating
            }
    except Exception as e:    
        print(e," at fetchUserData")
        return {'status':1}
            
	
## Get a user's rating history
def getRatingHistory(handle,apiObj):
    
    rating_data = apiObj.db.fetch_user_rating_hist(handle)
    if rating_data != None:
        print(f"Using Cache for {handle} in getRatingHistory ")
        return ujson.loads(rating_data[0])
    temp = "https://www.codechef.com/users/{}".format(handle)
    r = cc_commons.getWebpage(temp)
    img=""
    r = str(r)
    stats = ""
    idx = r.find("date_versus_rating")
    new_r = r[idx-1:]
    idx = new_r.find("}]")
    new_r = new_r[:-(len(new_r)-idx)-1]
    new_r = "{" + new_r + "\"}]}}"
    new_r.replace("null","\"null\"")
    new_r = new_r.replace("\\",'')
    new_r = new_r.replace("\'",'')
    data = json.loads(new_r)
    apiObj.db.update_cc_user_data_rating_hist(handle,ujson.dumps(data))
    return data



## Get a user submission statistics
def getSubmissionStats(r):
    idx = r.find("colorByPoint")
    new_r = r[idx-1:]
    idx = new_r.find("}]")
    new_r = new_r[:-(len(new_r)-idx)-1]
    new_r = new_r.replace("\\n",'')
    new_r = new_r.replace("\\",'')
    new_r = new_r.replace("  ",'')
    data =  new_r[new_r.find("data")+5:].strip()
    data = data[1:-2].split('},{')
    retdata={}
    for d in data:
        retdata[d.split(',')[0].split(':')[1][1:-1]] = d.split(',')[1].split(':')[1]
    return retdata


## Get a user recent submissions
def getSubmission(username,apiObj):
    data = apiObj.getSubmissions(username)
    data = data['result']['data']['content']
    subs = []
    for d in data:
        cur = {'result':d['result'],'solution':'https://www.codechef.com/viewsolution/{}'.format(d['id']),'date':datetime.strptime(d['date'],"%Y-%m-%d %H:%M:%S").strftime('%I:%M:%p %d/%m/%Y'),'code':d['problemCode']}
        cur['problemUrl'] = "https://www.codechef.com/{}/problems/{}".format(d['contestCode'],d['problemCode'])
        subs.append(cur)
    return_data = []
    for i in range(min(len(subs),5)):
        em = '\N{EN SPACE}'
        sq = '\N{WHITE SQUARE WITH UPPER RIGHT QUADRANT}'
        verd = subs[i]['result']
        sol_link = subs[i]['solution']
        cur_date = subs[i]['date']
        prob_url = subs[i]['problemUrl']
        desc = f'`{em}{verd}{em}| {em}`[`view solution {sq}`]({sol_link} "View Solution")`{em} | {em}{cur_date}{em} | {em}`[`link {sq}`]({prob_url} "Link to contest page")'
        return_data.append([subs[i]['code'],desc])
    return return_data


def scan_util(username,apiObj):
    
    def isLong(name):
        ls=[
            'January Challenge',
            'February Challenge',
            'March Challenge',
            'April Challenge',
            'May Challenge',
            'June Challenge',
            'July Challenge',
            'August Challenge',
            'September Challenge',
            'October Challenge',
            'November Challenge',
            'December Challenge',
        ]
        for x in ls:
            if name.find(x)!=-1:
                return True
        return False

    data = getRatingHistory(username,True,driver)
    rating_data = data[0]
    contest_part_in = len(rating_data['date_versus_rating']['all'])
    current_rating = rating_data['date_versus_rating']['all'][::-1][0]['rating']
    last_contest = rating_data['date_versus_rating']['all'][::-1][0]['name']
    best_rank = min([[int(x['rank']),x['name']] for x in rating_data['date_versus_rating']['all']],key = lambda t: t[0])
    best_rating = max([int(x['rating']) for x in rating_data['date_versus_rating']['all']])
    best_star = rating_to_stars(best_rating)
    long_contest = sum([isLong(x['name']) for x in rating_data['date_versus_rating']['all']])
    short_contest = contest_part_in - long_contest
    real_ratio = "INF"
    if long_contest != 0:
    	real_ratio = short_contest/long_contest
    submission_stats = data[1]
    return {
        'contest_part_in':contest_part_in,
        'current_rating':current_rating,
        'best_star':best_star,
        'best_rating':best_rating,
        'stars':rating_to_stars(current_rating),
        'last_contest':last_contest,
        'best_rank':best_rank,
        'long_contest':long_contest,
        'short_contest': short_contest,
        'real_ratio': real_ratio,
        'submission_stats':submission_stats,
        'user_pic':data[2]
    }


def get_feedback_for_fav(long_no,short_no,username):
    feedback_fav=""
    if long_no > short_no:
        feedback_fav = f"It can be said that {username} likes long challenges more"
    elif long_no < short_no:
        feedback_fav = f"It is obvious that {username} likes to grind on short challenges more"
    else:
        feedback_fav = f"{username} loves both short and long challenges equally"
    return feedback_fav

def get_feedback_for_real_ratio(real_ratio,username):
    if real_ratio=="INF":
        return ""
    feedback_rr=""
    if real_ratio == 1:
        feedback_rr =  f"Nice ! looks like {username} loves to have things in balance.."
    elif real_ratio > 100:
        feedback_rr =  f"{username} who is this?? {username} would choose short contest over long any given day"
    elif  real_ratio > 50:
        feedback_rr =  f"{username} orz... Do i need to say anything..?"
    elif  real_ratio > 20:
        feedback_rr =  f"{username} is without a doubt a seasoned player in short contests."
    elif  real_ratio > 15:
        feedback_rr =  f"{username} is a badass when it comes to taking risk in short contests."
    elif  real_ratio > 10:
        feedback_rr =  f"Its obvious that {username} loves long contest"
    elif  real_ratio > 5:
        feedback_rr =  f"Orz..There is a little more inclination towards short contest"
    elif  real_ratio > 1:
        feedback_rr =  f"{username} is not scared of short contests"
    elif real_ratio < 0.1:
        feedback_rr =  f"Very few short contests... Seems like a special case"
    elif real_ratio < 0.25:
        feedback_rr =  f"{username} is more focused on long challenges"
    elif real_ratio < 0.5:
        feedback_rr =  f"On any given day {username} would chose long over short"
    elif real_ratio < 0.5:
        feedback_rr =  f"{username} loves long contest more than short"
    elif real_ratio < 0.75:
        feedback_rr =  f"Its obvious that {username} loves long contest"
    elif real_ratio < 0.8:
        feedback_rr =  f"There is a little more inclination towards long contest"
    return feedback_rr

def getAnalysis(username,data,feedback_rr,feedback_fav):
    analysis= f"""
```yaml
{username} is currently rated {data['current_rating']} orz.
Owns a shiny {data['stars']}.

Once upon a time, {username} reached a rating of {data['best_rating']}
He was flexing {data['best_star']} back then..

{username} participated in {data['contest_part_in']} contest.

The last contest {username} took part in was {data['last_contest']}.

Okay, now moment of showoff.
{username} best performance till date is Rank {data['best_rank'][0]} in {data['best_rank'][1]}.

{username} took part in {data['long_contest']} long contest and {data['short_contest']} short contest.
{feedback_fav}

Sparky has a reality ratio, which is ratio of short to long contest.
{username} has a reality ratio of  [ {data['real_ratio']} ]

{feedback_rr}

Nerd Stats:

1> AC  : {data['submission_stats']['solutions_accepted']}
2> WA  : {data['submission_stats']['wrong_answers']}
3> CE  : {data['submission_stats']['compile_error']}
4> RE  : {data['submission_stats']['runtime_error']}
5> TLE : {data['submission_stats']['time_limit_exceeded']}

```
    """
    return analysis


def getSolvedCodes(handle,apiObj):
    data = apiObj.getUserData(handle)
    problem_stats = data['data']['content']['problemStats']['solved']
    solved = {}
    for p in problem_stats:
        for code in problem_stats[p]:
            solved[code]=True
    return solved