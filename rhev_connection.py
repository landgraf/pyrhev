#!/bin/env python
# -*- coding: utf-8 -*-
import httplib,urllib
import base64
import string
import libxml2
import rhev_settings
def get_headers():
    userid = rhev_settings.USERNAME
    passwd = rhev_settings.PASSWORD
    auth = base64.encodestring("%s:%s" % (userid, passwd)).rstrip("\n")
    headers = {"Content-Type": "application/xml",
                     "Accept": "application/xml",
                     "Accept-Charset": "utf-8",
                     "Authorization" : ("Basic %s" % auth)}
    return headers

def get_tag_data(tagname,data):
    tags = rhev_get("/api/tags")
    doc = libxml2.parseDoc(tags)
    ctxt = doc.xpathNewContext()
    res = ctxt.xpathEval("/tags/tag[name[position()=1]= '" + tagname + "']")
    for i in res:
        return i.prop(data)

def get_cluster_data(cluster_name,data):
    clusters = rhev_get("/api/clusters")
    doc = libxml2.parseDoc(clusters)
    ctxt = doc.xpathNewContext()
    res = ctxt.xpathEval("/clusters/cluster[name [position()=1]= '"+ cluster_name + "']")
    for i in res:
        return i.prop(data)

def get_dc_data(dc_name,data):
    clusters = rhev_get("/api/datacenters")
    doc = libxml2.parseDoc(clusters)
    ctxt = doc.xpathNewContext()
    res = ctxt.xpathEval("/data_centers/data_center[name [position()=1]= '"+ dc_name + "']")
    for i in res:
        print i.prop(data)
        return i.prop(data)

def get_all_hosts(cluster):
    nics = []
    hosts = rhev_get("/api/hosts")
    doc = libxml2.parseDoc(hosts)
    ctxt = doc.xpathNewContext()
    res = ctxt.xpathEval("/hosts/host[cluster[@id='" + get_cluster_data(cluster ,"id")  + "']]")
    for i in res:
        #hrefs.append(i.prop("href"))
        nic = rhev_get(i.prop("href")+"/nics")
        nicdoc = libxml2.parseDoc(nic)
        ctxt = nicdoc.xpathNewContext()
        res = ctxt.xpathEval("/host_nics/host_nic[name='eth1']")
        for i in res:
            print i.prop("href")
            nics.append(i.prop("href"))
    return nics

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
    conn.request("POST", url, body = data.encode('utf-8'), headers = get_headers())
    r = conn.getresponse()
    ## DEBUG 
    print r.status, r.reason
    return r.read()
