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
# Print text to /var/log/httpd/ssl_error_log
import logging
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
            return(template('login.tpl'))
        access,admin_txt=getAccess(cur,userid)
        views_txt=getMenu(cur,userid)
        menu_txt=template('menu.tpl', admin_menu=admin_txt, views=views_txt,current_view="")
        data=transposeTasks(cur)
        orderidx=groupidx=propertyidx=idx=0
        if request.query.id:
            idx=int(request.query.id)
        if request.query.order:
            orderidx=int(request.query.order)
        if request.query.group:
            groupidx=int(request.query.group)
        if request.query.property:
            propertyidx=int(request.query.property)
        keys = list(data[0].keys())
        sort_keys=[]
        if groupidx>0:
            key=keys[groupidx]
            sort_keys.append(key+SORTORDER if key+SORTORDER in keys else key)
        if orderidx>0:
            key=keys[orderidx]
            sort_keys.append(key+SORTORDER if key+SORTORDER in keys else key)
        data = sorted(data, key=lambda x: tuple(x[key] for key in sort_keys))
        remkeys=[]
        delkeys=[]
        for key in keys:
            (delkeys if key.endswith(SORTORDER) or key == "taskid" else remkeys).append(key)
        for d in data:
            for key in delkeys:
                del d[key]
        orderby=groupby=propertyby=""
        for idx, property in enumerate(remkeys, start=1):
            orderby += LISTOPTIONSELECT % (idx, ' selected' if orderidx == idx else '', property)
            groupby += LISTOPTIONSELECT % (idx, ' selected' if groupidx == idx else '', property)
            propertyby += LISTOPTIONSELECT % (idx, ' selected' if propertyidx == idx else '', property)
        data_txt=showTable(data,groupidx)
        baseurlgroup="index.py?id=%s&order=%s&property=%s&group=" % (idx,orderidx,propertyidx)
        baseurlorder="index.py?id=%s&group=%s&property=%s&order=" % (idx,groupidx,propertyidx)
        baseurlproperty="index.py?id=%s&group=%s&order=%s&property=" % (idx,groupidx,orderidx)
        return(template('list_task.tpl',
            menu=menu_txt,
            groupby=groupby,
            orderby=orderby,
            propertyby=propertyby,
            rows=data_txt,
            baseurlorder=baseurlorder,
            baseurlgroup=baseurlgroup,
            baseurlproperty=baseurlproperty))
        conn.close()
    except Exception as e:
        return("ERROR: %s" % e)
#-----------------------------------------------------------------------
@app.route('/login', method='POST')
def login():
    try:
        conn,cur=openDB()
        session_id=getRandomString(SESSIONN)
        userid=getUser(conn,cur,request.forms.get('email'),request.forms.get('password'),session_id)
        if userid is None:
            return(template('redirect.tpl',link="../index.py",text="Wrong email/password",timeout=2))
        response.set_cookie('session_id',session_id, path='/',httponly=True,secure=True)
        return(template('redirect.tpl',link="../index.py",text="",timeout=0))
    except Exception as e:
        return("ERROR: %s" % e)
#-----------------------------------------------------------------------
@app.route('/logout')
def logout():
    try:
        conn,cur=openDB()
        session_id=getSessionCookie()
        userid=getSessionUser(cur,session_id)
        cur.execute(CLEARSESSION,(userid,))
        conn.commit()
        conn.close()
        response.set_cookie('session_id', '', path='/', expires=0,httponly=True,secure=True)
        return(template('redirect.tpl',link="../index.py",text="",timeout=0))
    except Exception as e:
        return("ERROR: %s" % e)
#-----------------------------------------------------------------------
@app.route('/settings')
def login():
    try:
        conn,cur=openDB()
        session_id=getSessionCookie()
        userid=getSessionUser(cur,session_id)
        if userid is None:
            conn.close()
            return(template('login.tpl'))

        menu_txt=template('menu.tpl', admin_menu=[], views=views_items)
        return(template('settings.tpl', menu=menu_txt,rows=[row['name'] for row in rows]))
    except Exception as e:
        return("ERROR: %s" % e)
#-----------------------------------------------------------------------
# Main
#-----------------------------------------------------------------------
if __name__ == "__main__":
    run(app, debug=True, server='cgi')     
#-----------------------------------------------------------------------
