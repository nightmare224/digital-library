FROM ubuntu:20.04

### Update and install packages
RUN apt update
RUN apt install curl -y
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN apt install python3-dev python3-pip -y
RUN apt install libpq-dev -y
RUN apt install libpq-dev unzip -y

### Args define
ARG WORKDIR_PATH
ARG SRCCODE_PATH
ARG SERVICE_PORT
ARG START_APP_FILE

### Specify work dir
WORKDIR ${WORKDIR_PATH}

### Copy and unpack local file to image
COPY ${SRCCODE_PATH} /${WORKDIR_PATH}/${SRCCODE_PATH}

## Install python packages
RUN pip3 install -r ${SRCCODE_PATH}/requirements.txt

### Service port number
EXPOSE ${SERVICE_PORT}

### Run command
ENV COMMAND=${SRCCODE_PATH}/run.sh
CMD bash ${COMMAND}