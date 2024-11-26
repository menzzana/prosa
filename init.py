#!/usr/bin/python
# coding=utf-8
"""
Prosa
Copyright (C) 2024  Henric Zazzi <henric@zazzi.se>
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
import os
import sys
import sqlite3
import random
import hashlib
from collections import OrderedDict
#-----------------------------------------------------------------------
# Constants
#-----------------------------------------------------------------------
DBADDRESS="prosa.sqlite"
SALTN=5
PASSWORDN=10
SESSIONN=20
# SQL Commands
GETSALT="select salt from user where email=?"
GETIDFROMPASSWORD="select id from user where email=? and password=?"
UPDATESESSION="update user set session_id=?,session_time=datetime('now','start of day','+2 day') where id=?"
CHECKSESSION="select id from user where session_id=? and session_time>datetime('now')"
INSERTUSER="insert into user(email,password,salt,full_name) Values(?,?,?,?)"
INSERTTAG="insert into tag(name) Values(?)"
INSERTPROJECT="insert into project(name,description) Values(?,?)"
INSERTACCESS="insert into user_access(user_id,project_id,access_id) Values(?,?,2)"
INSERTTAGVALUE="insert into tag(tag_id,name) Values(?,?)"
SETADMINISTRATOR="insert into user_access(user_id,access_id) Values(?,1)"
GETVIEWS="select distinct id,user_id,name,global_access from created_views"
GETACCESS="select useraccess,project from get_project_users where user_id=?"
CLEARSESSION="update user set session_id='',session_time=datetime('now') where id=?"
GETTAGVALUES="select distinct tag,tagvalue from all_tags where not tagvalue=''"
GETUSERS="select * from user"
GETTAGS="select * from tag"
GETPROJECTS="select * from project"
# HTML Text
BUTTONLINK="<a href='%s' class='button'>%s</a><br>"
BOLDLINK="<b><a href='index.py?id=%s'>%s</a></b><br>"
LISTOPTION="<option value='%s'>%s</option>"
LISTOPTIONSELECT="<option value=%d%s>%s</option>"
#-----------------------------------------------------------------------
# Functions
#-----------------------------------------------------------------------
def getRandomString(n):
    RANDOMPASSWD="ABCDEFGHJKLMNPQRSTUVXYZabcdefghjkmnpqrstuvxyz23456789"
    s1=""
    random.seed()
    for i in range(0,n):
        s1=s1+RANDOMPASSWD[random.randint(0,len(RANDOMPASSWD)-1)]
    return s1
#-----------------------------------------------------------------------
def createPassword(password=None):
    salt=getRandomString(SALTN)
    if password is None:
        password=getRandomString(PASSWORDN)
    hash_password=encryptText(password+salt)
    return salt,password,hash_password
#-----------------------------------------------------------------------
def encryptText(text):
    return hashlib.md5(text.encode()).hexdigest()
#-----------------------------------------------------------------------
def getSessionCookie():
    if 'HTTP_COOKIE' in os.environ:
        for cookie in os.environ['HTTP_COOKIE'].split(';'):
            (key, value ) = cookie.split('=');
            if key.strip() == "session_id":
                return value
    return None
#-----------------------------------------------------------------------
def getSessionUser(cur,session_id):
    if session_id is not None:
        cur.execute(CHECKSESSION,(session_id,))
        row=cur.fetchone()
        if row is not None:
            return row['id']
    return None
#-----------------------------------------------------------------------
def getUser(conn,cur,email,password,session_id):
    if email is not None and password is not None:
        cur.execute(GETSALT,(email,))
        row=cur.fetchone()
        if row is not None:
            hash_password=encryptText(password+row['salt'])
            cur.execute(GETIDFROMPASSWORD,(email,hash_password))
            row=cur.fetchone()
            if row is not None:
                cur.execute(UPDATESESSION,(session_id,row['id']))
                conn.commit()
                return row['id']
    return None
#-----------------------------------------------------------------------
def openDB():
    conn=sqlite3.connect(DBADDRESS)
    conn.row_factory=sqlite3.Row
    cur=conn.cursor()
    return conn,cur
#-----------------------------------------------------------------------
def transposeTags(rows):
    data = OrderedDict()
    for row in rows:
        if row['tag'] not in data:
            data[row['tag']]=[]
        if row['tagvalue'] not in data[row['tag']]:
            data[row['tag']].append(row['tagvalue'])
    return data
#-----------------------------------------------------------------------
def transposeTasks(rows):
    data = OrderedDict()
    data['taskid']=[]
    data['Project']=[]
    data['Task']=[]
    data['Creation date']=[]
    data['Due date']=[]
    data['User']=[]
    data['Role']=[]
    for row in rows:
        if row['tag'] not in data:
            data[row['tag']]=[]
    for row in rows:
        if row['taskid'] in data['taskid']:
            index = data['taskid'].index(row['taskid'])
        else:
            for key in data:
                data[key].append("")
            index = len(data['taskid']) - 1
            data['taskid'][index]=row['taskid']
            data['Project'][index]=row['project']
            data['Task'][index]=row['task']
            data['Creation date'][index]=row['creation_date']
            data['Due date'][index]=row['due_date']
        data[row['tag']][index] = row['tagvalue']
    return data
#-----------------------------------------------------------------------
def showTable(data):
    data_txt="<table><tr>"
    for header in data.keys():
        data_txt+="<td><b>"+header+"</b></td>"
    data_txt+="</tr>"
    max_len = max(len(values) for values in data.values())
    for i in range(max_len):
        data_txt+="<tr>"
        for tag in data:
            data_txt+="<td>"
            if i < len(data[tag]):
                data_txt+=str(data[tag][i])
            data_txt+="</td>"
        data_txt+="</tr>"
    data_txt+="</table>"
    return data_txt
#-----------------------------------------------------------------------
def getAccess(cur,userid):
    cur.execute(GETACCESS, (userid,))
    rows=cur.fetchall()
    admin_txt=""
    if any(row['useraccess'] == 1 for row in rows):
        admin_txt+=BUTTONLINK % ('tags.py','Tags')
        admin_txt+=BUTTONLINK % ('user_admin.py','User')        
    return rows,admin_txt
#-----------------------------------------------------------------------
def getMenu(cur,userid):
    cur.execute(GETVIEWS)
    rows=cur.fetchall()
    views_txt=""
    for row in rows:
        if row['global_access']==1 or row['user_id']==userid:
            views_txt+=BOLDLINK % (row['id'],row['name'])
    return views_txt
#-----------------------------------------------------------------------
