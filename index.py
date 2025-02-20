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
        projectidx=orderidx=groupidx=viewidx=0
        propertyidx=""
        propertylist=[]
        orderby=groupby=projectby=""
        if request.query.view:
            viewidx=int(request.query.view)
        if request.query.project:
            projectidx=int(request.query.project)
        if request.query.order:
            orderidx=int(request.query.order)
        if request.query.group:
            groupidx=int(request.query.group)
        if request.query.property:
            propertyidx=str(request.query.property)
            propertylist = [int(num) for num in propertyidx.split(",")]
        access,admin_txt=getAccess(cur,userid)
        views_txt=getMenu(cur,userid)
        current_view="index.py/add_view?group=%s&order=%s&property=%s&project=%s" % (groupidx,orderidx,propertyidx,projectidx)
        menu_txt=template('menu.tpl', admin_menu=admin_txt, views=views_txt,current_view=current_view)
        projectby=getProjects(cur,projectidx,userid)
        data=transposeTasks(cur,projectidx)
        keys = list(data[0].keys())
        sort_keys=[]
        if groupidx>0:
            key=keys[groupidx-1]
            sort_keys.append(key+SORTORDER if key+SORTORDER in keys else key)
        if orderidx>0:
            key=keys[orderidx-1]
            sort_keys.append(key+SORTORDER if key+SORTORDER in keys else key)
        data = sorted(data, key = lambda x: tuple((x[key]=='', x[key]) for key in sort_keys))
        curkeys=[]
        for key in keys:
            if key.endswith(SORTORDER):
                continue
            if keys.index(key)+1 not in propertylist and len(propertylist)>0:
                continue
            curkeys.append(key)
        for idx, property in enumerate(keys, start=1):
            if property in curkeys:
                orderby += LISTOPTIONSELECT % (idx, ' selected' if orderidx == idx else '', property)
                groupby += LISTOPTIONSELECT % (idx, ' selected' if groupidx == idx else '', property)
        data_txt=showTable(data,groupidx,curkeys)
        urlproject="index.py?viewid=%s&group=%s&order=%s&property=%s&project=" % (viewidx,groupidx,orderidx,propertyidx)
        urlgroup="index.py?viewid=%s&project=%s&order=%s&property=%s&group=" % (viewidx,projectidx,orderidx,propertyidx)
        urlorder="index.py?viewid=%s&project=%s&group=%s&property=%s&order=" % (viewidx,projectidx,groupidx,propertyidx)
        urlproperty="index.py?viewid=%s&project=%s&group=%s&order=%s&property=" % (viewidx,projectidx,groupidx,orderidx)
        conn.close()
        return(template('list_task.tpl',
            menu=menu_txt,
            projectby=projectby,
            groupby=groupby,
            orderby=orderby,
            rows=data_txt,
            baseurlproject=urlproject,
            baseurlorder=urlorder,
            baseurlgroup=urlgroup,
            baseurlproperty=urlproperty))
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
