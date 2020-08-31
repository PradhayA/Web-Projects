import os, csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# database engine object from SQLAlchemy that manages connections to the database
engine = create_engine("postgres://olkgsqchlhpaoz:3651fa44b38ac56408cc63f33de0aaea4e7f7ffee79acabce7b4f36dd203f229@ec2-54-247-79-178.eu-west-1.compute.amazonaws.com:5432/d8namlnsojbocv")
print(engine)
# create a 'scoped session' that ensures different users' interactions with the
# database are kept separate
db = scoped_session(sessionmaker(bind=engine))

file = open("books.csv")

reader = csv.reader(file)

db.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, username VARCHAR NOT NULL, password VARCHAR NOT NULL)")
db.execute(
    "CREATE TABLE reviews (user_id integer NOT NULL,comment VARCHAR NOT NULL, rating INTEGER NOT NULL,book_id integer NOT NULL, time timestamp NOT NULL)")
db.execute(
    "CREATE TABLE books (id SERIAL PRIMARY KEY, isbn VARCHAR NOT NULL,title VARCHAR NOT NULL,author VARCHAR NOT NULL,year VARCHAR NOT NULL)")

for isbn, title, author, year in reader:

    db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                {"isbn": isbn, 
                 "title": title,
                 "author": author,
                 "year": year})

    print(f"Added book {title} to database.")

    db.commit()