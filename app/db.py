from contextlib import contextmanager
import json
from pathlib import Path
import sqlite3
import uuid
from app.services.audit import canonical, digest, timestamp

class Store:
    def __init__(self, path):
        self.path = str(path)

    @contextmanager
    def connection(self):
        conn = sqlite3.connect(self.path, timeout=5)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys=ON')
        try:
            yield conn
            conn.commit()
        except BaseException:
            conn.rollback()
            raise
        finally:
            conn.close()

    def initialize(self):
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as conn:
            conn.execute('PRAGMA journal_mode=WAL')
            conn.executescript('''
                CREATE TABLE IF NOT EXISTS facilities(id TEXT PRIMARY KEY, body TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS runs(id TEXT PRIMARY KEY, facility_id TEXT NOT NULL,
                    status TEXT NOT NULL, created_at TEXT NOT NULL, request TEXT NOT NULL, error TEXT,
                    request_key TEXT UNIQUE);
                CREATE UNIQUE INDEX IF NOT EXISTS one_active_run ON runs((1))
                    WHERE status IN ('collecting', 'evaluating');
                CREATE TABLE IF NOT EXISTS snapshots(run_id TEXT PRIMARY KEY REFERENCES runs(id),
                    body TEXT NOT NULL, hash TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS results(run_id TEXT PRIMARY KEY REFERENCES snapshots(run_id), body TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS decisions(id TEXT PRIMARY KEY, run_id TEXT UNIQUE REFERENCES results(run_id),
                    idempotency_key TEXT UNIQUE NOT NULL, request_hash TEXT NOT NULL, body TEXT NOT NULL, bundle_hash TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS outbox(decision_id TEXT PRIMARY KEY REFERENCES decisions(id), body TEXT NOT NULL);
            ''')
            for table in ('snapshots', 'results', 'decisions', 'outbox'):
                for operation in ('UPDATE', 'DELETE'):
                    conn.execute(f"CREATE TRIGGER IF NOT EXISTS immutable_{table}_{operation.lower()} BEFORE {operation} ON {table} BEGIN SELECT RAISE(ABORT, 'immutable record'); END")
            conn.execute("UPDATE runs SET status='interrupted', error='SERVER_RESTART' WHERE status IN ('collecting','evaluating')")
            facility = {'facility_id':'kc-demo', 'display_name':'Kansas City — Synthetic Administrative Office',
                'synthetic':True, 'latitude':39.0997, 'longitude':-94.5786, 'timezone':'America/Chicago',
                'opening_time_local':'08:00', 'closing_time_local':'17:00', 'working_days':[0,1,2,3,4],
                'minimum_notice_minutes':30, 'telework_supported':True, 'supervisor_contact_label':'Demo facility supervisor'}
            conn.execute('INSERT OR IGNORE INTO facilities VALUES (?, ?)', (facility['facility_id'], canonical(facility)))

    def facilities(self):
        with self.connection() as conn:
            return [json.loads(row[0]) for row in conn.execute('SELECT body FROM facilities ORDER BY id')]

    def facility(self, id):
        with self.connection() as conn:
            row = conn.execute('SELECT body FROM facilities WHERE id=?', (id,)).fetchone()
        if not row:
            raise KeyError(id)
        return json.loads(row[0])

    def add_facility(self, body):
        with self.connection() as conn:
            conn.execute('INSERT INTO facilities VALUES (?,?)', (body['facility_id'], canonical(body)))

    def create_run(self, body, key):
        with self.connection() as conn:
            existing = conn.execute('SELECT id,request FROM runs WHERE request_key=?', (key,)).fetchone()
            if existing:
                if existing['request'] != canonical(body):
                    raise ValueError('Idempotency key reused with different evaluation')
                return existing['id'], False
            id = str(uuid.uuid4())
            conn.execute('INSERT INTO runs(id,facility_id,status,created_at,request,request_key) VALUES (?,?,?,?,?,?)',
                         (id, body['facility_id'], 'collecting', timestamp(), canonical(body), key))
            return id, True

    def update_run(self, id, status, error=None):
        with self.connection() as conn:
            conn.execute('UPDATE runs SET status=?,error=? WHERE id=?', (status,error,id))

    def save_snapshot(self, id, body):
        with self.connection() as conn:
            conn.execute('INSERT INTO snapshots VALUES (?,?,?)', (id,canonical(body),digest(body)))
        return digest(body)

    def save_result(self, id, body, status):
        with self.connection() as conn:
            conn.execute('INSERT INTO results VALUES (?,?)', (id,canonical(body)))
            conn.execute('UPDATE runs SET status=? WHERE id=?', (status,id))

    def run(self, id):
        with self.connection() as conn:
            row = conn.execute('SELECT * FROM runs WHERE id=?', (id,)).fetchone()
            snap = conn.execute('SELECT body,hash FROM snapshots WHERE run_id=?',(id,)).fetchone()
            result = conn.execute('SELECT body FROM results WHERE run_id=?',(id,)).fetchone()
            decision = conn.execute('SELECT id FROM decisions WHERE run_id=?',(id,)).fetchone()
        if not row:
            raise KeyError(id)
        data = dict(row)
        data['request'] = json.loads(data['request'])
        if snap:
            data['snapshot'] = json.loads(snap['body'])
            if digest(data['snapshot']) != snap['hash']:
                raise ValueError('Snapshot integrity failure')
            data['snapshot_hash'] = snap['hash']
        if result:
            data.update(json.loads(result['body']))
        if decision:
            data['decision_id']=decision['id']
        return data

    def recent(self):
        with self.connection() as conn:
            return [dict(row) for row in conn.execute('SELECT id,facility_id,status,created_at FROM runs ORDER BY created_at DESC LIMIT 50')]

    def decisions(self):
        with self.connection() as conn:
            return [{'decision_id':row['id'], **json.loads(row['body'])['decision']} for row in conn.execute('SELECT id,body FROM decisions ORDER BY rowid DESC LIMIT 50')]

    def replay(self, id):
        with self.connection() as conn:
            row = conn.execute('SELECT body,bundle_hash FROM decisions WHERE id=?',(id,)).fetchone()
        if not row:
            raise KeyError(id)
        body = json.loads(row['body'])
        if digest(body) != row['bundle_hash']:
            raise ValueError('Historical bundle integrity failure')
        return {'mode':'REPLAY', 'bundle_hash':row['bundle_hash'], **body}
