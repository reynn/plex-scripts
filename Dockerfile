FROM alpine:3.6

COPY requirements.txt /app/requirements.txt

RUN apk add --update --no-cache \
        python3 \
    && pip3 install -r /app/requirements.txt

COPY . /app

ENTRYPOINT ["/usr/bin/python3", "/app/plex_data_collector.py"]