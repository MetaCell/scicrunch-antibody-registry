import os
import subprocess
import sys

from cloudharness.applications import get_current_configuration
from cloudharness.utils.config import CloudharnessConfig


def generate_antibodies_csv_file(fname, status="CURATED"):
    app = get_current_configuration()
    my_env = os.environ
    os.environ["PGPASSWORD"] = app.harness.database['pass']
    # execute shell command
    proc = subprocess.run([
        "psql", "-h",
        f"{app.db_name}.{CloudharnessConfig.get_namespace()}",
        "-U", app.harness.database.user,
        "-d", app.harness.database.postgres['initialdb'],
        "-c",
        f"\\copy ({app['export_query']} AND status='{status}') TO '{fname}' DELIMITER ',' CSV HEADER"],
        env=my_env,
        stderr=subprocess.STDOUT,
        text=True
    )
    if proc.returncode != 0:
        raise Exception("Error during csv export: %s", proc.stdout)


def generate_all_antibodies_fields_to_csv(fname, status="CURATED"):
    app = get_current_configuration()
    my_env = os.environ
    os.environ["PGPASSWORD"] = app.harness.database['pass']
    # execute shell command
    proc = subprocess.run([
        "psql", "-h",
        f"{app.db_name}.{CloudharnessConfig.get_namespace()}",
        "-U", app.harness.database.user,
        "-d", app.harness.database.postgres['initialdb'],
        "-c",
        f"\\copy ({app['export_all_fields_query']} AND status='{status}') TO '{fname}' DELIMITER ',' CSV HEADER"],
        env=my_env,
        stderr=subprocess.STDOUT,
        text=True
    )
    if proc.returncode != 0:
        raise Exception("Error during csv export: %s", proc.stdout)


if __name__ == '__main__':
    def test_export(self):
        from api.services import export_service
        fname = "/tmp/f.csv"
        export_service.generate_antibodies_csv_file(fname)

        with open(fname) as f:
            l = f.readlines()
            assert l
    test_export()
