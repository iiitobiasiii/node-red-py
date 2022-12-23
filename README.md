# node-red-py

This package simplifies usage of the node-red API.

## Installation

`python -m pip install path/to/project`

## Usage

See `example.ipynb`

connect to your node-red via the `NodeRedApi` class. Authenticate if necessary with its `authenticate` method and your username and password.
If you want to connect to influxdb or mqtt brokers that exist already in your node-red flows, get them and their IDs with `get_mqtt_brokers`  and `get_influxdb`.  

Build your flow with the `Flow` class in the `nodes` module. Add nodes with the different nodes in the `nodes` module. Add wires/connections with the connect_nodes function. 