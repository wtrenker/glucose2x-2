from pony.orm import Database, Optional, Required, PrimaryKey, db_session, sql_debug, select, delete
from datetime import datetime
import Session

db = Database()

class Log(db.Entity):
    sessionid = PrimaryKey(str)
    datetime = Required(datetime)
    location = Optional(str)
    entry = Optional(str)

db.bind(provider='sqlite', filename='db/SessionsLog.db', create_db=False)
db.generate_mapping(create_tables=False)

# def initLog():
#
#     with db_session:
#         objsess = SessionInfo['log']
#         objsess.value = json.dumps([])

def putLog(location, line):
    with db_session:
        Log(sessionid=Session.sessionID, datetime=datetime.now(), location=location, entry=line)
log = putLog

def dumplog():
    print('--------- db log -----------')
    with db_session:
        qry = select((l.sessionid, l.datetime, l.location, l.entry) for l in Log).order_by(2)
        if qry.count() == 0:
            print('empty log')
        else:
            for logline in qry:
                print(logline)
    print('------- end of db log --------')

def emptylog():
    with db_session:
        delete(l for l in Log)


if __name__ == '__main__':
    Session.initSession()
    log('1234', 'try this')
    dumplog()
    emptylog()
    dumplog()


