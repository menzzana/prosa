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
        cur.execute(GETTAGVALUES)
        rows=cur.fetchall()
        data=transposeTags(rows)
        data_txt=showTable(data)
        cur.execute(GETTAGS)
        rows=cur.fetchall()
        tags=""
        for row in rows:
            tags+=LISTOPTION % (row['id'],row['name'])
        conn.close()
        return(template('tags.tpl', menu=menu_txt,rows=data_txt,tags=tags))
    except Exception as e:
        return("ERROR: %s" % e)
#-----------------------------------------------------------------------
@app.route('/add_tag', method='POST')
def addTag():
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
        cur.execute(INSERTTAG,(request.forms.get('tag')))
        conn.commit()
        conn.close()
        return(template('redirect.tpl',link="../tags.py",text="",timeout=0))
    except Exception as e:
        return("ERROR: %s" % e)
#-----------------------------------------------------------------------
@app.route('/add_value', method='POST')
def addTagValue():
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
        if not request.forms.get('tags'):
            conn.close()
            return(template('redirect.tpl',link="../tags.py",text="No tag was selected",timeout=2))
        cur.execute(INSERTTAGVALUE,(request.forms.get('tags'),request.forms.get('tagvalue')))
        conn.commit()
        return(template('redirect.tpl',link="../tags.py",text="",timeout=0))
        conn.close()
    except Exception as e:
        return("ERROR: %s" % e)
#-----------------------------------------------------------------------
# Main
#-----------------------------------------------------------------------
if __name__ == "__main__":
    run(app, debug=True, server='cgi')     
#-----------------------------------------------------------------------
