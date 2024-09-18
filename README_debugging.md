### Debugging


Find the container ID of your flask and postgres containers:

```
docker ps 
```
Should look something like:

```
CONTAINER ID   IMAGE          COMMAND                  CREATED             STATUS             PORTS                                                                                  NAMES
83baf2dbbd3a   665a47a0ce37   "npm start"              About an hour ago   Up About an hour   0.0.0.0:2992->2992/tcp, :::2992->2992/tcp, 0.0.0.0:8080->5000/tcp, :::8080->5000/tcp   evseq_app_flask-dev_1
4623059f56b7   b9390dd1ea18   "docker-entrypoint.s…"   About an hour ago   Up About an hour   5432/tcp                                                                               evseq_app_postgres_1
```
Exec into the postgres db by running:

```
docker exec -it 4623059f56b7 bash
```

Where 4623059f56b7 is the container ID from before.

Once logged in then you need to initialise the database by running the initDB sql.
```
psql -U ylong levseq

```
Now paste in all the sql statements in `init_db.sql`.

To look at the table ya can go:
```
\l

\c levseq

\dt
```

If there is nothing there copy and paste the init_db.sql in!
Exec into the DB, first find the container ID and then exec into it:
```
docker exec -it 6c9fa1a6dfe5 psql -U ylong -d levseq;
```

Note you may need to remove the DB and restart if you're changing the password or something
```
docker rm -v -f $(docker ps -qa)
docker volume ls
 docker volume rm  levseq_vdb_postgres-data
```

Alternative is to just copy and paste the init DB stuff in (yes I'm sure there is a nicer way ;) ) if things have 
failed. You may need to have changed the 

After doing this you should be able to see the tables in there:

```
levseq=# \dt;
          List of relations
 Schema |    Name     | Type  | Owner 
--------+-------------+-------+-------
 public | batch       | table | ylong
 public | data        | table | ylong
 public | experiments | table | ylong
 public | groups      | table | ylong
 public | roles       | table | ylong
 public | users       | table | ylong
(6 rows)
```