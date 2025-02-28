# BEE-AGENT TOOLS FOR DEVOPS TASKS

### Automated Tools for DevOps tasks like deployment, ssl certificate renewal and checking certificate expiry.
### This Repo contains automated scripts with a flask application which exposes these automated scripts to a local url. Bee-Agent can hit these api's to run these scripts as it's tools.
### This Repo also includes this scripts as python function tools in the tools directory, which can be directly fed to Bee-Agent as a tool.

## Get Started

> NOTE  
> If you don't have python installed, expand and run the following section first.

<details><summary> [Required] Install Python 3.11+ on Your Laptop</summary>

1. Install `brew` if you have a MAC
```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Install `Python 3.11`, change the version of python if needed
```sh
brew install python@3.11
```
</details>

## Installation and Setup
1. Clone this Repo:
    ```
    git clone git@github.com:IBM/SSLCertificationPython.git
    cd SSLCertificationPython/ApplicationUtilities
    ```

2. Install Dependencies:
    ```
    pip install -r requirements.txt
    ```

## Running the application
#### renew_app.py is the flask application containing all the routes for all automating scripts. Running this file will expose all the scripts to an api url which Bee-Agent can access.
```
python3 renew_app.py
```


## Setup Bee-Agent
#### Add all the python function tools mentioned in the api_callings.py as a separate tool in bee-agent ui.