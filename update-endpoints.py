#!/usr/bin/python

__author__      = 'Matt Fischer <matt.fischer@twcable.com>'
__copyright__   = 'Copyright 2013, Matt Fischer'

"""
Update the endpoints in a keystone db using mysql
"""

import MySQLdb
import argparse
import urlparse
import sys

# a12ab673016d40da

def main(dbhost, username, password, new_endpoint, endpoint_type):
    db = MySQLdb.connect(host=dbhost, user=username, passwd=password,
            db="keystone")
    cur = db.cursor()
    cur.execute("select id, url from endpoint where interface='%s'" % endpoint_type)
    for row in cur.fetchall():
        url = str(row[1])
        endpoint_id = str(row[0])
        try:
            u = urlparse.urlparse(url)
            print "Changing %s to %s in URL %s" % (u.hostname,new_endpoint, url)
            urlstring = "%s://%s:%s%s" % (u.scheme, new_endpoint, u.port,
                u.path)
            cur.execute("""UPDATE endpoint
                            SET url=%s
                            WHERE id=%s
                            """, (urlstring, endpoint_id))
        except Exception as e:
            print "Could not parse URL, giving up: %s (%s)" % (url, e)
            cur.close()
            db.close()
            sys.exit(1)
    db.commit()
    cur.close()
    db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", help="database username", required=True)
    parser.add_argument("--password", help="database password", required=True)
    parser.add_argument("--host", help="database host", required=True)
    parser.add_argument("--endpoint", help="endpoint to move the public endpoints to", required=True)
    parser.add_argument("--endpoint-type", help="which type of endpoint to modify", required=True, choices=['public','internal','admin'])
    args = parser.parse_args()
    main(args.host, args.username, args.password, args.endpoint, args.endpoint_type)
