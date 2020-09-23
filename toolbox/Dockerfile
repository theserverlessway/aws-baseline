FROM theserverlessway/awsinfo:latest

RUN apt-get install -y build-essential gcc libffi-dev libssl-dev openssl musl-dev git curl

RUN git clone https://github.com/toniblyx/prowler.git /prowler
ENV PATH="/prowler:${PATH}"

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -U -r requirements.txt
RUN pip3 install scoutsuite

RUN mkdir -p /etc/bash_completion.d

RUN awsinfo complete > /root/.awsinfo_completion

RUN activate-global-python-argcomplete
COPY bashrc /root/.bashrc

ENV PS1='\[\e[0;32m\]\w \[\e[0;32m\]→\[\e[39m\] '

ENTRYPOINT []