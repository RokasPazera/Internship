import os
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


load_dotenv()
url = os.getenv("INFLUXDB_URL")
token = os.getenv("INFLUXDB_TOKEN")
org = os.getenv("INFLUXDB_ORG")
bucket = os.getenv("INFLUXDB_BUCKET")

if not token:
    raise ValueError("Missing required token credentials in .env file.")
if not org:
    raise ValueError("Missing required org credentials in .env file.")
if not bucket:
    raise ValueError("Missing required bucket credentials in .env file.")

client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()

check_query = f'from(bucket: "{bucket}") |> range(start: -30d) |> filter(fn: (r) => r._measurement == "meters") |> limit(n: 1)'
existing = query_api.query(org=org, query=check_query)

if any(table.records for table in existing):
    print("Seed data already present, skipping.")
else:
    write_api = client.write_api(write_options=SYNCHRONOUS)
    for i in range(20):
        point = Point("meters") \
            .tag("sensor", "sensor1") \
            .field("distance", 80 - i)
        write_api.write(bucket=bucket, org=org, record=point)
        print("Data point successfully written!")

client.close()
