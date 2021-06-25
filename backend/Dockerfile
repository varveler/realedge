FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    python3.8 \
    python3-pip \
    python3.8-dev \
    git \
    nano \
    wget

ENV PYTHONUNBUFFERED 1
WORKDIR /backend

#RUN adduser --disabled-password --gecos '' tasksuser
ADD wait-for-it.sh /backend/
RUN chmod +x /backend/wait-for-it.sh

#RUN apt-get install -yqq wget

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/91.0.4472.101/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

#RUN apt-get install -yqq python-setuptools python-dev build-essential
#RUN apt-get install -yqq python-pip

COPY requirements.txt /backend
RUN pip3 install -r requirements.txt

#RUN mkdir -p /home/varveler
#RUN adduser --disabled-password --gecos '' varveler
#RUN chown varveler /usr/local/bin/

RUN apt-get clean && apt-get update && apt-get install -y locales
RUN locale-gen en_CA.UTF-8
COPY ./default_locale /etc/default/locale
RUN chmod 0755 /etc/default/locale
ENV LC_ALL=en_CA.UTF-8
ENV LANG=en_CA.UTF-8
ENV LANGUAGE=en_CA.UTF-8


COPY . /backend/

RUN chmod -R 777 /backend/tempOrdersFiles

#RUN chown varveler /home/varveler
#USER varveler
#ENV HOME /home/varveler
