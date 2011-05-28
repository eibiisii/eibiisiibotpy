#coding:utf-8
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import urllib
import urllib2
from BeautifulSoup import BeautifulSoup

class MyHTMLParser(object):
	def getFromC(self):
		html = self.getHTML('http://cookpad.com/recipe/hot','utf-8')
		soup = BeautifulSoup(html)
		findlist = soup.findAll('a',{'class' : 'recipe-title'})
		return findlist

	def getFromS(self):
		html = self.getHTML('http://www.genkotsu-hb.com/news/','utf-8')
		soup = BeautifulSoup(html)
		findlist = soup.findAll('h2')
		return findlist

	def getHTML(self, url, decode):
		html = urllib2.urlopen(url).read().decode(decode,'replace')
		return html
    	
    	
    	
"""    
def main():
	application = webapp.WSGIApplication([('/myparse', TestDriver)],
                                         debug=True)
	util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
"""
