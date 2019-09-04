import webapp2
import jinja2
import os
from google.appengine.api import users
import logging
from google.appengine.ext import ndb
from user import User
from anagrammodel import Anagram
from account import Account

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        url = ''
        url_string = ''
        user = users.get_current_user()
        logging.info(user)
        message = "welcome to my page"
        my_user = ""
        myuser = ""
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'

            user_key = ndb.Key('User', user.email())
            my_user = user_key.get()

            if my_user == None:
                welcome = 'Welcome to the application'
                myuser = User(id=user.email(), email_address=user.email(), count_word=0, count_anagram=0)
                myuser.put()
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        logging.info(my_user)
        # current_user = ndb.Key('User', user.email())
        # current_user = current_user.get()
        # logging.info(current_user.count_anagram)
        data_values = {
            "welcome": message,
            "url": url,
            "url_string": url_string,
            "current_user": myuser

        }
        logging.info(data_values)

        print(data_values)

        template = JINJA_ENVIRONMENT.get_template('home.html')
        self.response.write(template.render(data_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        word = self.request.get('word')
        current__user = Account.getUser(self)

        logging.info(word)
        string = list(word)
        string.sort()
        string = ''.join(string)
        key = user.email() + '/' + string

        anagram_key = ndb.Key('Anagram', key)
        anagrams = anagram_key.get()
        logging.info(anagrams)

        current_user = ndb.Key('User', user.email())
        current_user = current_user.get()
        logging.info(current_user)
        if anagrams:

            anagram_list = {
                "anagrams": anagrams.anagram_words,
                "current_user": current_user,
                "url": current__user["login_url"],
                "url_string": current__user["login_text"],
                "current_user": current__user["user"]
            }
        else:
            anagram_list = {
                "anagrams": [],
                "current_user": current_user,
                "url": current__user["login_url"],
                "url_string": current__user["login_text"],
                "current_user": current__user["user"],
                "error": True
            }

        template = JINJA_ENVIRONMENT.get_template('home.html')
        self.response.write(template.render(anagram_list))
        logging.info(word)


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
