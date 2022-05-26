FROM python:latest

WORKDIR /usr/app/src

COPY . ./

ENTRYPOINT [ "python", "jacksaver.py"]