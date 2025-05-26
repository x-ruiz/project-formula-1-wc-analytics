# SetUp
## Google Application Credentials
1. Export REPO_PATH to the root of the repository clone (/xxx/xxx/project-formula-1-wc)
1. Generate ADC file: ```gcloud auth application-default login``` -> ~/.config/gcloud/application_default_credentials.json
1. ```cp ~/.config/gcloud/application_default_credentials.json $REPO_PATH```
1. In .env, add GOOGLE_APPLICATION_CREDENTIALS=/usr/local/airflow/gcloud/application_default_credentials.json

<!-- ***After setting up .env and docker-compose.override.yaml to mount the local file***
1. Open the Airflow UI (usually http://localhost:8080).
1. Navigate to Admin -> Connections.
1. Edit or create a new Google Cloud connection (default Conn Id is often google_cloud_default).
1. Crucially, leave the Keyfile Path and Keyfile JSON fields empty.
1. (Optional but recommended) Fill in your Project Id.
1. Click Test and then Save. -->