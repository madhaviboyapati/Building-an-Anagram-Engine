import webapp2
import jinja2
import os
from anagrammodel import Anagram
import logging

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class SearchAnagramPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        template = JINJA_ENVIRONMENT.get_template('searchanagram.html')
        self.response.write(template.render({}))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        word = self.request.get('word')
        logging.info(word)
        template = JINJA_ENVIRONMENT.get_template('searchanagram.html')
        self.response.write(template.render({}))


app = webapp2.WSGIApplication([
    ('/searchanagram', SearchAnagramPage),
], debug=True)
