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

# Install the runtime interface client
RUN pip install \
        --target ${FUNCTION_DIR} \
        awslambdaric

# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Install Tesseract-OCR and all dependencies for tesserocr
RUN apt-get install -y tesseract-ocr
RUN apt-get install -y libtesseract-dev
RUN apt-get install -y libleptonica-dev
RUN apt-get install -y pkg-config
RUN apt-get install -y build-essential

RUN pip3 install -r ${FUNCTION_DIR}/requirements.txt

ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "app.lambda_handler" ]