# SSLCertificationPython
Basic Starter Tutorial on Bee-agent to do devops tasks using Agentic AI like deploying an application, checking and renewing the ssl certificate expiry of the same application.

# SSL-Agent 

### This Repo contains a Basic application (ApplicationDemo) which will be deployed, renew it's ssl certificate and check the certificate expiry using Agentic AI in Bee-Agent.<br> It also has another repo which has custom tools for Bee-Agent.<br> The tools can be found in the folder ApplicationUtilities.

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