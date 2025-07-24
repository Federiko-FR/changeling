FROM ubuntu:24.04
ARG BRANCH
RUN apt -q -y update \
 && apt install curl -y \
 && curl -fsSL -o /usr/local/bin/dbmate https://github.com/amacneil/dbmate/releases/download/v1.16.2/dbmate-linux-amd64 \
 && chmod +x /usr/local/bin/dbmate \
 && apt -q -y clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY ./docker/migrations/run.sh /code/run.sh
RUN chmod +x /code/run.sh

WORKDIR /code

COPY ./db/migrations /code/migrations

CMD /code/run.sh
