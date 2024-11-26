# Prosa
## Project Organiser for Suppport Activities

This is a simple project manager website that
can be used for tracking projects, and their todos

## Functionality

| Role | Tags | Projects | Own Project | Own Project access | Views |
| --- | --- | --- | --- | --- | --- |
| Administrator | rw | rw | rw | rw | rw |
| Project Leader | r | r | rw | rw | rw |
| Project Advisor | r | r | r | r | rw |
| Project Owner | r | r | r | r | rw |
| Developer | r | r | rw | r | rw |
| viewer | r | r | r | r | rw |

* Milestones
* Tasks
* Project Priority
* deadlines
* Sorted lists by ...
  * Various parameters
  * Sorted
  * Flexible list output

## Dependencies

The code has a couple of dependencies.

### bottle

Bottle is a python light weight web framework which is only dependent on one file, 
does not need to be installed and can be downloaded from https://pypi.org/project/bottle/#files

More information about bottle can be found at https://bottlepy.org/docs/dev/

### SQLite

SQLite is a C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine.
More information at https://www.sqlite.org/index.html

### Apache

The Apache HTTP Server with **cgi-bin** More information with https://httpd.apache.org/

## Installation

Goto to your the cgi-bin folder of your apache installation

````
git clone https://github.com/menzzana/prosa
wget <bottle source>
tar xvfp <bottle source>.tar.gz
ln -s <bottle source>/bottle.py bottle.py
sqlite3 prosa.sqlite < db.sql
````

New administrator can be added by using script **create_admin.py**
````
create_admin.py <username> <first name> <last name>
````

# License

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
