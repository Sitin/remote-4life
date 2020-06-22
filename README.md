[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/Sitin/remote-4life)

Remote Coding For Life
======================

Setup scripts for remote coding.

Project Setup
-------------

Create a virtual environment and install requirements:

```shell script
mkvirtualenv remote-4life --python <path to python 3.7+>
pip install -r requirements.txt
```

Or switch to the virtual environment:

```shell script
workon remote-4life
```

Initialize the project:

```shell script
make init
```

Then open `.env` file and fill the parameters.

Deploy
------

```shell script
make
```
