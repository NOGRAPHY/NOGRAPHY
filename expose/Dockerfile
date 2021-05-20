FROM public.ecr.aws/lambda/python:3.8

# copy application code to container
COPY app.py requirements.txt ./ocr ./

# Installs development tools (gcc compiler is needed)
RUN yum groups mark convert
RUN yum group install "Development Tools" -y

# install tesseract
RUN rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
RUN yum -y update
RUN yum -y install tesseract leptonica-devel

# install python dependencies
# TODO: "fatal error: tesseract/publictypes.h: No such file or directory"
RUN python3.8 -m pip install -r requirements.txt -t .

# TODO install poppler?

# set handler as command
CMD ["app.lambda_handler"]
