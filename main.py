import webapp2
import re
import cgi


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
PW_RE = re.compile(r"^.{3,20}$")


def valid_username(username):
    return USER_RE.match(username)


def valid_password(password):
    return PW_RE.match(password)


def valid_email(email):
    return EMAIL_RE.match(email)


def validate_inputs(username, password, verify, email):
    dict = {}
    if username and valid_username(username):
        dict['username'] = username
        dict['error_username'] = ''
    else:
        dict['username'] = username
        dict['error_username'] = 'Invalid Username'

    if not valid_password(password):
        dict['password'] = ''
        dict['error_password'] = 'Invalid Password'
        dict['verify'] = ''
        dict['error_verify'] = ''
    elif valid_password(password) and password == verify:
        dict['password'] = ''
        dict['error_password'] = ''
        dict['verify'] = ''
        dict['error_verify'] = ''
    else:
        dict['password'] = ''
        dict['error_password'] = ''
        dict['verify'] = ''
        dict['error_verify'] = 'Invalid Password Verification'

    if email and valid_email(email):
        dict['email'] = email
        dict['error_email'] = ''
    elif email and not valid_email(email):
        dict['email'] = email
        dict['error_email'] = 'Invalid Email'
    else:
        dict['email'] = ''
        dict['error_email'] = ''

    for key in dict:
        dict[key] = cgi.escape(dict[key], quote=True)

    return dict


header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
        label {
            font-size: 13px;
        }
    </style>
</head>
<body>
"""

footer = """
</body>
</html>
"""

form_html = """
<form action="/signup" method="post">
    <h2>Signup</h2>
    <label>USERNAME</label><br>
    <input type="text" name="username" value="{username}">
    <span class="error">{error_username}</span><br>
    <label>PASSWORD</label><br>
    <input type="password" name="password" value="{password}">
    <span class="error">{error_password}</span><br>
    <label>VERIFY PASSWORD</label><br>
    <input type="password" name="verify" value="{verify}">
    <span class="error">{error_verify}</span><br>
    <label>EMAIL (OPTIONAL)</label><br>
    <input type="text" name="email" value="{email}">
    <span class="error">{error_email}</span><br><br>
    <input type="submit">
</form>
"""


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        return self.response.write(*a, **kw)


class Main(Handler):
    def get(self):
        form_keys = {'username': '',
                'error_username': '',
                'password': '',
                'error_password': '',
                'verify': '',
                'error_verify': '',
                'email': '',
                'error_email': ''}
        self.write(header + form_html.format(**form_keys) + footer)


class SignUp(Handler):
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        form_keys = validate_inputs(username, password, verify, email)

        if valid_username(username) and valid_password(password) and password == verify and (valid_email(email) or not email):
            self.redirect('/welcome?name={0}'.format(username))
        else:
            self.write(header + form_html.format(**form_keys) + footer)


class Welcome(Handler):
    def get(self):
        name = self.request.get('name')
        self.write('Welcome ' + name + '!')

app = webapp2.WSGIApplication([
    ('/', Main),
    ('/signup', SignUp),
    ('/welcome', Welcome),
], debug=True)
