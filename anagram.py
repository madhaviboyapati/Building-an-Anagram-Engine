import webapp2
import jinja2
import os
from google.appengine.api import users
import logging
from google.appengine.ext import ndb
from user import User

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Anagram(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        url = ''
        url_string = ''
        user = users.get_current_user()
        logging.info(user)
        message = "welcome to my page"
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'

            user_key = ndb.Key('User', user.user_id())
            my_user = user_key.get()

            if my_user == None:
                welcome = 'Welcome to the application'
                myuser = User(id=user.user_id(), email_address=user.email())
                myuser.put()



        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        logging.info(user)

        data_values = {
            "welcome": message,
            "url": url,
            "url_string": url_string

        }
        logging.info(data_values)

        print(data_values)

        template = JINJA_ENVIRONMENT.get_template('addanagram.html')
        self.response.write(template.render(data_values))


app = webapp2.WSGIApplication([
    ('/addanagram', Anagram),
], debug=True)
