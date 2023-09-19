# Enriching podcast data with YouTube data

## Overview
The purpose of this project is to build a simple MVP for a REST API and a data pipeline that enriches Spotify podcast data with YouTube podcast data. It uses Python and the Spotify/YouTube APIs to obtain the necessary data, transforms them into a unified "Podcast" dataset, and then writes this into a SQLite database, to be accessed by a Django-based REST API. This is the start of a simple data pipeline for enriching various podcast data sources together.

** disclaimer: as an MVP, the project is still a work-in-progress and debugging still needs to be done. But, the data pipeline logic does work, and the core implementation of the product is available. **

## Primary Purpose
By having more diverse datasets and data integration sources, we can further enrich the podcast data that we provide to customers. By doing so, we can help customers better find the podcast audiences most suited for them and get more ROI for their time and advertisement.

## Data Sources
This project currently uses two primary data sources: (1) Spotify and (2) YouTube. This project uses the Spotify dataset as the "ground truth", since I assumed that most podcasts of note would exist, at the very least, on Spotify. YouTube is used as the enrichment source. 

As a first pass, I use one podcast (Andrew Huberman) as a working sample for this MVP. However, the modules are generalizable enough to be easily extended beyond just a single podcast.

A current shortcoming in the dataset is that the Spotify and YouTube APIs largely provide metadata (though YouTube does provide basic engagement metrics such as views and listens). It would be great if there were another, perhaps proprietary, dataset that delved into listening session metrics, such as how long a user played a podcast episode for and how many times they paused as well as information about the users themselves (so we can build a better image of the niche of users for whom the podcast appeals to).

## Data Sources Not Covered (but considered)
The workflow that is used here can easily support other integrations being added as well. As a part of this project, though I scoped it to only YouTube and Spotify, I also considered what other integrations could be useful. Some that came to mind include:
- Apple podcasts: another source of podcast information.
- Twitter: can be used, for example, as another way to measure engagement with a podcast. It could be possible, for example, to enrich podcast listening/streaming numbers with Twitter metrics in order to build a wider "engagement" metric and to better understand a podcast's reach.
- Google Trends: another source of metrics that can measure a podcast's audience size and reach. By doing, for example, keyword searches on the key topics covered in a given podcast, we can estimate a podcast's current and potential possible audience and estimate what their future audience sizes could be.
- Information about podcast hosts: some of these include:
    - IMDb
    - Rotten Tomatoes
    - Wikipedia

## Data Pipeline
The data pipeline consists of two main steps:
1. Data sync (managed in `src/integrations/sync_integrations.py`). Runs logic for syncing Spotify and YouTube podcast channels and podcast videos. Currently hardcoded to support only one channel (Andrew Huberman) as part of the MVP, but already built to support more (and a future "podcast discovery" service should exist upstream of this one to kick it off). Writes the synced data to a SQLite DB.
2. Data mapping (managed in `src/transformations/main.py`). Maps, transforms, and enriches the different data source to create a unified understanding of podcast data. Currently it consolidates YouTube and Spotify data into one, but can support further integrations plus more transformations. Creates mappings for "MappedChannel" and "MappedEpisode", unified understandings of podcast channels and episodes respecitvely which are to be enriched by each data source. Writes the synced data to a SQLite DB.

## API Endpoints
Simple Django-based REST API that exposes two API endpoints.
- GET /api/channels: returns a list of all the podcast channels.
- GET /api/episodes: returns a list of all the podcast episodes.
For the sake of an MVP, the output of the REST API just returns all the data in the format that they are stored in the SQLite DB and without any checking, filtering, etc. Future work should elaborate on the API features, such as returning episodes that meet a certain query or returning the episodes for only a certain channel. 

## Technology Stack
- Data pipeline: Python
- Frontend: React (very simple frontend, just contains two buttons, one to call each API endpoint, and upon clicking, returns the result as a table)
- Backend: Django
- DB: SQLite
- Caching: Redis (used primarily on the sync side to cache requests to YouTube and Spotify APIs to avoid getting rate-limited during development).
- Orchestration: Airflow (set to update every 24 hours)
- Deployment: Docker
- CI/CD: Github Actions
- Logging: logger Python module
- Linting/code quality: mypy, pre-commit hooks

## Possible Future Improvements
- A "podcast discovery" service upstream of the data pipeline that "discovers" podcasts (e.g., by scraping the Top 10 lists), and then adds them to a database of all known podcasts.
- A "podcast resync" service upstream of the data pipeline that, for every given podcast, can kick off the data pipeline so that a given podcast's data can be resynced.
- Discussion into ways that a podcast's "reach" can be measured. It's probably true that the most direct measure of a podcast's viability as an advertising outlet for a business is direct listens. However, if this podcast (or the podcast host) uses other social media, we can do supplementary analyses to get a better idea for the podcast's reach as well as what people think about it. For example, we can look at YouTube's engagement metrics (likes, number of views, etc.) and the comments on a given podcast upload to get a more diverse picture of user engagement than just number of listens.
- Data Quality and Validation: Enhance data validation and quality checks in the data pipeline. Implement automated checks to identify and handle missing or inconsistent data. Introduce data versioning and rollback mechanisms to maintain data integrity. Can use tools such as "Great Expectations" for this purpose.
- Scalability: As the user base grows, ensure the system can scale horizontally to handle increased traffic and data volume. Can move away from SQLite into something like Postgres.
