# project-formula-1-wc-analytics
UChicago Applied Data Analytics Supplementary Project

This project aims at creating historical dashboards representing data points across
formula 1 championships. Therefore, the ETL pipelines created are meant to be triggered
infrequently to ingest the raw data, as the dataset is not changing frequently. Dataset updates
etc. would require the pipelines to be retriggered manually.

***Trello***: https://trello.com/b/Fjycvl2O

## Ideation Phase
1. Aggregate circuits raw table with csv dataset containing population of each city, to see if there is
relationship with city density to circuit attendance

## Installations
### Airflow
https://www.astronomer.io/docs/astro/cli/install-cli/?tab=mac#install-the-astro-cli
```brew install airflow```
```astro dev init```

### GCloud Credentials
For local development only:
```gcloud auth application-default login``` -> ~/.config/gcloud/application_default_credentials.json

Allows for local api requests to GCP using python libraries. For production deployment, export a service
account credentials file and use as an ENV variable.

## Design Decisions
### Raw Data Storage
Chose to go with parquet over keeping things in CSV due to compression benefits and columnar benefits
(querying speed etc.)

- Choosing parquet over arrow since we want long term disk storage (not in memory)
- Choosing parquet over avro since we are likely only going to load certain columns, and not
entire rows, taking advantage of the columnar storage format.

### Raw Data ETL
Extract Raw Kaggle Data -> Transform to Parquet -> Load to GCS

Using pandas as total csv file size for all files is ~20MB which is small enough to be able to load
into memory before creating parquet files. 

### Processing ETL
Lets aggregate the raw data with another csv to show csv reading capabilities and transformations with pandas/or spark

