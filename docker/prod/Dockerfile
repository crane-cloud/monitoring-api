# use an official python runtime as the base image
FROM python:3.10

# set the (container) working directory
WORKDIR /app


# install netcat
RUN apt-get update && \
    apt-get install netcat-traditional -y

COPY requirements.txt /app/requirements.txt


# install dependencies
RUN pip install -r requirements.txt

# copy current (local) directory contents into the container
COPY . /app


# make port available to the world outside this container
EXPOSE 5000

# connect to start script when db is being used
ENTRYPOINT ["sh", "/app/scripts/start-prod.sh"]
