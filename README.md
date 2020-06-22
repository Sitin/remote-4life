Eclipse Theia For Life
======================

Setup scripts for remote Eclipse Theia.

> Based on the [How To Set Up the Eclipse Theia Cloud IDE Platform on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-set-up-the-eclipse-theia-cloud-ide-platform-on-ubuntu-18-04) 
> DigitalOcean manuals.

Project Setup
-------------

Create a virtual environment and install requirements:

```shell script
mkvirtualenv theia-4life --python <path to python 3.7+>
pip install -r requirements.txt
```

Or switch to the virtual environment:

```shell script
workon theia-4life
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
