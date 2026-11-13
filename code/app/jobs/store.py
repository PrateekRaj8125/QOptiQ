import sqlite3,json,os
from datetime import datetime,timezone
class JobStore:
    def __init__(self,path=None):
        self.path=path or os.getenv("QOPTIQ_SQLITE_PATH","qoptiq_jobs.db")
        with self.db() as c:
            c.execute("CREATE TABLE IF NOT EXISTS jobs(id TEXT PRIMARY KEY,status TEXT,payload TEXT,result TEXT,error TEXT,created TEXT,updated TEXT)")
    def db(self): return sqlite3.connect(self.path,check_same_thread=False)
    def create(self,jid,payload):
        now=datetime.now(timezone.utc).isoformat()
        with self.db() as c: c.execute("INSERT INTO jobs VALUES(?,?,?,?,?,?,?)",(jid,"queued",json.dumps(payload),None,None,now,now))
    def update(self,jid,status,result=None,error=None):
        now=datetime.now(timezone.utc).isoformat()
        with self.db() as c: c.execute("UPDATE jobs SET status=?,result=?,error=?,updated=? WHERE id=?",(status,json.dumps(result) if result is not None else None,error,now,jid))
    def get(self,jid):
        with self.db() as c: row=c.execute("SELECT id,status,payload,result,error,created,updated FROM jobs WHERE id=?",(jid,)).fetchone()
        if not row:return None
        d=dict(zip(["id","status","payload","result","error","created","updated"],row))
        d["payload"]=json.loads(d["payload"]); d["result"]=json.loads(d["result"]) if d["result"] else None
        return d
