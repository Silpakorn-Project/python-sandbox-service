# python-compiler-service
this is a python compiler service

## Swagger
http://localhost:8000/docs
http://localhost:8001/docs
## Installation
requirements
#####
python version 3.13.1 ***


clone project
```
git clone https://github.com/Silpakorn-Project/python-compiler-service.git
cd python-compiler-service
```

setup env
```
python3 -m venv env
or
python -m venv env
```

exec env
```
windows os
env/Sources/activate

macos
source env/bin/activate
```

install dependency
```
pip install -r requirements.txt
```

install image docker python-sandbox
```
docker build -t python-sandbox:latest . Dockerfile.sandbox
```

run
```
for develop
uvicorn app.main:app --reload
for production
uvicorn app.main:app 
```

## run
if you have docker you should this
```
docker-compose up --build
```

###
if you want to run sandbox you must wlil build dockerflie and config image name is python-sandbox to be able to run.
