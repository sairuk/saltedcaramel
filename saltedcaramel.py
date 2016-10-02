#!/usr/bin/env python
#-*- encoding: utf-8 -*-
###########################################################
# Salted Caramel (sairuk)
###########################################################
# sickbeard, rsync exclude script
#
# v02 complete rewrite after death of r01
# v01 wizardry
#
# 2DO
# add kodi user/pass support
#
import os
import shutil
import ConfigParser
from subprocess import Popen
from db import SQLHandler
from rsync import RsyncHandler
from url import URLHandler

appname = 'Salted Caramel'
appsht = 'saltedcaramel'
appver = "0.0.2"


def wrtlog(s):
    print s
    return

def wrtEmpty(f):
    e = open(f, 'w')
    e.close()
    return

def main():
    conf_dir = os.path.join(os.path.expanduser('~'), '.%s' % appsht)
    conf_filename = '%s.conf-example' % appsht
    conf_file = os.path.join(conf_dir, '%s.conf' % appsht)

    #### config
    if os.path.exists(conf_file):
        config = ConfigParser.ConfigParser()
        config.read(conf_file)

        ### sickbeard settings
        sb_ip = config.get('sickbeard', 'sb_ip')
        sb_port = config.get('sickbeard', 'sb_port')
        sb_path = config.get('sickbeard', 'sb_path')
        sb_dbloc = config.get('sickbeard', 'sb_dbloc')

        ### kodi settings
        kodi_ip = config.get('kodi', 'kodi_ip')
        kodi_port = config.get('kodi', 'kodi_port')
        kodi_user = config.get('kodi', 'kodi_user')
        kodi_pass = config.get('kodi', 'kodi_pass')

        ### rsync settings
        rs_exclude_file = os.path.join(conf_dir, config.get('rsync', 'rs_exclude_file'))
        rs_local_exclude_file = os.path.join(conf_dir, config.get('rsync', 'rs_local_exclude_file'))
        rs_source = config.get('rsync', 'rs_source')
        rs_dest = config.get('rsync', 'rs_dest')
        rs_params = config.get('rsync', 'rs_params')

        ### general
        debug = config.getboolean('general', 'debug')
        dryrun = config.getboolean('general', 'dryrun')

    else:
        wrtlog("Starting %s (v%s) run" % (appname, appver))
        wrtlog("[CRITICAL] %s file missing, first run?" % conf_file)

        ### first run
        wrtlog("[FIRSTRUN] Creating %s" % conf_dir)
        if not os.path.exists(conf_dir):
            os.mkdir(conf_dir)
        wrtlog("[FIRSTRUN] Copying %s to %s" % (conf_filename, conf_file))
        if os.path.exists(conf_dir):
            ### conf file
            shutil.copy(os.path.join('dist', conf_filename), conf_file)
            wrtlog("[FIRSTRUN] Creating required files %s" % conf_file)

            ### defauls
            wrtEmpty(os.path.join(conf_dir, 'sickbeard.exclude'))
            wrtEmpty(os.path.join(conf_dir, 'local.exclude'))
        else:
            wrtlog("[FIRSTRUN] We had a problem, trying copying files from dist manually")

        wrtlog("[FIRSTRUN] Default setup complete time to edit %s" % conf_file)
        exit()

    ## be kind baby
    if debug: wrtlog("Starting %s (v%s) run" % (appname, appver))

    ## initiate handlers
    if debug: wrtlog("Initiate handler SQL")
    db = SQLHandler(sb_dbloc)
    if debug: wrtlog("Initiate handler RSYNC")
    rsync = RsyncHandler()
    if debug: wrtlog("Initiate handler URL")
    url = URLHandler()

    ## read db
    #<showid>.S<season>E<episode>.<name>.*
    if debug: wrtlog("Extract episode information from SickBeard")
    #SELECT tv_shows.show_name, tv_episodes.season, tv_episodes.episode, tv_episodes.name FROM tv_episodes INNER JOIN tv_shows ON tv_episodes.showid = tv_shows.tvdb_id WHERE tv_episodes.status != 3
    result = db.execSQL("SELECT tv_shows.show_name, tv_episodes.season, tv_episodes.episode, tv_episodes.name FROM tv_episodes INNER JOIN tv_shows ON tv_episodes.showid = tv_shows.tvdb_id WHERE tv_episodes.status != 3", db.cursor())

    ## convert strings for rsync
    if debug: wrtlog("Convert results string to rsync case-insentive compatible strings")
    rsync_set = []
    for row in result:
        rsync_set.append(rsync.buildExcludeString(row))
    ## write exclude file
    if debug: wrtlog("Write rsync exclude file")
    rsync.writeExcludeFile(rsync_set, rs_exclude_file)

    ## if is dryrun we want to dry-run rsync
    if debug: wrtlog("This is a dryrun: %s" % dryrun)
    if dryrun:
        rsync.params = "--dry-run " + rs_params
        if debug: wrtlog("Amended runtime params: %s" % rs_params)

    ## build rsync exec string
    if debug: wrtlog("Build rsync exec string")
    rsync_exec = "%s %s %s %s %s %s %s %s" % \
                 (
                     rsync.cmd,
                     rs_params,
                     rsync.exclude,
                     rs_exclude_file,
                     rsync.exclude,
                     rs_local_exclude_file,
                     rs_source,
                     rs_dest,
                 )

    if debug: wrtlog("Built rsync exec string as: %s" % rsync_exec)

    ## execute rsync
    if debug: wrtlog("Executing rsync with: %s" % rsync_exec)
    p = Popen([rsync_exec], shell=True)
    p.communicate()

    ## update sickbeard
    if debug: wrtlog("Asking SickBeard to update")
    sb = url.posturl('http://%s:%s//home/postprocess/processEpisode/?dir=%s' % (sb_ip, sb_port, sb_path))
    if debug: wrtlog(sb)

    ## update kodi
    if debug: wrtlog("Asking Kodi to update")
    ko = url.posturl('http://%s:%s/jsonrpc?request=\{"jsonrpc":"2.0","method":"VideoLibrary.Scan"\}' % (kodi_ip, kodi_port))
    if debug: wrtlog(ko)

    return


if __name__ == "__main__":
    main()