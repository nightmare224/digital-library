#!/bin/bash

ABSPATH=`readlink -f $0`
DIRPATH=`dirname $ABSPATH`
cd ${DIRPATH}

### Load conf/config.ini configuration file ###
source <(grep = config.ini)

## log levels: DEBUG,INFO,WARN,ERROR,FATAL ##
function log() {
  timestamp=`date "+%Y-%m-%d %H:%M:%S"`
  echo "[${USER}][${timestamp}][${1}]: ${2}"
}

main() {
  
  log "INFO" "### Build ${IMAGE_NAME} Image ###"

  ## Docker login
  docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD}
  ret_val=$?
  if [[ ${ret_val} != 0 ]]; then
    log "ERROR" "Failed to login to docker user ${DOCKER_USERNAME}"
    exit 2
  fi

  docker buildx build -t "${BUILD_IMAGE_NAME}":"${BUILD_IMAGE_TAG}" \
    --platform ${PLATFORM} \
    --push -t ${BUILD_IMAGE_NAME}:${BUILD_IMAGE_TAG} \
    --no-cache=${BUILD_NO_CACHE} \
    --build-arg WORKDIR_PATH="${WORKDIR_PATH}" \
    --build-arg SRCCODE_PATH="${SRCCODE_PATH}" \
    --build-arg SERVICE_PORT="${SERVICE_PORT}" .
	 
  ret_val=$?
  if [[ ${ret_val} != 0 ]]; then
    log "ERROR" "Failed to build ${BUILD_IMAGE_NAME}:${BUILD_IMAGE_TAG} image"
    exit 1
  fi

}

main "$@"

