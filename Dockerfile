FROM python:3.11-slim
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

WORKDIR /workdir

# set up the wait script
RUN apt-get update \
  && apt-get install -y netcat \
  && apt-get install -y curl \
  && apt-get install -y --no-install-recommends git \
  && apt-get purge -y --auto-remove \
  && rm -rf /var/lib/apt/lists/*

ADD https://raw.githubusercontent.com/eficode/wait-for/fd4909a3b269d05bd5fe13d0e5d2b9b1bc119323/wait-for wait-for.sh
RUN chmod u+x wait-for.sh

RUN pip install  faust-streaming==0.10.13

WORKDIR /code/app
COPY ./app .
