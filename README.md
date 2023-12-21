## Homework 08

### The first part
#### Output data

We have a json file (`authors.json`) with authors and their properties: date and place of birth, a brief biography.

We also have a json file (`qoutes.json`) with quotes from these authors.

Procedure:

     1. We created the Atlas MongoDB cloud database.
     2. With the help of Mongoengine ODM, we created models for storing data from these files in the authors and quotes collections.
     3. When storing quotes, the author field in the document should not be a string value, but a [Reference fields] field where the ObjectID from the authors collection is stored.
     4. Wrote scripts for uploading json files to the cloud database.
     5. Implemented a script for searching quotes by tag, author's name or a set of tags. The script is executed in an infinite loop and accepts commands in the following format `command: value' using the usual input operator.
     6. Implemented for the name:Steve Martin and tag:life commands the ability to write abbreviated values for searching, for example name:st and tag:li, respectively.
     7. Cached the result of executing the name: and tag: commands using Redis, so that the search result is not taken from the MongoDB database, but from the cache upon repeated request.

Example:
     `name: Steve Martin` — find and return a list of all quotes by the author Steve Martin;
     `tag:life` — find and return a list of quotes for the tag life;
     `tags:life,live` — find and return a list of quotes with life or live tags (note: no spaces between life, live tags);
     `exit` — end the execution of the script

Display search results only in utf-8 format.

### The second part

    1. Wrote two scripts: consumer.py and producer.py. Using RabbitMQ, we organized the simulation of email distribution to contacts using queues.
    2. Using ODM Mongoengine, created a contact model. The model includes the following fields: full name, email, and a logical field that has a value of False by default. It means that the message to the contact has not been sent and should become True when sent.
    3. When the producer.py script is run, it generates a certain number of fake contacts and writes them to the database. Then queues a RabbitMQ message containing the ObjectID of the generated contact, and so on for all generated contacts.
    4. The consumer.py script receives a message from the RabbitMQ queue, processes it and simulates sending a message by email with a stub function. After the message is sent, the boolean field for the contact becomes True. The script runs constantly waiting for messages from RabbitMQ.