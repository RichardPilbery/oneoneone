FROM python:3.9-slim

RUN apt-get -y update
RUN apt-get -y install git
RUN git clone https://github.com/RichardPilbery/oneoneone.git

RUN mv ./oneoneone/* ./*

RUN pip install -r ./requirements.txt

CMD gunicorn -b 0.0.0.0:80 oneoneone.app:server
