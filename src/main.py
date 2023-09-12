"""Performs the key steps of the pipeline.

1. Sync the data
2. Perform data transformations
3. Dump data, load into Streamlit app.

TODO: can be done via Airflow.
"""
from integrations.sync_integrations import main as sync_integrations
from transformations.main import main as transform_podcasts
from visualizations.update_dashboard import main as update_dashboard

def main():
    sync_integrations()
    transform_podcasts()
    update_dashboard()
