#!/usr/bin/python
# coding=utf-8
"""
Slump
Copyright (C) 2024    Henric Zazzi <henric@zazzi.se>
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.    If not, see <http://www.gnu.org/licenses/>.
"""
#-----------------------------------------------------------------------
from init import *
#-----------------------------------------------------------------------
# Main
#-----------------------------------------------------------------------
try:
    if len(sys.argv) == 1:
        print("create_admin.py <email> <first name> <last name>")
        sys.exit(0)
    conn=sqlite3.connect(DBADDRESS)
    conn.row_factory=sqlite3.Row
    cur=conn.cursor()
    salt,password,hash_password=createPassword()
    cur.execute(INSERTUSER,(sys.argv[1],hash_password,salt,sys.argv[2]+" "+sys.argv[3]))
    last_id=cur.lastrowid
    cur.execute(SETADMINISTRATOR, (last_id,))
    conn.commit()
    conn.close()
    print("Password for %s: %s" % (sys.argv[1],password))

except Exception as e:
    print("Error %s:" % e.args[0])
