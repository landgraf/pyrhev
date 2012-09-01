#!/bin/env python2
# -*- coding: utf-8 -*-
import rhev_settings
from rhev_connection import *

class Selector(object):
    def _select(self,name,selector):
        number = len(selector)
        if number == 0:
            exit("Instanse not found, exiting")
        if number == 1:
            print "Founded 1 instance %s, using it"%selector[0]["name"]
            return getInstanceData(selector[0]["name"],"id")
        print "%d instance(s) is (are) founded please select"%int(number)
        for i in selector:
            print "%d) %s "%(selector.index(i),i["name"])
        a = input("Please specify:")
        print "Instance %s selected"%selector[a]["name"]
        return selector[a]

class VMSelector(Selector):
    def select(self,name):
        selector = getListOfVMs(name,True)
        result = super(VMSelector,self)._select(name,selector)
        return result["id"]

class NetworkSelector(Selector):
    def select(self,name):
        selector = getListOfVlans(name,True)
        result = super(NetworkSelector,self)._select(name,selector)
        return getNetworkData(result["name"],"id")

class SDSelector(Selector):
    def select(self,name):
        selector = getListOfSDs(name,True)
        result = super(SDSelector,self)._select(name,selector)
        return result["id"]
