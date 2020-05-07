#!/bin/bash

# Copy to u2
# scp -i /Users/baesangsun/.vagrant.d/boxes/percona/0/virtualbox/vagrant_private_key ./server.py vagrant@192.168.33.12:/home/vagrant/grpc-ghost
# scp -i /Users/baesangsun/.vagrant.d/boxes/percona/0/virtualbox/vagrant_private_key ./ghost_pb2.py vagrant@192.168.33.12:/home/vagrant/grpc-ghost
# scp -i /Users/baesangsun/.vagrant.d/boxes/percona/0/virtualbox/vagrant_private_key ./ghost_pb2_grpc.py vagrant@192.168.33.12:/home/vagrant/grpc-ghost


sudo lxc file push server.py  ghost_pb2.py ghost_pb2_grpc.py config.ini  u1/root/grpc-ghost/
sudo lxc file push server.py  ghost_pb2.py ghost_pb2_grpc.py config.ini  u3/root/grpc-ghost/

# sudo chown  -R '165536'.'165536'  /var/lib/lxd/containers/u2/rootfs/root/grpc-ghost

# apt install python3-pip
# pip3 install grpcio
# pip3 install mysql-connector-python