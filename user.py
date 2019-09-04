from google.appengine.ext import ndb


class User(ndb.Model):
    # email address of this user
    email_address = ndb.StringProperty()
    count_word = ndb.IntegerProperty()
    count_anagram = ndb.IntegerProperty()
