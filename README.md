Guildies API
==========

### Description

Guildies is an API for a fantasy RPG game focused on gathering the most unique items and becoming the most powerful guild with your friends. 


### Tech Stack
-Language: Python 3.6
-Framework: Flask
-Database: PostgreSQL
-Objection-relation mapper: SQLAlchemy


### Players

Players are identified by a unique ID, and provide a nickname and an email address when they sign up. They have a specific number of skill points, and they may possess zero or more items.

### Guilds

A guild consists of a team of two or more players. All guilds have a unique ID and a name, and  optionally a country code.

### Items

Items are special bonuses which the player encounters as they progress through the game, which can increase the player's skill points by a certain amount. If the player is not in a guild when they pick up an item, it simply increases their skill points. 

However, a special rule applies if a player is in a guild when they pick up an item: if anyone else in the guild has the same item, the skill points of the players with that item are decreased by the same amount first.


### Endpoints



/players/ [POST]
add a player to the database
~~~
    {
    	"nickname": "player1",
    	"email": "player1@email.com",
    	"skillpoints": 10
    }
~~~

/players/<Player_ID> [PUT]
update a player in the database
~~~
    {
    	"nickname": "player1",
    	"email": "UPDATEDplayer1@email.com",
    	"skillpoints": 15
    }
    values can be optionally omitted
~~~

/players/<Player_ID> [DELETE]
delete a player from the database

/guilds/ [POST]
add a guild to the database
~~~
    {
    	"name": "guild1",
    	"country_code": "105",
    }
    country_code can be optional

~~~

/guilds/<Guild_ID> [PUT]
update a guild in the database
~~~
    {
    	"name": "guild1",
    	"country_code": "106"
    }
    values can be optionally omitted
~~~

/guilds/<Guild_ID> [DELETE]
delete a guild from the database


/items/ [POST]
add an item to the database
~~~
    {
    	"skillpoints": "10"
    }
~~~

/items/<Item_ID> [PUT]
update an item in the database
~~~
    {
    	"skillpoints": "15"
    }
~~~

/items/<Item_ID> [DELETE]

/guilds/<int:guild_id>/players/<int:player_id> [PUT]
add a player to an existing guild

/guilds/<int:guild_id>/players/<int:player_id> [DELETE]
delete a player from an existing guild

/players/<int:player_id>/items/<int:item_id> [PUT]
add an item to a player

/guilds/<int:id>/skills [GET]
return the total skillpoints of a guild


All endpoints will return 
```
{
    "success": "true"
}
```
upon successful REST call

Getting started
---------------

The stack has been assembled as a set of Docker containers using `docker-compose`. The network is defined in `docker-compose.yml`, while the app server's image is defined in `Dockerfile`. 

To build the application and run it, install Docker and docker-compose on your computer, then run the following at a command prompt, in the current directory:

```
$ docker-compose up
```

This will take a few minutes as docker needs to download the images for Debian, PostgreSQL and so on that the containers are based on. Once all images are built the system will be available on localhost, port 5000 (which you can access through a web browser, postman etc.). Flask will automatically reload the server as you make changes to the code.

The entrypoint of the appserver image is also set up so that you can run arbitrary commands by supplying them on the command line. For example, to run an interactive Python shell, you would run

```
$ docker-compose run -p 5000:5000 appserver python
``` 

To get a shell inside the container, you would run


```
$ docker-compose run -p 5000:5000 appserver bash
```


You can rebuild by running 

```
$ docker-compose build
```

In some cases, you may need to supply the `--no-cache` flag to `docker-compose build` to force cached steps in the build to be regenerated.

### Configuration

The configuration for the application can be changed by editing the `Config` object in `app.py`.

### Database

The database is available inside the appserver container at the address `postgres:5432`. The username and password are `gamehive` and `gamehive`.

When you start the application for the first time, you will need to populate the database with the schema defined in your application. To do this, first find the name of the running app server container using `docker ps`:

```
$ docker ps
CONTAINER ID        IMAGE                COMMAND                  CREATED             STATUS              PORTS                    NAMES
0004849e6554        gamehive_appserver   "/docker-entrypoint...."   18 seconds ago      Up 22 seconds       0.0.0.0:5000->5000/tcp   gamehive_appserver_1
b1f97b5ad60f        postgres:9.6         "docker-entrypoint.s..."   19 seconds ago      Up 23 seconds       5432/tcp                 gamehive_postgres_1
```

We see here that the container is running as `gamehive_appserver_1`. We can now open a Python shell inside this container, and populate the schema as follows:

```
$ docker exec -ti gamehive_appserver_1 python
Python 3.6.4 (default, Dec 21 2017, 01:29:34)
[GCC 6.3.0 20170516] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from app import db
>>> db.create_all()
```

#### PostgresSQL shell

You can get a shell on the database server by running `psql` inside the postgres container, supplying the username and password on the command line:

```
$ docker exec -ti gamehive_postgres_1 psql gamehive gamehive
psql (9.6.6)
Type "help" for help.
