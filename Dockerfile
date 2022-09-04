FROM python:3.10-slim-buster

RUN apt update \
  && pip3 install pip wheel poetry --upgrade 

COPY ./ /src
WORKDIR /src
RUN mode=0755,target=/root/.cache/pip pip3 install .

COPY /data /data
COPY entrypoint.sh /
RUN chmod 755 entrypoint.sh

RUN rm -rf /src
WORKDIR /

CMD ["bash", "entrypoint.sh"]
