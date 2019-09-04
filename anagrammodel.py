from google.appengine.ext import ndb

class Anagram(ndb.Model):
    user = ndb.StringProperty()
    anagram_words = ndb.StringProperty(repeated=True)
    anagram_count = ndb.IntegerProperty()
    letter_count = ndb.IntegerProperty()
