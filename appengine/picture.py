import webapp2
from google.appengine.api import users
from google.appengine.api import images
import logging
from models import Person
import base64

admins = ['christian@christianjohnson.org',
          'jewishdan18@gmail.com',
          'michorowitz@gmail.com']

unknown_image = """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"""

class UploadProfilePic(webapp2.RequestHandler):
  def post(self):
    user = users.get_current_user()
    if user:
      if user.email() in admins:
        #Allow picture replacement for admins
        person = Person.get_by_id(self.request.get('rcsid'))
      else:
        person = Person.query(Person.linked_account == user).get()
      if person:
        person.picture = images.resize(self.request.get('file'), width=200, height=200,
                                       correct_orientation=True)                 
        person.put()
        logging.info('Uploaded Picture: ' + person.rcsid)
        return
    else:
      logging.info('Not Logged in to Modify Image')
    
class Image(webapp2.RequestHandler):
  def get(self, rcsid):
    person = Person.get_by_id(rcsid)
    if person and person.has_picture:
      self.response.headers['Content-Type'] = 'image/png'
      self.response.out.write(person.picture)
    else:
      self.response.headers['Content-Type'] = 'image/png'
      self.response.out.write(base64.b64decode(unknown_image))

app = webapp2.WSGIApplication([('/upload_picture', UploadProfilePic),
                               ('/picture/([^/]+)', Image)])