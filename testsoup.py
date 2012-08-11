#coding:utf-8
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import urllib
import urllib2
from BeautifulSoup import BeautifulSoup

APP_ID = ""  # 登録したアプリケーションID
PAGE_URL = "http://jlp.yahooapis.jp/MAService/V1/parse"
KEY_PHRASE_URL = "http://jlp.yahooapis.jp/KeyphraseService/V1/extract"

class TestSoup(object):   
    def getFromY(self,sentence):
        self.sentence = sentence
        result = self.morph(self.sentence, filter="9")
        return result

    def getKeyPhrase(self,sentence):
    	sentence = urllib.quote_plus(sentence.encode("utf-8"))
    	query = u"%s?appid=%s&sentence=%s" % (KEY_PHRASE_URL,APP_ID,sentence)
    	c = urllib2.urlopen(query)
    	soup = BeautifulSoup(c.read())
	return soup.result.keyphrase.string

# 形態素解析した結果をリストで返す
    def morph(self, sentence, results="uniq", filter="1|2|3|4|5|6|7|8|9|10|11|12|13"):
        #ret = []
        # 文章をURLエンコーディング
        sentence = urllib.quote_plus(sentence.encode("utf-8"))
        query = "%s?appid=%s&results=%s&filter=%s&sentence=%s" % (PAGE_URL, APP_ID, results, filter, sentence)
        c = urllib2.urlopen(query)
        soup = BeautifulSoup(c.read())
	#return soup
        return [w.surface.string for w in soup.uniq_result.word_list]
"""
def main():
	application = webapp.WSGIApplication([('/soup', TestSoup)],
                                         debug=True)
	util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
"""
