#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
#import cgi
from google.appengine.ext import db

# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *args, **kwargs):
        self.response.out.write(*args, **kwargs)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kwargs):
        self.write(self.render_str(template, **kwargs))

class UserSubmission(db.Model):
    title = db.StringProperty(required = True)
    wordart = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):
    def render_blog(self, title="", wordart="", error=""):
        wordvomit = db.GqlQuery("""select * from UserSubmission
                            order by created desc limit 5""")
        self.render("blog.html", title=title, wordart=wordart,
                    error=error, wordvomit=wordvomit)

    def get(self):
        self.render_blog()

    def post(self):
        title = self.request.get("title")
        wordart = self.request.get("wordart")

        if title and wordart:
            w = UserSubmission(title=title, wordart=wordart)
            w.put()

            self.redirect("/")
        else:
            error = "We require your title and your blog content."
            self.render_blog(title, wordart, error)

# class ViewPostHandler(webapp2.RequestHandler):
#     def get(self, id):
#         pass

app = webapp2.WSGIApplication([
    ('/', MainPage),
    #('/blog', BlogHandler),
    #('/newpost', NewPostHandler),
    #(webapp2.Route('/blog/<id:\d+>', ViewPostHandler))
], debug=True)
