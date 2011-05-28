# -*- coding: utf-8 -*-

import tweepy

CONSUMER_KEY = 'w6yw70NmTOWXl1K1v3U1gQ'
CONSUMER_SECRET = 'zyMM9q6iXAGjdcRArhzvJxCixxrbGXVbC3o3b9X3PE'

TOKEN_KEY = '116679230-bTMZj6uCijl89SooB2IfJjYoRArH55umB3M1EUsw'
TOKEN_SECRET = 'xMgY6jGazd3VxIsMp3Er5mzowjR8uUuX7y0IEAeCyo'

class TwitterAuth(object):
	def getAuth(self):
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(TOKEN_KEY,TOKEN_SECRET)
		oauthapi = tweepy.API(auth)
		return oauthapi

	def update(self,oauthapi,post):
		oauthapi.update_status(post.encode('utf-8'))

	def reply_update(self,oauthapi,post,id):
		oauthapi.update_status(post.encode('utf-8'),id)
