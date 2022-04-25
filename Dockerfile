FROM python:3.9-slim

RUN apt-get -y update
RUN apt-get -y install git

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

RUN git clone https://github.com/RichardPilbery/oneoneone.git

CMD gunicorn -b 0.0.0.0:80 oneoneone.app:server
