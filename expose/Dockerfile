FROM ubuntu:latest 
FROM python:3.7

RUN apt-get update -y
#RUN apt-get install -y  python3.7 python3-pip
RUN apt update && apt install -y libsm6 libxext6
RUN DEBIAN_FRONTEND='noninteractive' apt-get -y install tesseract-ocr 

RUN pip install pillow
RUN pip install pytesseract
RUN pip install opencv-contrib-python

# copy application code to container
COPY app.py tesserocr-2.3.0-cp37-cp37m-manylinux1_x86_64.whl requirements.txt ./ocr ./ 

# Installs development tools (gcc compiler is needed)
#RUN yum groups mark convert
#RUN yum group install "Development Tools" -y

# install tesseract
#RUN rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
#RUN yum clean all
#RUN yum -y update
#RUN yum install tesseract -y 

# install python dependencies
# TODO: "fatal error: tesseract/publictypes.h: No such file or directory"
#RUN yum -y install libleptonica-dev libtesseract-dev
RUN pip install tesserocr-2.3.0-cp37-cp37m-manylinux1_x86_64.whl
RUN python3.7 -m pip install -r requirements.txt -t .

# TODO install poppler?

ENTRYPOINT ["python"]

# set handler as command
CMD ["app.lambda_handler"]
