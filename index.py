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
        menu_txt=template('menu.tpl', admin_menu=admin_txt, views=views_txt)
        tags=['None','Project','Creation date','Due date']
        tagssql=['','project','creation_date','due_date']
        cur.execute(GETTAGS)
        rows=cur.fetchall()
        for row in rows:
            tags.append(row['name'])
            tagssql.append(row['name'])
        orderix=groupidx=idx=0
        if request.query.id:
            idx=request.query.id
        if request.query.order:
            orderidx=request.query.order
        if request.query.group:
            groupidx=request.query.group
        orderby=groupby=""
        for idx, tag in enumerate(tags):
            orderby += LISTOPTIONSELECT % (idx, ' selected' if int(orderidx) == idx else '', tag)
            groupby += LISTOPTIONSELECT % (idx, ' selected' if int(groupidx) == idx else '', tag)
        tasksql="select * from all_tasks,get_project_users where get_project_users.project=all_tasks.project"
        if orderidx>0:
            tasksql+=" order by  %s" % (tagssql[int(groupidx)],) 
        if orderidx>0:
            if "order" in tasksql:
                tasksql+=",%s" % (tagssql[int(orderidx)],)  
            else:
                tasksql+=" order by  %s" % (tagssql[int(orderidx)],) 
        cur.execute(tasksql)
        rows=cur.fetchall()
        cur.execute("select * from created_views where id=?", (request.query.id,))
        row_views=cur.fetchall()
        data=transposeTasks(rows)
        del data['taskid']

        data_txt=showTable(data)


        baseurlgroup="index.py?id=%s&order=%s&group=" % (idx,orderidx)
        baseurlorder="index.py?id=%s&group=%s&order=" % (idx,groupidx)
        return(template('list_task.tpl', menu=menu_txt,groupby=groupby,orderby=orderby,rows=data_txt,baseurlorder=baseurlorder,baseurlgroup=baseurlgroup))
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
