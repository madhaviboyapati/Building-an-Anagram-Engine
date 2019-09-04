from user import User
from google.appengine.api import users
from google.appengine.ext import ndb


class Account:
    @classmethod
    def getUser(cls, request):
        user = users.get_current_user()
        url = ""
        url_string = ""
        my_user = ""

        if user:
            url = users.create_logout_url(request.request.uri)
            url_string = 'logout'

            user_key = ndb.Key('User', user.email())
            my_user = user_key.get()

            if my_user == None:
                myuser = User(id=user.email(), email_address=user.email(), count_word=0, count_anagram=0)
                myuser.put()
        else:
            url = users.create_login_url(request.request.uri)
            url_string = 'login'

        return {"login_url":url, "login_text":url_string,"user":my_user}


