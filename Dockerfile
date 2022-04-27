FROM python:3.9-slim

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update
RUN apt-get -y install git
RUN git clone https://github.com/RichardPilbery/oneoneone.git

RUN apt-get -y install nano
RUN apt-get -y install gcc python3-dev

RUN cp -a oneoneone/. . && rm -r oneoneone

RUN pip install -r ./requirements.txt

CMD gunicorn -b 0.0.0.0:80 index:server
