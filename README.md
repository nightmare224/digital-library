# Digital Library

## Introduction
[Digital Library](https://github.com/nightmare224/digital-library) is an implemntaion of [How to protect reader lending privacy under a cloud environment: a technical method](https://www.emerald.com/insight/content/doi/10.1108/LHT-07-2020-0178/full/html) paper. 

There are four components in paper's system model (Figure 1) which is _**Database**_(Cloud Database), _**Server**_ (Cloud Server), _**Client**_(Lending Interface, Query Interface), and _**User**_ (Reader, Worker, Administrator). 
<img src="https://github.com/nightmare224/digital-library/blob/master/docs/images/system-model.png" alt="system-model"/>
In this implementation, I choose **PostgreSQL** as the _**Database**_, which store all the data including reader information, literature information, and lending records. _**Server**_ is a **Flask web application** which in charge of making queries in Database, and only Administrator could access Server's APIs. _**Client**_ is also a **Flask web application** which make HTTP requests to _Server_. It is an interface for unprivileged _User_ such as _Reader_ and _Worker_ to make queries through _Server_ in _Database_. Both _Server_ and _Client_ have Swagger pages for _User_ to intract with their APIs.

## Quick Started
The follow steps would create three docker containers to represent ***Server***, ***Client***, and ***Database***.
### Prerequisite
1. **Install Docker engine and Docker compose**
    > The easiest way is to install [Docker Desktop](https://docs.docker.com/desktop/install/mac-install/), which includes Docker Compose along with Docker Engine and Docker CLI.

### Install
To install Digital Library, follow the below steps:
1. **Clone the Anime Reminder repository**
    ```bash
    git clone https://github.com/nightmare224/digital-library.git
    ```
2. **Deploy and run Digital Library**
    
    ```bash
    bash digital-library/deploy/run.sh
    ```

### Usage

**Note**: To demostrate the scenario in paper easily, some demo data are inserted in database beforehand.

- See and interact with **_Server_** APIs on **[https://127.0.0.1:5001/apidocs/](https://127.0.0.1:5001/apidocs/)**

  <img src="https://github.com/nightmare224/digital-library/blob/master/docs/images/swagger-server.png" alt="system-model"/>

- See and interact wich ***Client*** APIs on **[https://127.0.0.1:5002/apidocs/](https://127.0.0.1:5002/apidocs/)**

  <img src="https://github.com/nightmare224/digital-library/blob/master/docs/images/swagger-client.png" alt="system-model"/>





