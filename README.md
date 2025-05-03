# Cloud Computing Final Project

**Uses the MVC Project Template for [BlackSheep](https://github.com/Neoteroi/BlackSheep)**

## Local Devopment Notes
Start server:
```bash
python3 -m venv venv
source venv/bin/activate.fish 
pip install -r requirements.txt
python dev.py
```

Migrate Local:
```bash
cd sql

sudo -u postgres createdb cloud
sudo -u postgres psql -d cloud -f create.sql
sudo -u postgres psql -d cloud
\copy households FROM 'households.csv' (format csv, null "null", DELIMITER ',', HEADER);
\copy products FROM 'products.csv' (format csv, null "null", DELIMITER ',', HEADER);
\copy transactions FROM 'transactions.csv' (format csv, null "null", DELIMITER ',', HEADER);

create role app with login password '{password}';
GRANT CONNECT ON DATABASE cloud to app;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app;
GRANT INSERT ON ALL TABLES IN SCHEMA public TO app;
GRANT USAGE ON SEQUENCE public.users_id_seq TO app;
```

## Cloud Development Notes
Useful Links:
- [Connect to Google Cloud SQL w/ PSQL](https://cloud.google.com/sql/docs/postgres/connect-admin-ip)
https://cloud.google.com/sql/docs/mysql/connect-app-engine-standard
- [App Engine Python](https://cloud.google.com/appengine/docs/standard/python3/building-app)

Migrate to Cloud SQL:
1. First, run:
    ```bash
    cd sql
    psql "sslmode=require hostaddr=IP_ADDR user=postgres dbname=postgres"
    \i create.sql
    \copy households FROM 'households.csv' (format csv, null "null", DELIMITER ',', HEADER);
    \copy products FROM 'products.csv' (format csv, null "null", DELIMITER ',', HEADER);
    \copy transactions FROM 'transactions.csv' (format csv, null "null", DELIMITER ',', HEADER);
    ```
2. Then, create an `app` user by following this [tutorial](https://cloud.google.com/sql/docs/postgres/create-manage-users)

Deploy:
1. gcloud app deploy
2. gcloud app logs tail -s default