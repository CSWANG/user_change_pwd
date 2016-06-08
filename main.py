# -*- coding: utf-8 -*-

from bottle_single import get, post, request, route, run, template, response

import random

from time import sleep

seckey = "qazwsxedcdsa" + str(random.randint(1, 1000000000))

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

@route('/')
@route('/login')
def login():
    return html_template('login.html')

@route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        login_dict = {'username': username, 'password': password}
        if check_login(username, password):
            response.set_cookie("username", username)
            response.set_cookie("account", username, secret=create_key(username))
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
    else:
        return "You are not logged in. Access denied."

def change():
    return html_template('change_passwd.html')

@route('/change', method='POST')
def do_change():
    username = request.get_cookie("username")
    username = request.get_cookie("account", secret=create_key(username))
    newpasswd = request.forms.get('newpasswd')
    a_newpasswd = request.forms.get('a_newpasswd')
    if newpasswd == a_newpasswd:
        if username:
            if change_passwd(username, newpasswd) == True:
                response.set_cookie("account", username, secret=random.randint(1, 1000000000))
                return html_template('thanks_for_your_help.html')
            else:
                return "Please call Allen Wang (ext 5985)"
        else:
            return "You are not logged in. Access denied."
    else:
        return template(change(), username=request.get_cookie("username"))

def check_login(user, password):
    import crypt
    import spwd
    try:
        enc_pwd = spwd.getspnam(user)[1]
        if enc_pwd in ["NP", "!", "", None]:
            return False
        if enc_pwd in ["LK", "*"]:
            return False
        if enc_pwd == "!!":
            return False
        if crypt.crypt(password, enc_pwd) == enc_pwd:
            return True
        else:
            return False
    except KeyError:
        return False
    return False

def change_passwd(username, password='Welcome1'):
    import subprocess
    p = subprocess.Popen(["chpasswd"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = p.communicate("%s:%s" % (username, password))
    if p.returncode is not 0:
        return False
    return True

def main():
    run(host='0.0.0.0', port=5985)

if __name__ == '__main__':
    main()
