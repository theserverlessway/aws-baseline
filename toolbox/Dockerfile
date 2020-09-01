FROM toniblyx/prowler:latest as prowler

FROM theserverlessway/awsinfo:latest

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -U -r requirements.txt

RUN mkdir -p /etc/bash_completion.d

RUN awsinfo complete > /root/.awsinfo_completion

RUN activate-global-python-argcomplete
COPY bashrc /root/.bashrc

COPY --from=prowler /prowler /prowler
ENV PATH="/prowler:${PATH}"

ENV PS1='\[\e[0;32m\]\w \[\e[0;32m\]→\[\e[39m\] '

ENTRYPOINT []