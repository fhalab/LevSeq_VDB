# levseq

Web app for locally hosting levseq. Our goal is to make this also as a centralised resource, for this we are 
working with other protein database managers and software engineers, so stay tuned! We would love feedback in 
the meantime about how we can improve sequnece function data collection and sharing. If you have any suggestions
please post an issue, we would love to build this into a community driven thing.

## Running once setup


```bash
docker compose up postgres
```

```bash
docker compose up flask-dev
```

Then just go to your local server: `http://127.0.0.1:8080/` you should be able to see the below!

![screenshot](images/main.png)


## Database setup (only run the first time)

You'll need to create a .env file with the following variables:

```
DB_URL=postgresql://{the user below}:{the password below}@postgres:5432/{name of the DB}
DB_USER=
DB_PASSWORD=
SECRET_KEY=
```

You need to have docker installed for this to work, this has been tested on a mac and linux!

** TBH I had issues running the database so I combined it into the docker compose. This could be problematic for a 
full prod deployment so something to consider.**

First run docker compose to spin everything up:
```bash
docker compose up postgres
```

```bash
docker compose up flask-dev
```

