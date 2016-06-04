# -*- coding: utf-8 -*-

from bottle_single import get, post, request, route, run, template, response

import random

from time import sleep

login_html = "<p>Your login information was correct. username:{{username}} password:{{password}}</p>"
login_fail =  "<p>Login failed. username:{{username}} password:{{password}}</p>"

int_ran = random.randint(1,1000000000)
seckey = "qazwsxedcdsa" + str(int_ran)

def create_key(str):
    str = str + seckey
    return md5(str)

def md5(str):
    import hashlib
    import types
    if type(str) is types.StringType:
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()
    else:
        return ''

def html_template(file='login.html'):
    file = 'template/%s' % (file)
    f = open(file, 'r')
    html = f.read()
    return html

#@get('/login') # or @route('/login')
@route('/')
@route('/login')
def login():
    return html_template('login.html')

#@post('/login') # or @route('/login', method='POST')
@route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password) == True:
        login_dict = {'username': username, 'password': password}
        if check_login(username, password):
            response.set_cookie("username", username)
            response.set_cookie("account", username, secret=create_key(username))
            #return template(change(), **login_dict) 
            #return template(login_html, **login_dict) 
            html = change()
            return template(change(), **login_dict) 
        else:
            return restricted_area()
    else:
        return restricted_area()

@route('/change')
@route('/restricted')
def restricted_area():
    username = request.get_cookie("username")
    username = request.get_cookie("account", secret=create_key(username))
    if username:
        return template(change(), username=username) 
        #return template("Hello {{name}}. Welcome back.", name=username)
    else:
        return "You are not logged in. Access denied."

def change():
    return html_template('change_passwd.html')

@route('/change', method='POST')
def do_change():
    username = request.get_cookie("username")
    username = request.get_cookie("account", secret=create_key(username))
    newpasswd = request.forms.get('newpasswd')
    if username:
        #return template("Hello {{name}}. Welcome back.", name=username)
        if change_passwd(username, newpasswd) == True:
            response.set_cookie("account", username, secret=int_ran)
            return html_template('thanks_for_your_help.html')
        else:
            return "Please call Allen Wang (ext 5985)"
    else:
        return "You are not logged in. Access denied."

#SYSTEM OPS

def check_login(username, password):
    if username == "root":
        return False

    if password == "Welcome1":
        return True
    else:
        return False

def change_passwd(username, password='Welcome1'):
    from subprocess import Popen, PIPE, check_call
    #check_call(['useradd', 'test'])
    proc=Popen(['passwd', username],stdin=PIPE,stdout=PIPE,stderr=PIPE)
    #proc.stdin.write('Welcome1\n')
    proc.stdin.write(password+'\n')
    sleep(1)
    proc.stdin.write(password)
    proc.stdin.flush()
    stdout,stderr = proc.communicate()
    #print username
    #print password
    print stdout
    print stderr
    return stdout,stderr
    

# TEST AREA
@route('/tmp')
def tmp():
    return html_template('thanks_for_your_help.html')

def main():
    run(host='10.206.102.202', port=5985)

if __name__ == '__main__':
    main()
