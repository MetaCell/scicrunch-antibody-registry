import psycopg2
from cloudharness import applications

app = applications.get_configuration('areg-portal')
conn_string = f"postgres://{app.db_name}:{app.harness.database.postgres.ports[0]['port']}/asu?user={app.harness.database.user}&password=metacell"
conn = psycopg2.connect(conn_string)
connection = psycopg2.connect(user=app.harness.database.user,
                              password="pynative@#29",
                              host=app.db_name,
                              port=app.harness.database.postgres.ports[0]['port'],
                              database=app.db_name)
cur = conn.cursor()
