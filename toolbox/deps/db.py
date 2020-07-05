import sqlite3
from pathlib import Path


class RepoDb:

    def __init__(self):
        db_dir = Path.home().joinpath("toolbox")
        db_dir.mkdir(exist_ok=True)
        self.db_path = db_dir.joinpath("test.db")

        self.conn = sqlite3.connect(str(self.db_path))
        self.cursor = self.conn.cursor()

    def insert(self, group_id: str, artifact_id: str):
        self.cursor.execute("INSERT INTO saved_deps VALUES (?, ?)", (group_id, artifact_id))
        self.conn.commit()

    def get_all(self):
        self.cursor.execute("select * from saved_deps")
        return self.cursor.fetchall()

    def __enter__(self):
        self.cursor.execute("""
        create table if not exists saved_deps
        (group_id text, artifact_id text)
        """)
        self.conn.commit()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
