# levseq

Web app for locally hosting levseq. Our goal is to make this also as a centralised resource, for this we are 
working with other protein database managers and software engineers, so stay tuned! We would love feedback in 
the meantime about how we can improve sequnece function data collection and sharing. If you have any suggestions
please post an issue, we would love to build this into a community driven thing.

## Running
You need to set your `.env` file (see below) but otherwise the below should work! (add the below lines to a .env file)

```
DATABASE_URL=postgresql://{the user below}:{the password below}@postgres:5432/{name of the DB}
DB_USER=
DB_PASSWORD=
SECRET_KEY=
# Environment variable overrides for local development
FLASK_APP=levseq_vdb/app.py
FLASK_DEBUG=1
FLASK_ENV=development
GUNICORN_WORKERS=1
LOG_LEVEL=debug
# In production, set to a higher number, like 31556926
SEND_FILE_MAX_AGE_DEFAULT=0

```

```bash
docker compose up postgres
```

```bash
docker compose up flask-dev
```

Then just go to your local server: `http://127.0.0.1:8080/` you should be able to see the below!

![screenshot](images/main.png)


## Database setup (only run the first time)


You need to have docker installed for this to work, this has been tested on a mac and linux!

