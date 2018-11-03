salted Caramel - bitterly sweet rsync for sickbeard
===================================================
Salted Caramel joins rsync and sickbeard together to
provide a means to pull shows from a remote locale
via rsync and trigger use sickbeard to process them.

Salted Caramel will build an rsync compatible exclude
list from your sickbeard db including every entry
except those flagged as 'Wanted' so you only dowload
those you 'want',

local.exclude is included to override items manually

general process
===============
read sickbeard.db => rsync exclude list => rsync \
=> trigger sickbeard post-processing \
=> trigger kodi post processing

usage
===============
1.) download and extract saltedcaramel
2.) enter saltedcaramel directory
3.) run saltedcaramel python saltedcaramel.py
    nb: on first run it will copy the conf file to
    your home directory .saltedcaramel
4.) edit the config file to match your system
5.) run saltedcaramel to begin processing

requirements
===============
. sickbeard
. rsync
. python >=2.7

sickbeard setup
===============
Config => Post Processing
 TV Download Dir (unimportant)
 Keep Original Files (optional)
 Move Associated Files => Checked
 Rename Episodes => Checked
 Scan and Process => Unchecked

 nb: the above is only the recommended setup

 If you used Scan and Process with saltedcaramel
 Sickbeard _may_ remove you directories while files
 are being downloaded
