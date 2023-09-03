# Build you own redis-like database (BYOR) ☁️

It is an example implementation of socket programming in Python3 by recreating the well-known in-memory data storage Redis. 

Currently, it has only these commands

- GET
- SET

Also, I implemented encoding and decoding protocols of only

- Integer
- String
- Error

Lastly, it can serve for *multiple clients* and *handling race condition with lock mechanism*.


In order to run, please follow these steps:

1. Create and activate python3 environment (for virtualenv users):

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Go to the project folder:

```bash 
cd ./byor
```

3. Run the server first with the command:

```bash
python -m byor.main run-server
```

4. Now, server is ready to accept connections. And you can open a new terminal/terminals and start using commands. 

- Adding value to the db:
```bash
python -m byor.main set key1 val1
```
- Getting (Querying the value of the key):
```bash
python -m byor.main get key1
```


