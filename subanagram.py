import webapp2
import jinja2
import os
from anagrammodel import Anagram
import logging
import itertools
from google.appengine.api import users
from google.appengine.ext import ndb
from account import Account

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class SubAnagramPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        current_user = Account.getUser(self)

        template = JINJA_ENVIRONMENT.get_template('subanagram.html')
        self.response.write(template.render({"url": current_user["login_url"],"url_string": current_user["login_text"], "current_user": current_user["user"]}))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        current_user = Account.getUser(self)
        word = self.request.get('word')
        logging.info(word)
        subs = []
        anagrams = [];
        for i in range(len(word) - 1, 2, -1):
            result = itertools.combinations(list(word), i)
            for val in list(result):
                subs.append("".join(val))
        logging.info(subs)
        for term in subs:

            string = list(term)
            string.sort()
            string = ''.join(string)
            key = user.email() + '/' + string
            anagram_key = ndb.Key('Anagram', key)
            anagram = anagram_key.get()
            logging.info(anagram)
            if anagram:
                anagrams.extend(anagram.anagram_words)

        logging.info(anagrams)
        error = False
        if len(anagrams)==0:
            error = True

        template = JINJA_ENVIRONMENT.get_template('subanagram.html')
        self.response.write(template.render({"anagrams": anagrams,"url": current_user["login_url"],"url_string": current_user["login_text"], "current_user": current_user["user"],"error":error}))


app = webapp2.WSGIApplication([
    ('/subanagram', SubAnagramPage),
], debug=True)