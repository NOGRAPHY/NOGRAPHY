# Define function directory
ARG FUNCTION_DIR="/function"

#FROM python:3.7-buster as build-image
FROM python:3.7-buster

# Install aws-lambda-cpp build dependencies
RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev

# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Create function directory
RUN mkdir -p ${FUNCTION_DIR}

# Copy function code
COPY app.py ${FUNCTION_DIR}
COPY ocr/* ${FUNCTION_DIR}/
COPY requirements.txt ${FUNCTION_DIR}

# Install the runtime interface client
RUN pip install \
        --target ${FUNCTION_DIR} \
        awslambdaric

# Multi-stage build: grab a fresh copy of the base image
# FROM python:3.7-buster

# Include global arg in this stage of the build
# ARG FUNCTION_DIR
# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Copy in the build image dependencies
# COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

RUN pip3 install -r ${FUNCTION_DIR}/requirements.txt

ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "app.handler" ]