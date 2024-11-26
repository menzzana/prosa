#!/usr/bin/python
# coding=utf-8
"""
prosa
Copyright (C) 2024  Henric Zazzi <hzazzi@kth.se>
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
#-----------------------------------------------------------------------
import Cookie
from init import *
from bottle import run, redirect, Bottle, template, response, request, post
#-----------------------------------------------------------------------
app = Bottle()
#-----------------------------------------------------------------------
@app.route('/')
def index():
    try:
        conn,cur=openDB()
        session_id=getSessionCookie()
        userid=getSessionUser(cur,session_id)
        if userid is None:
            conn.close()
            return(template('redirect.tpl',link="../index.py",text="",timeout=0))
        access,admin_txt=getAccess(cur,userid)
        if not any(row['useraccess'] == 1 for row in access):
            conn.close()
            return(template('redirect.tpl',link="../index.py",text="",timeout=0))
        views_txt=getMenu(cur,userid)
        menu_txt=template('menu.tpl', admin_menu=admin_txt, views=views_txt)
        cur.execute(GETUSERS)
        rows=cur.fetchall()
        users=""
        for row in rows:
            users+=LISTOPTION % (row['id'],row['full_name']+" ("+row['email']+")")
        return(template('user_admin.tpl', menu=menu_txt,users=users))
        conn.close()
    except Exception as e:
        return("ERROR: %s" % e)
#-----------------------------------------------------------------------
@app.route('/delete_user', method='POST')
def deleteUser():
    try:
        conn,cur=openDB()
        session_id=getSessionCookie()
        userid=getSessionUser(cur,session_id)
        if userid is None:
            conn.close()
            return(template('redirect.tpl',link="../index.py",text="",timeout=0))
        access,admin_txt=getAccess(cur,userid)
        if not any(row['useraccess'] == 1 for row in access):
            conn.close()
            return(template('redirect.tpl',link="../index.py",text="",timeout=0))
        if not request.forms.get('users'):
            conn.close()
            return(template('redirect.tpl',link="../user_admin.py",text="No user was selected",timeout=2))
        cur.execute("delete from user_access where user_id=?",(request.forms.get('users'),))
        cur.execute("delete from task_view where user_id=?",(request.forms.get('users'),))
        cur.execute("delete from user where id=?",(request.forms.get('users'),))
        conn.commit()
        return(template('redirect.tpl',link="../user_admin.py",text="",timeout=0))
        conn.close()
    except Exception as e:
        return("ERROR: %s" % e)
#-----------------------------------------------------------------------
@app.route('/add_user', method='POST')
def addUser():
    try:
        conn,cur=openDB()
        session_id=getSessionCookie()
        userid=getSessionUser(cur,session_id)
        if userid is None:
            conn.close()
            return(template('redirect.tpl',link="../index.py",text="",timeout=0))
        access,admin_txt=getAccess(cur,userid)
        if not any(row['useraccess'] == 1 for row in access):
            conn.close()
            return(template('redirect.tpl',link="../index.py",text="",timeout=0))
        salt,password,hash_password=createPassword(request.forms.get('password'))
        cur.execute(INSERTUSER,(request.forms.get('email'),hash_password,salt,request.forms.get('full_name')))
        if request.forms.get('administrator')=='on':
            last_id=cur.lastrowid
            cur.execute(SETADMINISTRATOR, (last_id,))
        conn.commit()
        conn.close()
        return(template('redirect.tpl',link="../user_admin.py",text="",timeout=0))
    except Exception as e:
        return("ERROR: %s" % e)
#-----------------------------------------------------------------------
# Main
#-----------------------------------------------------------------------
if __name__ == "__main__":
    run(app, debug=True, server='cgi')     
#-----------------------------------------------------------------------
