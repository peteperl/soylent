#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/flaskserver/")

from ComputeApi import app as application
application.secret_key = '3959Asjfoi3oDSE'
