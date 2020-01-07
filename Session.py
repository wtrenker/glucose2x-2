from pony.orm import Database, Optional, Required, PrimaryKey, db_session, sql_debug, select, delete
# from pathlib import Path
import json
import pprint
import secrets
from datetime import datetime

db = Database()

class Sessions(db.Entity):
    sessionid = PrimaryKey(str)
    datetime = Required(datetime)
    jsonstr = Optional(str)

db.bind(provider='sqlite', filename='db/SessionsLog.db', create_db=False)
db.generate_mapping(create_tables=False)

def _getdict():
    with db_session:
        jsoninfo = Sessions[sessionID]
    value = jsoninfo.jsonstr
    if value is None or value == '':
        return ''
    value = json.loads(value)
    return value

def getSession(name):
    pydict = _getdict()
    if pydict == '':
        return None
    return pydict.get(name)

def putSession(name, value):
    pydict = _getdict()
    pydict = pydict if pydict is not None and pydict != '' else {}
    pydict.update({name:value})
    jsondict = json.dumps(pydict)
    with db_session:
        sessjson = Sessions[sessionID]
        sessjson.jsonstr = jsondict

def rem(name):
    pass

sessionID = ''
def initSession():
    global sessionID
    sessionID = secrets.token_hex(32)
    with db_session:
        Sessions(sessionid=sessionID, datetime=datetime.now(), jsonstr='{}')

def dumpsessions():
    print('--------- sessions -----------')
    with db_session:
        qry = select((s.sessionid, s.datetime, s.jsonstr) for s in Sessions).order_by(2)
        if qry.count() == 0:
            print('no sessions')
        else:
            for sessline in qry:
                print(sessline)
    print('------- end of sessions --------')

def emptysessions():
    with db_session:
        delete(s for s in Sessions)

if __name__ == '__main__':
    initSession()
    print(sessionID)
    putSession('first', 123)
    print(f'jsonval = {_getdict()}')
    putSession('second', 'abc')
    print(f'second = {getSession("second")}')
    dumpsessions()
    emptysessions()
    dumpsessions()


