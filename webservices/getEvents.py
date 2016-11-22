import sys
sys.path.append('/root/2AU_python_script/dao')
from dao import dao
import json

class GetEvents:
    def GET(self):
        try:
            db = dao('10.157.15.161', '2AU', 'password', '2AU')
            cursor = db.getDao()
            cursor.execute("SELECT * FROM evenement")
            query_result = [ dict(line) for line in [zip([ column[0] for column in cursor.description], row) for row in cursor.fetchall()] ]
            print query_result
        except Exception, e:
            print "Error [%r]" % (e)
            sys.exit(1)

#getevent = GetEvents()
#print getevent.GET()
