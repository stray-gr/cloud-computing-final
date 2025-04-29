# Cloud Computing Final Project

Project template for [BlackSheep](https://github.com/Neoteroi/BlackSheep)
web framework to start Web APIs.

## TODO (Q4 -> Q5 -> Q6 -> Q1 -> Q7)
- ~~create users table~~
- ~~load data into sql~~
- ~~create household dashboard (let users select household)~~
- add ability to view latest data (10 most recent results, let user make number bigger)
- add metrics to dashboard
- create write-up of AI models 
- ML IDEA: train model (input is a product, output is a product likely to be bought with input)

## NOTES
Start server:
```bash
python3 -m venv venv
source venv/bin/activate.fish 
pip install -r requirements.txt
npx @tailwindcss/cli -i ./app/static/input.css -o ./app/static/output.css --watch
python dev.py
```

For creating secret keys for sessions:
```bash
python -c 'import secrets; print(secrets.token_hex())'
cat 8451_The_Complete_Journey_2_Sample-2/400_transactions.csv | tr -d "[:blank:]" > transactions.csv 
```

Migrate:
```bash
sudo -u postgres createdb cloud
sudo -u postgres psql -d cloud -f sql/create.sql
sudo -u postgres psql -d cloud
\copy households FROM 'sql/households.csv' (format csv, null "null", DELIMITER ',', HEADER);
\copy products FROM 'sql/products.csv' (format csv, null "null", DELIMITER ',', HEADER);
\copy transactions FROM 'sql/transactions.csv' (format csv, null "null", DELIMITER ',', HEADER);

create role app with login password '{password}';
GRANT CONNECT ON DATABASE cloud to app;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app;
GRANT INSERT ON ALL TABLES IN SCHEMA public TO app;
GRANT USAGE ON SEQUENCE public.users_id_seq TO app;

sudo -u postgres psql -U app -h localhost cloud
```

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password BLOB NOT NULL,
    email TEXT NOT NULL
);
```
``` bash
> sqlite3 proj.db
sqlite> .read create.sql
sqlite> select * from users;
```

python:
- https://htmx.org/docs/
- https://tailwindcss.com/docs/installation/using-vite
- https://www.neoteroi.dev/blacksheep/sessions/
- https://www.geeksforgeeks.org/hashing-passwords-in-python-with-bcrypt/
- https://www.geeksforgeeks.org/using-python-environment-variables-with-python-dotenv/

SQLite:
- [Read Schema](https://www.sqlitetutorial.net/sqlite-describe-table/)
- [CSV](https://www.sqlitetutorial.net/sqlite-import-csv/)
- [Insert](https://www.sqlitetutorial.net/sqlite-python/insert/)
    - refer to `add_task` and `main`
- [Select](https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/)

PSQL:
- [Upload CSV](https://stackoverflow.com/questions/2987433/how-to-import-csv-file-data-into-a-postgresql-table)

Azure:
- https://learn.microsoft.com/en-us/azure/app-service/getting-started?pivots=stack-python
- https://learn.microsoft.com/en-us/azure/app-service/tutorial-python-postgresql-app-flask?tabs=copilot&pivots=azure-portal
- https://learn.microsoft.com/en-us/azure/app-service/configure-language-python

## Getting started

1. create a Python virtual environment
2. install dependencies
3. run the application

### For Linux and Mac

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python dev.py
```

### Env variables

To test applying a different color to the top section, set an env variable
`BG_COLOR` with a valid value for a CSS color.

```bash
BG_COLOR="#fd7e14" python dev.py
```

To test serving the application at a different path prefix, set an env variable
`APP_ROUTE_PREFIX` with the desired prefix. This feature is available since
BlackSheep 2.1.0, and can be useful when using a proxy server and path based
routing.

```bash
APP_ROUTE_PREFIX="orange" python dev.py
```

### Docker

Build an image using the example image.

```bash
docker build -t mvcdemo .
```

Run the image once built, for example to map from the host `8080`:

```bash
docker run --rm -p 8080:80 mvcdemo
```

To test running with customizations to test the application at a different
path:

```bash
docker run --name mvcdemo --rm -p 8080:80 -e BG_COLOR='#fd7e14' -e APP_ROUTE_PREFIX='orange' mvcdemo
```

Then navigate to [http://localhost:8080/orange/](http://localhost:8080/orange/).

To test using the image from Docker Hub:

```bash
docker run --name mvcdemo --rm -p 8080:80 \
    -e BG_COLOR='#fd7e14' \
    -e APP_ROUTE_PREFIX='orange' \
    robertoprevato/mvcdemo
```
