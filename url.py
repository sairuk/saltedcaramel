#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import urllib2

class URLHandler(object):
    def __init__(self):
        self.url="http://localhost:8081"

    def posturl(self, url):
        ''' request it don't force it '''
        req = urllib2.Request(url)
        try:
            resp = urllib2.urlopen(req).getcode()
        except urllib2.URLError as e:
            resp = e.reason
        if resp == 200:
            return "Success"
        else:
            return "[ERROR] response was: %s" % resp
        return