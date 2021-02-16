#_*_coding: utf-8 _*_
import datetime
import time
import requests
import json
import re
import os
import execjs
import traceback
import random
# import http.cookiejar as cj



if "SERVERCHAN_KEY" in os.environ:
    serverchan_key = os.environ["SERVERCHAN_KEY"]
    print('exist')
        
user = os.environ["USER"]
passwd = os.environ["PASSWORD"]

print(serverchan_key)
print(user)
print(passwd)

if serverchan_key==NULL:
    print('serverchan_key=null')
if serverchan_key=='':
    print("serverchan_key=''")
