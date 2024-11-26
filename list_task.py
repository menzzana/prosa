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
from bottle import run, Bottle, template, response, request, post
# Print text to /var/log/httpd/ssl_error_log
import logging
#-----------------------------------------------------------------------
# Constants
#-----------------------------------------------------------------------
PRINTPROJECT="select * from task"
#-----------------------------------------------------------------------
# Main
#-----------------------------------------------------------------------
app = Bottle()
#-----------------------------------------------------------------------
@app.route('/', method='POST')
def handle_form():
    try:
        reload(sys)
        sys.setdefaultencoding('utf8')
        conn=sqlite3.connect(DBADDRESS)
        conn.row_factory=sqlite3.Row
        cur=conn.cursor()
        session_id=getRandomString(SESSIONN)
        
        # Print to the log
        logging.basicConfig(level=logging.INFO)
        logging.info(request.forms.get('email'))
        logging.info(request.forms.get('password'))  
        #logging.info("Request Content-Type: {}".format(request.headers.get('Content-Type')))

        email=getUser(conn,cur,request.forms.get('email'),request.forms.get('password'),session_id)
        if email is None:
            session_id=getSessionCookie()
            email=getSessionUser(cur,session_id)
        else:
            response.set_cookie('session_id',session_id, path='/')
        #response.content_type = 'text/html; charset=UTF-8' 
        #print(response)
        if email is None:
            return(template('redirect.tpl',link="index.py",text="Wrong email/password"))
        cur.execute(PRINTPROJECT)
        rows=cur.fetchall()
        conn.close()
        return(template('list_task.tpl', rows=[row['name'] for row in rows]))
    except Exception as e:
        return("ERROR: %s" % e)
#-----------------------------------------------------------------------
if __name__ == "__main__":
    run(app, server='cgi')     
#-----------------------------------------------------------------------
