import csv
import requests
from dagster import get_dagster_logger, job, op


@op(config_schema={"url": str})
def download_csv(context):
    response = requests.get(context.op_config["url"])
    lines = response.text.split("\n")
    return [row for row in csv.DictReader(lines)]

@op
def sort_by_calories(cereals):
    sorted_cereals = sorted(cereals, key=lambda cereal: int(cereal["calories"]))
    get_dagster_logger().info(f'Most caloric cereal: {sorted_cereals[-1]["name"]}')


@job
def configurable_job():
    sort_by_calories(download_csv())