#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import sqlite3

class SQLHandler(object):
    def __init__(self, sb_loc):
        self.user = ''
        self.password = ''
        if os.path.exists(sb_loc):
            self.dbname = sb_loc
        else:
            self.dbname = None
            print "[ERROR] Cannot open %s" % sb_loc

    def cursor(self):
        conn = sqlite3.connect(self.dbname)
        return conn.cursor()

    def execSQL(self, sql, c):
        return c.execute(sql)