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
    #id = db.Key.from_path.("UserSubmission", int(id))


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
#            moving to NewPostHandler class
#            w = UserSubmission(title=title, wordart=wordart)
#            w.put()
            self.redirect("/newpost")
        else:
            error = "A title and blog content are required."
            self.render_blog(title, wordart, error)

class NewPostHandler(Handler): #Do I want it to inherit from MainPage?

    def render_blog_post(self, title="", wordart=""):
        self.render("newpost.html", title=title, wordart=wordart)

    def get(self):
        w = UserSubmission(title=title, wordart=wordart)
        w.put()
        w.render_blog_post()

class ViewPostHandler(webapp2.RequestHandler):
    #pass
    def get(self, id):
        #blog_id = UserSubmission(id=id)
        #return blog_id
        #id=5
        self.response.write(5)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    #('/blog', BlogHandler),
    ('/newpost', NewPostHandler),
    (webapp2.Route('/blog/<id:\d+>', ViewPostHandler))
    #('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
