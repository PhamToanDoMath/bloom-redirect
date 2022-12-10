# Miniproject Distributed System
## Introduction
This is a proof of concept project to prove the feasibility of using Bloom Filter in authentication and redirecting users in distributed computing.

## Disclaimer
In this repository, I used *pybloom* - a Python library that supports multiple variance of Bloom Filter.

# Installation
```
python python-bloomfilter/setup.py
python api.py
curl -L  -X POST -H "Content-type:application/json" -d '{"username":"toan","password":"pham"}' http://127.0.0.1:8080/login
python client-flask/api.py
```

# Functionality Test

Register new user into given domain (e.g: localhost:9999)
```
curl -X POST -H "Content-type:application/json" -d '{"username":"toan","password":"pham","company":"localhost:9999"}' http://127.0.0.1:8080/users
```

Login with username and password and get redirected to correct domain name
```
curl -L  -X POST -H "Content-type:application/json" -d '{"username":"toan","password":"pham"}' http://127.0.0.1:8080/login
```
