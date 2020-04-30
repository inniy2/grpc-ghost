#!/bin/bash

# Copy to host2
scp -i /Users/baesangsun/.vagrant.d/boxes/percona/0/virtualbox/vagrant_private_key ./server.py vagrant@192.168.33.12:/home/vagrant/grpc-ghost

scp -i /Users/baesangsun/.vagrant.d/boxes/percona/0/virtualbox/vagrant_private_key ./ghost_pb2.py vagrant@192.168.33.12:/home/vagrant/grpc-ghost

scp -i /Users/baesangsun/.vagrant.d/boxes/percona/0/virtualbox/vagrant_private_key ./ghost_pb2_grpc.py vagrant@192.168.33.12:/home/vagrant/grpc-ghost


# apt install python3-pip
# pip3 install grpcio
# pip3 install mysql-connector-python