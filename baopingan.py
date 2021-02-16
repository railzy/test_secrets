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
        
user = os.environ["USER"]
passwd = os.environ["PASSWORD"]

print(serverchan_key)
