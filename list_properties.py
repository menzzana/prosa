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
        projectidx=orderidx=groupidx=viewidx=0
        propertyidx=""
        propertylist=[]
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
        data=transposeTasks(cur,0)
        keys = list(data[0].keys())
        props=""
        for idx,property in enumerate(keys, start=1):
            if not property.endswith(SORTORDER):
                props += LISTOPTIONSELECT % (idx, ' selected' if idx in propertylist or len(propertylist)==0 else '', property)
        #urlproperty="?viewid=%s&group=%s&order=%s&property=%s&project=" % (viewidx,groupidx,orderidx,propertyidx)
        return template('list_properties.tpl', properties=props) #,urlproperty=urlproperty)
    except Exception as e:
        return("ERROR: %s" % e)
#-----------------------------------------------------------------------
# Main
#-----------------------------------------------------------------------
if __name__ == "__main__":
    run(app, debug=True, server='cgi')     
#-----------------------------------------------------------------------
