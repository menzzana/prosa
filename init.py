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
# Needed for debugging
import logging

#-----------------------------------------------------------------------
# Constants
#-----------------------------------------------------------------------
DBADDRESS="prosa.sqlite"
SALTN=5
PASSWORDN=10
SESSIONN=20
SORTORDER="_n"
# SQL Commands
GETSALT="select salt from user where email=?"
GETIDFROMPASSWORD="select id from user where email=? and password=?"
UPDATESESSION="update user set session_id=?,session_time=datetime('now','start of day','+2 day') where id=?"
CHECKSESSION="select id from user where session_id=? and session_time>datetime('now')"
INSERTUSER="insert into user(email,password,salt,full_name) Values(?,?,?,?)"
INSERTTAG="insert into property(name) Values(?)"
INSERTPROJECT="insert into project(name,description) Values(?,?)"
INSERTACCESS="insert into user_access(user_id,project_id,access_id) Values(?,?,2)"
INSERTTAGVALUE="insert into property(property_id,name) Values(?,?)"
SETADMINISTRATOR="insert into user_access(user_id,access_id) Values(?,1)"
GETVIEWS="select distinct id,user_id,name,global_access from created_views"
GETACCESS="select useraccess,project from get_project_users where user_id=?"
CLEARSESSION="update user set session_id='',session_time=datetime('now') where id=?"
GETTAGVALUES="select distinct property,property_value from all_properties where not property_value=''"
GETUSERS="select * from user"
GETTAGS="select * from property"
GETPROJECTS="select * from project"
GETTASKS="select * from all_tasks"
GETPROPERTIES="select * from property"
# HTML Text
BUTTONLINK="<a href='%s' class='button'>%s</a><br>"
BOLDLINK="<b><a href='index.py?id=%s'>%s</a></b><br>"
LISTOPTION="<option value='%s'>%s</option>"
LISTOPTIONSELECT="<option value=%d%s>%s</option>"
TABLECELLWIDTH="120"
TABLEHEADER="<td style='width: "+TABLECELLWIDTH+"px'><b>%s <a href='test.html' class='button button-small'>-</a><br></b></td>"
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
def transposeTags(cur):
    cur.execute(GETTAGVALUES)
    rows = cur.fetchall()
    dict1=OrderedDict()
    data=[]
    for row in rows:
        dict1[row['property']] = ''
    for row in rows:
        found=False
        for d1 in data:
            if d1[row['property']]=='':
                d1[row['property']]=row['property_value']
                found=True
                break
        if not found:
            dict2=OrderedDict(dict1)
            dict2[row['property']]=row['property_value']
            data.append(dict2)
    return data
#-----------------------------------------------------------------------
def transposeTasks(cur):
    propcols=[]
    cur.execute(GETPROPERTIES)
    rows=cur.fetchall()
    for row in rows:
        propcols.append(row['name'])
    cur.execute(GETTASKS)
    rows=cur.fetchall()
    taskcols=[]
    for row in cur.description:
        if row[0] not in ('property', 'property_value', 'property_value'+SORTORDER):
            taskcols.append(row[0])
    colnames=taskcols+propcols+[item + SORTORDER for item in propcols]
    data = []
    #logging.basicConfig(level=logging.INFO)
    #logging.info(colnames)
    for row in rows:
        index = next((i for i, entry in enumerate(data) if entry['taskid'] == row['taskid']), None)
        if index is None:
            index = len(data) 
            data.append(OrderedDict.fromkeys(colnames, ""))
            for col in taskcols:
                data[index][col]=row[col]
        if row['property_value']:
            data[index][row['property']] = row['property_value']
            data[index][row['property']+SORTORDER] = row['property_value'+SORTORDER]
    return data
#-----------------------------------------------------------------------
def showTable(data,groupidx):
    keys=list(data[0].keys())
    data_txt=""
    last_txt=None
    header_txt="<table><tr>"
    for header in keys:
        if groupidx==0 or keys[groupidx-1]!=header:
            header_txt+=TABLEHEADER % (header,)
    header_txt+="</tr>"
    for r in data:
        if groupidx==0 and data_txt=="":
            data_txt+=header_txt
        if groupidx>0:
            if r[keys[groupidx-1]]!=last_txt:
                if data_txt!="":
                    data_txt+="<table>"
                data_txt+="<br><b>"+keys[groupidx-1]+": </b>"+r[keys[groupidx-1]]+"<br>"+header_txt
            last_txt=r[keys[groupidx-1]]
        data_txt+="<tr>"
        for idx,c in enumerate(r.values(),start=1):
            if groupidx==0 or groupidx!=idx:
                data_txt+="<td>"+str(c)+"</td>"
        data_txt+="</tr>"
    data_txt+="</table>"
    return data_txt
#-----------------------------------------------------------------------
def getAccess(cur,userid):
    cur.execute(GETACCESS, (userid,))
    rows=cur.fetchall()
    admin_txt=""
    if any(row['useraccess'] == 1 for row in rows):
        admin_txt+=BUTTONLINK % ('properties.py','Tags')
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
