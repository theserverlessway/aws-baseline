FROM flomotlik/awsinfo:latest

RUN apk add --no-cache --update build-base gcc libffi-dev openssl-dev openssl musl-dev python-dev git curl

RUN git clone https://github.com/toniblyx/prowler.git /prowler
ENV PATH="/prowler:${PATH}"

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -U -r requirements.txt

RUN mkdir -p /etc/bash_completion.d

RUN awsinfo complete > /root/.awsinfo_completion

RUN activate-global-python-argcomplete
COPY bashrc /root/.bashrc

ENV PS1='\[\e[0;32m\]\w \[\e[0;32m\]→\[\e[39m\] '

ENTRYPOINT []