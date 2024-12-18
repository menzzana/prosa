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
        menu_txt=template('menu.tpl', admin_menu=admin_txt, current_view="", views=views_txt)
        data=transposeTags(cur)
        data_txt=showTable(data,0)
        cur.execute(GETTAGS)
        rows=cur.fetchall()
        props=""
        for row in rows:
            props+=LISTOPTION % (row['id'],row['name'])
        conn.close()
        return(template('properties.tpl', menu=menu_txt,rows=data_txt,props=props))
    except Exception as e:
        return("ERROR: %s" % e)
#-----------------------------------------------------------------------
@app.route('/add_property', method='POST')
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
        cur.execute(INSERTTAG,(request.forms.get('property')))
        conn.commit()
        conn.close()
        return(template('redirect.tpl',link="../properties.py",text="",timeout=0))
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
        if not request.forms.get('props'):
            conn.close()
            return(template('redirect.tpl',link="../properties.py",text="No property was selected",timeout=2))
        cur.execute(INSERTTAGVALUE,(request.forms.get('props'),request.forms.get('property_value')))
        conn.commit()
        return(template('redirect.tpl',link="../properties.py",text="",timeout=0))
        conn.close()
    except Exception as e:
        return("ERROR: %s" % e)
#-----------------------------------------------------------------------
# Main
#-----------------------------------------------------------------------
if __name__ == "__main__":
    run(app, debug=True, server='cgi')     
#-----------------------------------------------------------------------
