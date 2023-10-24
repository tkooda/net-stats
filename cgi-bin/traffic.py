#!/usr/bin/python3

## tkooda : 2012-10-23 : possibly rebuild some png files before printing HTML that references them

import os
import sys
import time
import subprocess

DIR_IMG = "/var/www/html/rrd/image/"
URL_BASE = "/rrd/image"

# period name and seconds to cache old png ..
PERIODS = [
	( "hour", 30 ),
	( "hours", 300 ),
	( "day", 3600 ),
	( "week", 300 ),
	( "month", 3600 * 4 ),
	( "thismonth", 3600 * 4 ),
	( "year", 86400 ),
	]


def get_default_iface_name_linux():
	route = "/proc/net/route"
	with open(route) as f:
		for line in f.readlines():
			try:
				iface, dest, _, flags, _, _, _, _, _, _, _, =  line.strip().split()
				if dest != '00000000' or not int(flags, 16) & 2:
					continue
				return iface
			except:
				continue


iface = get_default_iface_name_linux()

print( """\
HTTP/1.0 200 OK
Content-type: text/html

<html>
<body>
The Blue graph shows traffic leaving the interface (from the interface's point of view), the Green graph (grows downward) shows traffic entering the {} interface.<br/>
<br/>
""".format( iface )  )

for period_name, period_min in PERIODS:
    fname = "%s-traffic-%s.png" % ( iface, period_name )
    fpath = os.path.join( DIR_IMG, fname )
    
    if not os.path.exists( fpath ) or \
            os.stat( fpath )[8] + period_min < time.time():
        subprocess.call( [ "/etc/sv/traffic-stats/bin/make-graphs",
                           iface, period_name ], stdout=open('/dev/null', 'w') )
    
    url = os.path.join( URL_BASE, fname )
    print( """<a name="%s">%s</a> :<br/><img src="%s"><br/><br/><br/>""" % ( period_name, period_name, url ) )

print( """\n</body>\n</html>\n""" )

