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
        views_txt=getMenu(cur,userid)
        menu_txt=template('menu.tpl', admin_menu=admin_txt, current_view="", views=views_txt)
        cur.execute(GETPROJECTS)
        rows=cur.fetchall()
        projects=""
        for row in rows:
            projects+=LISTOPTION % (row['id'],row['name'])
        conn.close()
        return(template('projects.tpl', menu=menu_txt,projects=projects))
    except Exception as e:
        return("ERROR: %s" % e)
#-----------------------------------------------------------------------
@app.route('/add_project', method='POST')
def addTag():
    try:
        conn,cur=openDB()
        session_id=getSessionCookie()
        userid=getSessionUser(cur,session_id)
        if userid is None:
            conn.close()
            return(template('redirect.tpl',link="../index.py",text="",timeout=0))
        access,admin_txt=getAccess(cur,userid)
        cur.execute(INSERTPROJECT,(request.forms.get('project'),request.forms.get('description')))
        last_id=cur.lastrowid
        cur.execute(INSERTACCESS,(userid,last_id))
        conn.commit()
        conn.close()
        return(template('redirect.tpl',link="../projects.py",text="",timeout=0))
    except Exception as e:
        return("ERROR: %s" % e)
#-----------------------------------------------------------------------
# Main
#-----------------------------------------------------------------------
if __name__ == "__main__":
    run(app, debug=True, server='cgi')     
#-----------------------------------------------------------------------
