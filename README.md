##
---
How to build in ubuntu

`python3 --version`

`sudo apt install python-pip`

`sudo apt install virtualenv`

`virtualenv venv --python=python3.6`

`source venv/bin/activate`

`pip install grpcio`

`pip install grpcio-tools`

`pip install mysql-connector-python`

`pip install configparser`

`python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/ghost.proto`