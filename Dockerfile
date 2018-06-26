FROM python:3.5

# add requirements.txt to the image
ADD requirements.pip requirements.pip

ADD . /app
# set working directory to /app/
WORKDIR /app/

# install python dependencies
RUN pip install -r requirements.pip
