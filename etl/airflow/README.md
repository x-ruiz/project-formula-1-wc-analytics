# SetUp (Local Development)
## Google Application Credentials
1. Export REPO_PATH to the root of the repository clone (/xxx/xxx/project-formula-1-wc)
1. Generate ADC file: ```gcloud auth application-default login``` -> ~/.config/gcloud/application_default_credentials.json
1. ```cp ~/.config/gcloud/application_default_credentials.json $REPO_PATH/etl/credentials/gcloud```
1. In .env, add GOOGLE_APPLICATION_CREDENTIALS=/usr/local/airflow/gcloud/application_default_credentials.json\

## Kaggle Credentials
1. Download API Credential file from Kaggle
1. Move kaggle.json to $REPO_PATH/etl/credentials/kaggle
1. In .env, add KAGGLE_CONFIG_DIR=/usr/local/airflow/credentials/kaggle
