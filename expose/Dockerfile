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
COPY /app ${FUNCTION_DIR}/
COPY requirements.txt ${FUNCTION_DIR}
COPY tesserocr-2.3.0-cp37-cp37m-manylinux1_x86_64.whl ${FUNCTION_DIR}

# Install the runtime interface client
RUN pip install \
        --target ${FUNCTION_DIR} \
        awslambdaric

# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

RUN apt-get install -y tesseract-ocr

RUN pip install tesserocr-2.3.0-cp37-cp37m-manylinux1_x86_64.whl
RUN pip3 install -r ${FUNCTION_DIR}/requirements.txt

ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "app.lambda_handler" ]