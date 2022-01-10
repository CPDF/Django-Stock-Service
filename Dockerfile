# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.9

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# Set the working directory to /api_service
WORKDIR /django_challenge-main/
COPY requirements.txt /django_challenge-main/
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /api_service
ADD . /api_service/

