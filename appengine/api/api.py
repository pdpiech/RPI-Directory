from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import logging
import cgi
import urllib
from models import Person

class Api(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    year  = urllib.unquote( cgi.escape(self.request.get('year' )) )
    major = urllib.unquote( cgi.escape(self.request.get('major')) )
    name  = urllib.unquote( cgi.escape(self.request.get('name' )) )
    
    query = Person.all()
    
    if year is not "":
      query = query.filter('year = ',year)
    if major is not "":
      query = query.filter('major = ',major)
    
    names = name.split()[:3]
    if len(names) > 0:
      query = query.filter('first_name = ', names[0])
    if len(names) > 1:
      query = query.filter('last_name = ', names[-1])
    if len(names) > 2:
      query = query.filter('middle_name = ', names[1])
    
    people = query.fetch(100)
    
    if len(names) == 1:
      query = Person.all()
      if year is not "":
        query = query.filter('year = ',year)
      if major is not "":
        query = query.filter('major = ',major)
      query = query.filter('last_name = ', names[0])
      people.extend(query.fetch(100))
    
    l = []
    
    for p in people:
      l.append(Person.buildMap(p))
    s = repr(l)
    s = s.replace('"',"'")
    self.response.out.write(s)
    

application = webapp.WSGIApplication(
  [
    ("/api/", Api)
  ])
   
def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()