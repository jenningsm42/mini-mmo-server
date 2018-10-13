# mini-mmo-server
The server for a very simple open world (not so massively) multiplayer online game. Mainly used as a playground for me to test various concepts in a networked environment.

## Requirements
* Protobuf compiler
* Python 3.7

A virtualenv is also highly recommended.

## Usage

### Locally
Copy the `proto/` folder from [mini-mmo-client](https://github.com/jenningsm42/mini-mmo-client) into the root directory of this repository first, then:

To install,

```
$ make
```

To run,

```
$ game-server [OPTIONS]
```

### Docker
First build the image,

```
$ docker-compose build
```

Then run it,

```
$ docker-compose up -d
```

### Options
* `-p <port>`, `--port <port>`: Bind to the specified port. Default: `1337`
* `-v`, `--verbose`: Enable verbose output, including debug-level logs.
* `--db <db-uri>`: Connect to the specified database, in any format accepted by SQLAlchemy. Default: `sqlite:///tmp/foobar.db`
