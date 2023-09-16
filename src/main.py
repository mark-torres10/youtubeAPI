"""Performs the key steps of the pipeline.

1. Sync the data
2. Perform data transformations

TODO: can be done via Airflow.
"""
from integrations.sync_integrations import main as sync_integrations
from transformations.main import main as transform_podcasts

def main() -> None:
    sync_integrations()
    transform_podcasts()
