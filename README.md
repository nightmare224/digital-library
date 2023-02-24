# Digital Library

## Introduction
[Digital Library](https://github.com/nightmare224/digital-library) is an implemntaion of [How to protect reader lending privacy under a cloud environment: a technical method](https://www.emerald.com/insight/content/doi/10.1108/LHT-07-2020-0178/full/html) paper. 

There are four components in paper's system model (Figure 1) which is _**Database**_(Cloud Database), _**Server**_ (Cloud Server), _**Client**_(Lending Interface, Query Interface), and _**User**_ (Reader, Worker, Administrator). 
<img src="https://github.com/nightmare224/digital-library/blob/master/docs/images/system-model.png" alt="system-model"/>
In this implementation, I choose PostgreSQL as the _Database_, which store all the data including reader information, literature information, and lending records. _Server_ is a Flask web application which in charge of making query in Database, and only Administrator could access Server's APIs. _Client_ is also a Flask web application which make HTTP requests to _Server_. It is an interface for unprivileged _User_ such as _Reader_ and _Worker_ to make query requests to _Database_. Both of _Server_ and _Client_ have Swagger pages for User to intract with their APIs.

## Quick Started
### Prerequisite

## Feature
### System Model



## Quick Started
### Prerequisite
