from Crawler import Crawler
from models import SearchPosition

import cgi
import datetime
import urllib
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.api import memcache
from google.appengine.ext.webapp.util import run_wsgi_app


class Driver(webapp.RequestHandler):
  def get(self):
    self.response.out.write('<html><body>')
    index = memcache.get("index")

    if not index:
	  index_from_ds = SearchPosition.get_by_key_name("index")
	  if not index_from_ds:
		index = 1
		#Add it to datastore
		SearchPosition(key_name="index", position=index).put()
	  else:
	  	index = index_from_ds.position
	result = Crawler.getMap(index)

	if result:
	  self.response.out.write("Found something")
	else:
	  self.response.out.write("Didn't find something")

	#Update Memcache
	if not memcache.add("index", index + 1, 86400):
	  logging.error("Memcache set failed")

	#Update DataStore
	index_from_ds = SearchPosition.get_by_key_name("index")
	index_from_ds.position = (index + 1)
	index_from_ds.put()
	
application = webapp.WSGIApplication([
  ("/crawl/.*", Driver)
  ])

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()