# 4rexify-api

4rexify-backend is the backend of 4rexify app

## Installation
Follow these few steps to deploy the project on your workstation.
This is for workstation running in Linux or MacOS only.

### Requirements
Before following these steps, make sure to have installed:
* [Python3](https://phoenixnap.com/kb/how-to-install-python-3-ubuntu)
* [Pip3](https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/)
* Virtual environment: `sudo apt install -y python3-venv` || `pip install virtualenv`
* [Git Installed](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [Git Setup](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup)

Let's start now

### Clone the project
```
git@github.com:codewithmide/4Rexify.git
```

### Create a virtual environment to isolate our package dependencies locally
`python3 -m venv venv` || `virtualenv venv`

### Activate the virtual environment
`. venv/bin/activate`

### Move to the cloned project folder and install the requirements
```
cd 4rexify-api
pip3 install -r requirements.txt
```

### Setup your environment variables
To setup your environment variables:
  * Duplicate the **.env.sample** file and rename it as **.env**
  * Edit the new **.env** file with the your own informations as described in the file

## Usage
Nothing is simpler than this ):
Just run the server with `python runserver` that's all!

**Happy Coding!!!!**


