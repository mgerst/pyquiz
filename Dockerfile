FROM python:3
ENV PYTHONUNBUFFERED 1
ENV JEOPARDY_ENV docker

RUN mkdir /code
WORKDIR /code

# Install nodejs
RUN curl -sL https://deb.nodesource.com/setup_9.x | bash -
RUN DEBIAN_FRONTEND=noninteractive apt-get install -yqq nodejs

# Setup python dependencies
ADD requirements.txt /code/
RUN pip install -r requirements.txt

# Setup node dependencies
ADD package.json /code/
RUN npm install

ADD . /code/

RUN npm run build
