# Digital Library

## Introduction
[Digital Library](https://github.com/nightmare224/digital-library) is an implemntaion of [How to protect reader lending privacy under a cloud environment: a technical method](https://www.emerald.com/insight/content/doi/10.1108/LHT-07-2020-0178/full/html) paper. 

There are four components in paper's system model (Figure 1) which is _**Database**_(Cloud Database), _**Server**_ (Cloud Server), _**Client**_(Lending Interface, Query Interface), and _**User**_ (Reader, Worker, Administrator). 
<img src="https://github.com/nightmare224/digital-library/blob/master/docs/images/system-model.png" alt="system-model"/>
In this implementation, I choose **PostgreSQL** as the _**Database**_, which store all the data including reader information, literature information, and lending records. _**Server**_ is a **Flask web application** which in charge of making queries in Database, and only Administrator could access Server's APIs. _**Client**_ is also a **Flask web application** which make HTTP requests to _Server_. It is an interface for unprivileged _User_ such as _Reader_ and _Worker_ to make queries through _Server_ in _Database_. Both _Server_ and _Client_ have Swagger pages for _User_ to intract with their APIs.

## Quick Started
The following steps would create three docker containers to represent ***Server***, ***Client***, and ***Database***.
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

To demostrate the scenario in paper easily, some demo data are inserted in database beforehand. You can play with those data through ***Server* and *Client* APIs**.

- See and interact with **_Server_ APIs** on **[http://127.0.0.1:5001/apidocs/](http://127.0.0.1:5001/apidocs/)**

  <img src="https://github.com/nightmare224/digital-library/blob/master/docs/images/swagger-server.png" alt="system-model"/>

- See and interact wich ***Client* APIs** on **[http://127.0.0.1:5002/apidocs/](http://127.0.0.1:5002/apidocs/)**

  <img src="https://github.com/nightmare224/digital-library/blob/master/docs/images/swagger-client.png" alt="system-model"/>



## Demostration

This section would demostrate some scenario that mentioned in paper, and also explain how it works behind the scenes.

### Scenario1

<pre style="text-align: center;">Reader(ID: 2019IN013) lends the literature(ID: 1)</pre>

Send HTTP `POST` request to *Client* API `/digitallibrary/client/api/reader/{rid}/record` to create record.

<img src="https://github.com/nightmare224/digital-library/blob/master/docs/images/scenario1-1.png" alt="scenario1-1"/>

#### How it works

1. Reader send `POST` request to *Client* API `/digitallibrary/client/api/reader/{rid}/record` with **original reader number** (rid) *2019IN013* and **literature number** (bid) *1*.

2. Inside the *Client*, it would do query transformation, which would generate **ciphertext** (rtt) and **featured reader number**(rid) based on the feature construction process shown in Figure3. The ciphertext is completed by AES encryption and Base64 encode, i.e. `Base64Encode(AES(lending time + original reader number))`

   <img src="https://github.com/nightmare224/digital-library/blob/master/docs/images/feature-construction.png" alt="feature-construction"/>

3. *Client* sends the `POST` request to *Server* API `/digitallibrary/client/api/reader/{rid}/record` with **featured reader number ** (rid)  *7PBC52BAB* and the **ciphertext field** (rtt) *NPTnTn/sj8R4zuGsBW22ezjgV5DD*

   <img src="https://github.com/nightmare224/digital-library/blob/master/docs/images/scenario1-2.png" alt="scenario1-2"/>

4. *Server* would insert this record into *Database*

### Scenario2

<pre style="text-align: center;">Reader(ID: 2019IN013) get his own lending records</pre>

Send HTTP `GET` request to *Client* API  `/digitallibrary/client/api/reader/{rid}/record`  to get records.

<img src="https://github.com/nightmare224/digital-library/blob/master/docs/images/scenario2-1.png" alt="scenario2-1"/>

#### How it works

1. Send HTTP `GET` request to *Client* API  `/digitallibrary/client/api/reader/{rid}/record`  to get records with **original reader number** (rid) *2019IN013*.

2. Inside the *Client*, it send HTTP `GET` request to *Server* API `/digitallibrary/server/api/reader/{rid}/record` with **featured reader number** (rid)  *7PBC52BAB*. The response of _Server_ would be like:

   ```json
   [
     {
       "bid": "1",
       "rid": "7PBC52BAB",
       "rtt": "NPTnTn/sj8R4zuGsBW22ezjgV5DD",
       "sta": "202302251946",
       "tid": "1"
     },
     {
       "bid": "2",
       "rid": "7PBC52BAB",
       "rtt": "NPTnT3/sjsR4zuGsBW22ezjjXJDA",
       "sta": "202302252245",
       "tid": "2"
     }
   [
   ```

3. To verify whether the records belong to reader *2019IN013*, do Base64 decode and AES decrypt on ciphertext field (rtt) . This step is necessary because there is a **many-to-one** mapping from **original reader number** to featured reader number, for example, both *2019IN013* and *2018IN113* get *7PBC52BAB* after feature construction.

4. *Client* gather all the records which belong to reader *2019IN013* and then send HTTP response. The response of *Client* would be like:

   **verbose=1**

   ```json
   [
     {
       "bid": "1",
       "rid": "7PBC52BAB",
       "rtt": "NPTnTn/sj8R4zuGsBW22ezjgV5DD",
       "sta": "202302251946",
       "tid": "1",
       "tle": "Nicole Tai",
       "type": "reader"
     }
   ]
   ```

   **verbose=0**

   ```json
   [
     {
       "bid": "1",
       "rid": "7PBC52BAB",
       "rtt": "NPTnTn/sj8R4zuGsBW22ezjgV5DD",
       "sta": "202302251946",
       "tid": "1"
     }
   ]
   ```
