from datetime import date
import os
import subprocess
import sys

from cloudharness.applications import get_current_configuration
from cloudharness.utils.config import CloudharnessConfig


def _copy_query_to_csv(query, fname):
    """Write a \\copy query result to fname, atomically. A `\\copy` interrupted partway
    (worker recycle, pod restart, DB hiccup, ...) leaves a partial file behind; copying to
    a temp path first and renaming into place on success ensures a partial write is never
    mistaken for a completed export by callers that check fname's existence/mtime."""
    app = get_current_configuration()
    my_env = os.environ
    os.environ["PGPASSWORD"] = app.harness.database['pass']
    tmp_fname = f"{fname}.tmp"
    proc = subprocess.run([
        "psql", "-h",
        f"{app.db_name}.{CloudharnessConfig.get_namespace()}",
        "-U", app.harness.database.user,
        "-d", app.harness.database.postgres['initialdb'],
        "-c",
        f"\\copy ({query}) TO '{tmp_fname}' DELIMITER ',' CSV HEADER"],
        env=my_env,
        stderr=subprocess.STDOUT,
        text=True
    )
    if proc.returncode != 0:
        if os.path.exists(tmp_fname):
            os.remove(tmp_fname)
        raise Exception("Error during csv export: %s", proc.stdout)
    os.replace(tmp_fname, fname)


def generate_antibodies_csv_file(fname, status="CURATED"):
    app = get_current_configuration()
    _copy_query_to_csv(f"{app['export_query']} AND status='{status}'", fname)


def generate_antibodies_fields_by_status_to_csv(fname, status:str='', lastedit_time: date=None):
    app = get_current_configuration()
    query = app['export_all_fields_query']
    if status:
        query += f" AND status='{status}'"
    if lastedit_time:
        query += f" AND lastedit_time::date >= '{lastedit_time}'"
    _copy_query_to_csv(query, fname)


if __name__ == '__main__':
    def test_export(self):
        from api.services import export_service
        fname = "/tmp/f.csv"
        export_service.generate_antibodies_csv_file(fname)

        with open(fname) as f:
            l = f.readlines()
            assert l
    test_export()
