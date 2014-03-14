#!/usr/bin/python

## tkooda : 2012-10-23 : possibly rebuild some png files before printing HTML that references them

import os
import sys
import time
import subprocess

DIR_IMG = "/var/www/servers/.default/rrd/traffic"
URL_BASE = "/rrd/traffic"
IFACE = "eth0"

# period name and seconds to cache old png ..
PERIODS = [ ( "hour", 30 ),
	( "hours", 30 ),
	( "day", 60 ),
	( "week", 60 ),
	( "month", 300 ),
	( "thismonth", 300 ),
	( "year", 300 ), ]

print """\
HTTP/1.0 200 OK
Content-type: text/html

The Blue graph shows traffic leaving the interface (from the interface's point of view), the Green graph (grows downward) shows traffic entering the interface.<br/>
<br/>
"""

for period_name, period_min in PERIODS:
    fname = "%s-traffic-%s.png" % ( IFACE, period_name )
    fpath = os.path.join( DIR_IMG, fname )
    
    if not os.path.exists( fpath ) or \
            os.stat( fpath )[8] + period_min < time.time():
        subprocess.call( [ "/etc/sv/net-stats/bin/mkgraph-hires-bits",
                           IFACE, period_name ], stdout=open('/dev/null', 'w') )
    
    url = os.path.join( URL_BASE, fname )
    print """<a name="%s">%s</a> :<br/><img src="%s"><br/><br/><br/>""" % ( period_name, period_name, url )
