# A simple Site to post articles using python's Flask

_This is a simple blogging site created with Flask as backend._

This uses two tables, One for storing user's information (user_info) and another one to store the articles posted by the users (articles). (Oracle Database)

To create `user_info` table, use the following syntax:

```
create table user_info(ID number generated always as identity START WITH 1000 INCREMENT BY 1,
name varchar2(50),
email varchar2(50),
username varchar2(20),
password varchar2(100),
register_date timestamp
);
```
To create `articles` table, use the following syntax:

```
create table articles(ID number generated always as identity START WITH 1000 INCREMENT BY 1,
title varchar2(50),
author varchar2(50),
body blob,
post_date timestamp
);
```
To run the app, open a command prompt, then: 
```
python app.py
```
Open a browser and point to localhost.
