FROM python:3.10-slim-buster
WORKDIR /SERVICE
ARG SERVICE
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./$SERVICE .
CMD ["python3", "-u" ,"app.py"]