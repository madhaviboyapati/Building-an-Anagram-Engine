import webapp2
import jinja2
import os
from anagrammodel import Anagram
import logging
from account import Account
from google.appengine.api import users

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from user import User

from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class UploadAnagramPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        current_user = Account.getUser(self)
        upload_url = blobstore.create_upload_url('/upload')
        done = self.request.params

        template = JINJA_ENVIRONMENT.get_template('uploadanagram.html')
        self.response.write(template.render({"url": current_user["login_url"],"url_string": current_user["login_text"], "current_user": current_user["user"], "upload_url":upload_url,"done":done}))

    def post(self):
        pass
        # self.response.headers['Content-Type'] = 'text/html'
        # user = users.get_current_user()
        # current_user = Account.getUser(self)
        #
        # word = self.request.get('word')
        # logging.info(word)
        # template = JINJA_ENVIRONMENT.get_template('uploadanagram.html')
        # self.response.write(template.render({"url": current_user["login_url"],"url_string": current_user["login_text"], "current_user": current_user["user"]}))


class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        user = users.get_current_user()
        upload = self.get_uploads()[0]
        logging.info(upload)
        blob_reader = blobstore.BlobReader(upload.key())
        for word in blob_reader.readlines():
            logging.info(word.rstrip())
            word = word.rstrip()
            logging.info(word)
            string = list(word)
            string.sort()
            string = ''.join(string)
            key = user.email() + '/' + string
            anagram_key = ndb.Key('Anagram', key)
            anagrams = anagram_key.get()
            logging.info(anagrams)
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

        self.redirect('/uploadanagram?done=done')


app = webapp2.WSGIApplication([
    ('/uploadanagram', UploadAnagramPage),
    ('/upload', PhotoUploadHandler)
], debug=True)
