[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/Sitin/remote-4life)

Remote Coding For Life
======================

Setup scripts for remote coding.

Project Setup
-------------

Create a virtual environment and install requirements:

```shell script
mkvirtualenv remote-4life --python <path to python 3.7+>
```

Or switch to the virtual environment:

```shell script
workon remote-4life
```

Initialize the project:

```shell script
make setup
```

Then open `.env` file and fill the parameters.

Configuration
-------------

Perform this script to load parameters to `config.yaml`:

```shell script
make load
```

Edit `config.yaml` and upload it:

```shell script
make load
```

Clean up the config (for safety):

```shell script
make clean
```

Deploy
------

```shell script
make
```

SSH to Server
-------------

```shell script
make ssh
```

Destroy
-------

```shell script
make destroy
```

