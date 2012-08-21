
import httplib
import base64
import string
import rhev_settings
def get_headers():
    userid = rhev_settings.USERNAME
    passwd = rhev_settings.PASSWORD
    auth = base64.encodestring("%s:%s" % (userid, passwd))
    headers = {"Content-type": "application/xml",
                     "Accept": "application/xml",
                     "Authorization" : "Basic %s" % auth}
    return headers

def rhev_connect():
    rhev = rhev_settings.HOST_PORT
    conn = httplib.HTTPSConnection(rhev)
    return conn

def rhev_get(url):
    conn = rhev_connect()
    conn.request("GET",url,None,get_headers())
    r = conn.getresponse()
    return r.read()

def rhev_post(url,data):
    conn = rhev_connect()
    print url
    print data
    conn.request('POST', url, data, get_headers())
    r = conn.getresponse()
    return r.read()
    #return "Fuck"
