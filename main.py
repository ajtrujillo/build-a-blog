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
    words = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

#landing page handler where user submits a title and body
class NewPost(Handler):

    def render_blog_form(self, title="", words="", error=""):
        self.render("newpost.html", title=title, words=words,
                    error=error)

    def get(self):
        self.render_blog_form()

    def post(self):
        title = self.request.get("title")
        words = self.request.get("words")
        post = UserSubmission(title=title, words=words)
        post.put()

        if title and words:
            self.redirect("/list")
            return

        else:
            error = "A title and blog content are required."
            self.render_blog_form(title, words, error)

#handler where we can see just the last post submitted in its entirety
class ViewPostHandler(Handler):

    def get(self, blog_id):
        submission = UserSubmission.get_by_id(int(blog_id))

        if submission:
            self.render("blog.html", submission=submission)

        else:
            error = "There is no blog post with that ID."
            self.render("blog.html", error=error)


#handler to see list of last five posts
class ListHandler(Handler):

    def get(self):
        blog_list = db.GqlQuery("""select * from UserSubmission order by created desc limit 5""")
        self.render("list.html", blog_list=blog_list)


app = webapp2.WSGIApplication([
    ('/newpost', NewPost),
    webapp2.Route('/blog/<blog_id:\d+>', ViewPostHandler),
    ('/list', ListHandler),
], debug=True)
