FROM python:3.9-slim

RUN apt-get -y update
RUN apt-get -y install git

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . ./

RUN git clone https://github.com/RichardPilbery/oneoneone.git

EXPOSE 8050
