import webapp2
import jinja2
import os
#import cgi
from google.appengine.ext import db

# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

# making a helper class
class Handler(webapp2.RequestHandler):
    def write(self, *args, **kwargs):
        self.response.out.write(*args, **kwargs)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kwargs):
        self.write(self.render_str(template, **kwargs))

#gql stuff here
class UserSubmission(db.Model):
    title = db.StringProperty(required = True)
    wordart = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    #id = db.Key.from_path.("UserSubmission", int(id))


class MainPage(Handler):
    def render_blog_form(self, title="", wordart="", error=""):
        self.render("blog.html", title=title, wordart=wordart,
                    error=error)

    def get(self):
        self.render_blog_form()

    def post(self):
        title = self.request.get("title")
        wordart = self.request.get("wordart")

        if title and wordart:
            self.redirect("/newpost")
            return

        else:
            error = "A title and blog content are required."
            self.render_blog(title, wordart, error)


class ViewPostHandler(Handler):

    def render_blog_post(self, title="", wordart=""):
        blog_post= db.GqlQuery("""select * from UserSubmission where id == %s""" %(id))
        self.render("newpost.html", title=title, wordart=wordart, id=id)

    def get(self, id):
        #blog_id = UserSubmission(id=id)
        #return blog_id
        #id=5
        self.response.write(5)
        #post.key().id()
        self.render_blog_post(!!!!)

    def post(self):
         title = self.request.get("title")
         wordart = self.request.get("wordart")
         usersubmission = UserSubmission(title=title, wordart=wordart)
         usersubmission.put()
         usersubmission.render_blog_post()


class ListHandler(Handler):
    def get(self):
        blog_list = db.GqlQuery("""select * from UserSubmission
                            order by created desc limit 5""")
        self.render("blog.html", title=title, wordart=wordart,
                    error=error, blog_list=blog_list)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    (webapp2.Route('/blog/<id:\d+>', ViewPostHandler)),
    #('/blog', BlogHandler),
    ('/newpost', NewPostHandler),

    #('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
