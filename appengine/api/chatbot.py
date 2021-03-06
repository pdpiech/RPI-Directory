from google.appengine.api import xmpp
from google.appengine.ext.webapp import xmpp_handlers
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache
from google.appengine.api import urlfetch
import urllib

import logging
import cgi
import urllib
import webapp2

class ChatHandler(webapp2.RequestHandler):
  def post(self):
    message = xmpp.Message(self.request.POST)
    query = message.body.lower()
    search_string = urllib.quote(query)
    message.reply("Searching...try again in a few seconds if I don't get back to you :)")
    url = 'http://rpidirectory.appspot.com/api?q=' + search_string + '&page_size=3&page_num=1&source=chatbot'

    rpc = urlfetch.create_rpc(deadline=20)
    urlfetch.make_fetch_call(rpc, url)
    text = ''
    try:
      result = rpc.get_result()
      if result.status_code == 200:
          text = result.content
      else:
        message.reply("An internal error occured, please try again in a few minutes.")
        return
    except urlfetch.DownloadError:
      message.reply("A different internal error occured, please try again in a few minutes.")
      return

    #result = urlfetch.fetch(url, deadline=20)
    #if result.status_code != 200:
      #message.reply("An internal error occured, please try again in a few minutes.")
      #return

    s = ''
    d = eval(text)

    resultCount = 3

    for person in d['data']:
      if resultCount <= 0:
        break
      resultCount -= 1
      s += '*' + person['name'] + "*\n"
      #s += '('

      if 'email' in person:
        s += person['email'] + '\n'

      if 'major' in person:
        s += person['major'] + '\n'
      elif 'department' in person:
        s += person['department'] + '\n'

      if 'year' in person:
        s += person['year'] + '\n'
      elif 'title' in person:
        s += person['title'] + '\n'
      else:
        s += 'Faculty\n'
      #s += ')\n'
    if s == '':
      s = "No results found"
    message.reply(s)



app = webapp2.WSGIApplication([
    ("/_ah/xmpp/message/chat/", ChatHandler)
  ])
