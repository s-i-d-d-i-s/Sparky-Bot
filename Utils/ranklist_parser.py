import requests
import json
import pickle
import os
from .constants import headers
import time

def saveRanklist(CONTEST):
	if os.path.isfile("Data/ContestRanklists/"+CONTEST+".cache"):
		return  f"{CONTEST} already saved !"

	url = f"https://www.codechef.com/rankings/{CONTEST}?filterBy=&order=asc&sortBy=rank"
	params = (
		('sortBy', 'rank'),
		('order', 'asc'),
		('page', '1'),
		('itemsPerPage', '100'),
	)

	response = json.loads(requests.get('https://www.codechef.com/api/rankings/{}'.format(CONTEST), headers=headers, params=params).content)
	pages = response['availablePages']
	print("Available Pages : {}".format(pages))  
	res = []
	for i in range(pages):
		if i%5==0:
			time.sleep(10)
		params = (
			('sortBy', 'rank'),
			('order', 'asc'),
			('page', i+1),
			('itemsPerPage', '100'),
		)
		print("Scanning Page No : {}".format(i+1))
		response = json.loads(requests.get('https://www.codechef.com/api/rankings/{}'.format(CONTEST), headers=headers, params=params).content)
		for r in response['list']:
			if CONTEST.find("COOK")!=-1:
				res.append([r['user_handle'],r['score']])
			else:
				res.append([r['user_handle'],str(r['score'])+" Pts"])
	dbfile = open(f'Data/ContestRanklists/{CONTEST}.cache', 'wb') 
	pickle.dump(res, dbfile)
	dbfile.close()

	return f"Saved {CONTEST}"




def getRanklist(CONTEST,botmode=0):
    pages = 1
    res = []
    items = 100
    if botmode==1:
        pages=1
        items = 25
    else:
        url = f"https://www.codechef.com/rankings/{CONTEST}?filterBy=&order=asc&sortBy=rank"
        params = (
            ('sortBy', 'rank'),
            ('order', 'asc'),
            ('page', '1'),
            ('itemsPerPage', items),
        )
        response = json.loads(requests.get('https://www.codechef.com/api/rankings/{}'.format(CONTEST), headers=headers, params=params).content)
        pages = response['availablePages']
        print("Available Pages : {}".format(pages))  


    for i in range(pages):
        params = (
            ('sortBy', 'rank'),
            ('order', 'asc'),
            ('page', i+1),
            ('itemsPerPage', items),
        )
        print("Scanning Page No : {}".format(i+1))
        response = json.loads(requests.get('https://www.codechef.com/api/rankings/{}'.format(CONTEST), headers=headers, params=params).content)
        for r in response['list']:
            if botmode==1:
                if CONTEST.find("COOK")!=-1:
                    res.append([r['user_handle'],r['score']])
                else:
                    res.append([r['user_handle'],str(r['score'])+" Pts"])
            else:
                res.append(r['user_handle'])
    return res
