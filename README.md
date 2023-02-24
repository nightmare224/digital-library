# Digital Library

## Introduction
[Digital Library](https://github.com/nightmare224/digital-library) is an implemntaion of [How to protect reader lending privacy under a cloud environment: a technical method](https://www.emerald.com/insight/content/doi/10.1108/LHT-07-2020-0178/full/html) paper. 

This repo use RESTful APIs with Python Flask framework and PostgreSQL Database to implement the mechanism proposed in paper.

## Feature
### System Model
There are three components in paper's system model (Figure 1) which is **Server** (Cloud Server), **Client**(Lending Interface, Query Interface), and **User**(Reader, Worker, Administrator). In this implementation, I create one Flask web application to represent Server, one Flask web application to represent Client, and both of them have Swagger pages for Users to intract with their APIs.
<img src="https://github.com/nightmare224/digital-library/blob/master/docs/images/system-model.png" alt="system-model"/>


## Quick Started
### Prerequisite
