import webapp2
import jinja2
import os
from anagrammodel import Anagram
import logging
from user import User
from google.appengine.api import users
from google.appengine.ext import ndb

from account import Account

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class AddAnagramPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()
        current_user = Account.getUser(self)

        template = JINJA_ENVIRONMENT.get_template('addanagram.html')
        self.response.write(template.render({"url": current_user["login_url"],"url_string": current_user["login_text"], "current_user": current_user["user"]}))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        current_user = Account.getUser(self)
        word = self.request.get('word')
        logging.info(word)
        string = list(word)
        string.sort()
        string = ''.join(string)
        key = user.email() + '/' + string
        anagram_key = ndb.Key('Anagram', key)
        anagrams = anagram_key.get()
        logging.info(anagrams)
        done = False
        if anagrams:
            if word not in anagrams.anagram_words:
                anagrams.anagram_words.append(word)
                anagrams.anagram_count = anagrams.anagram_count + 1
                anagrams.put()

                user_key = ndb.Key('User', user.email())
                user1 = user_key.get()
                user1.count_anagram = user1.count_anagram + 1
                user1.put()
        else:

            newAnagram = Anagram(id=key, anagram_words=[word], user=user.email(), anagram_count=1,
                                 letter_count=len(word))
            newAnagram.put()

            user_key = ndb.Key('User', user.email())
            user1 = user_key.get()
            user1.count_word = user1.count_word + 1
            user1.count_anagram = user1.count_anagram + 1
            user1.put()
        done = True

        template = JINJA_ENVIRONMENT.get_template('addanagram.html')
        self.response.write(template.render({"url": current_user["login_url"],"url_string": current_user["login_text"], "current_user": current_user["user"], 'done':done}))


app = webapp2.WSGIApplication([
    ('/addanagram', AddAnagramPage),
], debug=True)
