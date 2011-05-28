# -*- coding: utf-8 -*-

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from twitter import TwitterAuth
from testsoup import TestSoup
from myhtmlparser import MyHTMLParser

import cgi
import os
from google.appengine.ext.webapp import template

import random
import re
import urllib2
import random

import unicodedata

class Status(db.Model):
	content = db.StringProperty()

class SinceId(db.Model):
	sinceid = db.StringProperty()

class Often(db.Model):
	word = db.StringProperty()

class Money(db.Model):
	category = db.StringProperty()
	money = db.IntegerProperty()
	date = db.DateTimeProperty(auto_now_add=True)

class OsusumeMyId(db.Model):
	statusid = db.StringProperty()

class Osusume(db.Model):
	user_name = db.StringProperty()
	osusume = db.StringProperty()

class Update(webapp.RequestHandler):
	def get(self):
		twitter = TwitterAuth()
		twitterapi = twitter.getAuth()
		#p = Status(content=u"できたかなー")
		#p.put()
		posts_query = Status.all()
		posts = posts_query.fetch(1000)
		post = posts[random.randint(0,len(posts)-1)].content
		self.response.out.write(post)
		twitter.update(twitterapi,post)

class TestKeyPhrase(webapp.RequestHandler):
	def get(self):
		soup = TestSoup()
		keyphrase = soup.getKeyPhrase("")
		self.response.out.write(keyphrase)

class ReplyUpdate(webapp.RequestHandler):
	def get(self):
		twitter = TwitterAuth()
		twitterapi = twitter.getAuth()
		key = db.Key.from_path('SinceId','m_last')
		now_sinceid = db.get(key).sinceid
		self.response.out.write(now_sinceid)
		now_sinceid = long(now_sinceid)
		mentionlist = twitterapi.mentions(now_sinceid)
		if len(mentionlist) != 0:
			mentionlist.reverse()
			cooking = Cooking()
			findlist = cooking.doParse()
			#osusumeMyIdList = OsusumeMyId.all()
			#osusumeMyIdLists = osusumeMyIdList.fetch(1000)
			for line in mentionlist:
				'''
				for osusumeMyId in osusumeMyIdLists:
					if str(line.in_reply_to_status_id) == osusumeMyId.statusid:
						category_name = osusumeMyId.key().name()
						#str(category_name)
						self.response.out.write(u'成功だよ！')
						soup = TestSoup()
						line_text = line.text.replace('@eibiisii_bot','')
						osusume_good = soup.getKeyPhrase(line_text)
						self.response.out.write(osusume_good)
						#osusume_good = str(osusume_good)
						status = u'「%s」' % osusume_good
						statusid = line.id
						screen_name = line.user.screen_name
						#screen_name = str(screen_name)
						text = u'@%s %s　へー' % (screen_name,status)
						twitter.reply_update(twitterapi,text,statusid)
						self.response.out.write(text)
						osusume_good = unicode(str(osusume_good),'utf-8')
						o = Osusume(user_name=screen_name,osusume=osusume_good)
						o.put()
						break
					continue
				'''
				if u'料理' in line.text:
					rnd = random.randint(0,len(findlist)-1)
					status = u'これつくってー！ / %s %s' % (findlist[rnd].string, findlist[rnd]['href'])
					screen_name = line.user.screen_name
					statusid = line.id
					text = u"@%s %s" % (screen_name,status)
					twitter.reply_update(twitterapi,text,statusid)
					self.response.out.write(text)
				else:
					continue
			new_sinceid = mentionlist.pop().id
			d = SinceId(key_name="m_last",sinceid=str(new_sinceid))
			d.put()

class CheckDM(webapp.RequestHandler):
	def get(self):
		twitter = TwitterAuth()
		twitterapi = twitter.getAuth()
		#money = Money(category=u'',money=150)
		#money.put()
		key = db.Key.from_path('SinceId','dm_last')
		now_sinceid = db.get(key).sinceid
		self.response.out.write(now_sinceid)
		now_sinceid = long(now_sinceid)
		dmlist = twitterapi.direct_messages(now_sinceid)
		p = re.compile(u'(.+)?＠(\d+)?円')
		if len(dmlist) != 0:
			dmlist.reverse()
			for line in dmlist:
				#self.response.out.write(line.text)
				#self.response.out.write(line.id)
				#self.response.out.write(line.sender_id)
				#self.response.out.write(line.sender_screen_name)
				#self.response.out.write(line.created_at)
				if line.sender_screen_name == 'eibiisii':
					if u'円' and u'＠' in line.text:
						a = p.search(line.text)
						self.response.out.write(a.group(1))
						self.response.out.write(" ")
						self.response.out.write(a.group(2))
						self.response.out.write(" ")
						money = Money(category=a.group(1),money=int(a.group(2)),date=line.created_at)
						money.put()
			twitter.update(twitterapi,u'@eibiisii できたよ！')
			now_sinceid = dmlist.pop().id
			self.response.out.write(now_sinceid);
			t = SinceId(key_name="dm_last",sinceid=str(now_sinceid))
			t.put()
		else:
			self.response.out.write(u'DMないよ！');


class Timeline(webapp.RequestHandler):
	def get(self):
		twitter = TwitterAuth()
		twitterapi = twitter.getAuth()
		key = db.Key.from_path('SinceId','tl_last')
		now_sinceid = db.get(key).sinceid
		self.response.out.write(now_sinceid)
		now_sinceid = long(now_sinceid)
		tl = twitterapi.friends_timeline(since_id=now_sinceid)
		texts = ''
		i = 1
		for line in tl:
			if i==1:
				now_sinceid = line.id
				i = i+1
			text = line.text
			if '@' in text:
				text = re.sub('@\w+?\s','',text)
			self.response.out.write(text)
			self.response.out.write("<br />")
			texts = '%s%s' % (texts,text)
		self.response.out.write(texts)
		self.response.out.write(now_sinceid)
		t = SinceId(key_name="tl_last",sinceid=str(now_sinceid))
		t.put()

class XMLParser(webapp.RequestHandler):
	def deleteObstacle(self,text):
		if '@' in text:
			text = re.sub('@\w+?[\s:]','',text)
		if 'http' in text:
			text = re.sub("s?https?://[-_.!~*'()a-zA-Z0-9;/?:@&=+$,%#]+","",text)
		if 'Photo:' in text:
			text = text.replace('Photo:','')
		if 'RT' in text:
			text = re.sub('RT:?','',text)
		return text

	def checkMany(self,results):
		manylist = []
		prev = ''
		count = 1
		listin = False
		p = re.compile('\d+')
		p2 = re.compile('[wｗ]+')
		for a in results:
			a = unicodedata.normalize('NFKC',a) # 全角半角正規化
			if prev == '':
				prev = a
			if prev != a:
				count = 1 # 初期化
				prev = a
			if prev == a:
				if self.doFilter(a):# よく使う言葉だったらコンティニュー
					continue
				if re.search(p,a):# 数字だったらコンティニュー
					continue
				if re.search(p2,a):# ｗだったらコンティニュー
					continue
				count = count + 1
				if count > 2:
					manylist.append(a)
					listin = True
					self.response.out.write(a)
					self.response.out.write('<br />')
					#d = Often(word=a)
					#d.put()
		if listin:
			manylist = sorted(set(manylist)) # 重複を削除してソート
		return manylist

	def get(self):
		twitter = TwitterAuth()
		twitterapi = twitter.getAuth()
		tl = twitterapi.friends_timeline()
		#texts = ''
		results = []
		soup = TestSoup()
		for line in tl:
			# @、URL、Photo、RTなどの文字列を弾く
			text = self.deleteObstacle(line.text)
			result = soup.getFromY(text) # 配列が返ってくる
			for w in result:
				results.append(w)
		#for b in results:
		#	self.response.out.write(b)
		#	self.response.out.write('<br />')
		#self.response.out.write('-----------------------<br />')
		updateText = ''
		if len(results)!=0:
			results.sort()
			manylist = self.checkMany(results)
			if len(manylist)!=0:
				text = u'と'.join(manylist)
				updateText = u'%sが盛り上がってるかも！' % text
			else:
				updateText = u'(´･ω･`)うーん'
		else:
			updateText = u'(´･ω･`)あれ？'
		self.response.out.write(updateText)
		twitter.update(twitterapi,updateText)

#	def makeUpdateText(self,manylist):
#		text = ''
#		count = 0
#		size = len(manylist)
#		andtext = ''
#		for many in manylist:
#			count += 1
#			if count<size:
#				andtext = u'と'
#			else:
#				andtext = ''
#			text = '%s%s%s' % (text,many,andtext)
#		updateText = u'%sが盛り上がってるかも！'
#		return updateText

	def doFilter(self,content):
		if content in u'私、俺、自分、おれ、わたし、人':
			return True
		elif content in u'今日、明日、今':
			return True
		elif content in u'これ、それ、あれ、どれ':
			return True
		elif content in u'こと、もの':
			return True
		elif content in u'どの、どこ、何':
			return True
		else:
			return False
		
class Cooking(webapp.RequestHandler):
	def get(self):
		findlist = self.doParse()
		twitter = TwitterAuth()
		twitterapi = twitter.getAuth()
		rnd = random.randint(0,len(findlist)-1)
		tweet = u'@eibiisii これつくってー！ / %s %s' % (findlist[rnd].string, findlist[rnd]['href'])
		twitter.update(twitterapi,tweet)
		self.response.out.write(tweet)
	def doParse(self):
		parse = MyHTMLParser()
		findlist = parse.getFromC()
		return findlist

class Recomend(webapp.RequestHandler):
	def get(self):
		twitter = TwitterAuth()
		twitterapi = twitter.getAuth()
		categories = [u'漫画',u'映画',u'音楽',u'アニメ']
		index = random.randint(0,len(categories)-1)
		tweet = u'@eibiisii6 ！' % categories[index]
		twitter.update(twitterapi,tweet)
		mytweets = twitterapi.user_timeline(screen_name = 'eibiisii_bot',count = 1)
		if len(mytweets) != 0:
			last_tweet_id = mytweets[0].id
			self.response.out.write(last_tweet_id)
			o = OsusumeMyId(key_name = categories[index],statusid = str(last_tweet_id))
			o.put()

class Sawayaka(webapp.RequestHandler):
	def get(self):
		parse = MyHTMLParser()
		findlist = parse.getFromS()
		url = 'http://www.genkotsu-hb.com/'
		for find in findlist:
			text = find.string
			self.response.out.write(text)
			if u'創業価格フェア' in text:
				text = '%s%s%s%s' % (u'@eibiisii 「',text,u'」だって！―炭焼きレストランさわやか ',url)
				self.response.out.write(text)
				twitter = TwitterAuth()
				twitterapi = twitter.getAuth()
				twitter.update(twitterapi,tweet)


application = webapp.WSGIApplication(
                                    [
                                     ('/update', Update),
                                     ('/timeline', Timeline),
                                     ('/parse',XMLParser),
                                     ('/cooking',Cooking),
                                     ('/reply',ReplyUpdate),
                                     ('/checkdm',CheckDM),
                                     ('/recomend',Recomend),
				     ('/keyphrase',TestKeyPhrase),
				     ('/sawayaka',Sawayaka),
                                    ],
                                     debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
