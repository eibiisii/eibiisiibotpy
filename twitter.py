# -*- coding: utf-8 -*-

import tweepy

CONSUMER_KEY = '自分の'
CONSUMER_SECRET = '自分の'

TOKEN_KEY = '自分の'
TOKEN_SECRET = '自分の'

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
