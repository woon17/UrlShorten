import tzlocal
import pytz
import os

DOMAIN2="http://localhost:8000/"

def getLocalCreateAt(createAt):
    local_timezone = tzlocal.get_localzone()
    return createAt.replace(tzinfo=pytz.utc).astimezone(local_timezone)

def getDomains():
    if os.environ['LOCAL_HOST'] == 'True':
        DOMAIN1="http://127.0.0.1:8000/"
        return [DOMAIN1, DOMAIN2]
    else:
        DOMAIN1="https://myshortenurlapp.herokuapp.com/"
        return [DOMAIN1]

def getHomeDomain():
    if os.environ['LOCAL_HOST'] == 'True':
        return "http://localhost:8000/"
    else:
        DOMAIN1="https://myshortenurlapp.herokuapp.com/"
        return DOMAIN1
