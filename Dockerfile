FROM python:3.10.4-buster

RUN apt-get update
RUN apt-get install build-essential
WORKDIR /code/
COPY . .
CMD ["/bin/bash","/code/build_run.sh"]