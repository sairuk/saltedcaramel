#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#  2DO
#  convert buildExcludeString to more robust system
#  ?regex?
#

import os

# this is a hack to get around unicode errors when writing
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#defaults
exclude = "exclude.list"

class RsyncHandler(object):
    def __init__(self):
        self.cmd = '/usr/bin/rsync'
        self.exclude = "--exclude-from"
        self.fn_blacklist = ['.','/',":","(",")","`","'","",'"',",","’","?",'“','”']
        self.fn_whitelist = ["0","1","2","3","4","5","6","7","8","9"," ",'-']

    def encodeChar(self, c, enc="utf-8"):
        return c.encode(enc)

    def decodeChar(self, c, enc="utf-8"):
        return c.decode(enc)

    def buildSeperator(self,s, sep="."):
        return s.replace(' ',sep)

    def buildCharString(self,s):
        charlist = []
        for c in s:
            if c in self.fn_blacklist:
                pass
            elif c in self.fn_whitelist:
                charlist.append(c)
            else:
                charlist.append("[%s%s]" % (self.encodeChar(c.upper()), self.encodeChar(c.lower())))
        return "".join(charlist)

    def buildIntPad(self,c):
        return '%02d' % c

    def buildExcludeString(self,t):
        ''' return a compatible exclude string for rsync --exclude-from'''
        esList = []
        #0 chars
        for c in t[0]:
            esList.append(self.buildCharString(c))
        c = None
        #1 paddednum
        esList.append(".%s%s" % ( self.buildCharString("S"), self.buildIntPad(t[1])))
        #2 paddednum
        esList.append("%s%s." % ( self.buildCharString("E"), self.buildIntPad(t[2])))
        #3 chars
        for c in t[3]:
            esList.append(self.buildCharString(c))
        c = None

        return "%s*" % self.buildSeperator("".join(esList))


    def writeExcludeFile(self, l, exclude=exclude):
        ''' write the exclude file form '''
        with open(exclude, 'w') as f:
            for line in l:
                f.write("%s\n" % line)
        return