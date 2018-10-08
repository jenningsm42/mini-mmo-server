# mini-mmo-server
The server for a very simple open world (not massively) multiplayer online game

## Requirements
* Protobuf compiler
* Python 3.7

A virtualenv is also highly recommended.

## Usage
Copy the `proto/` folder from [mini-mmo-client](https://github.com/jenningsm42/mini-mmo-client) into the root directory of this repository first!

To install:

```
$ make
```

To run:

```
$ game-server
```

Currently the `-v` and `-p <port>` arguments are available - verbose and port number.
