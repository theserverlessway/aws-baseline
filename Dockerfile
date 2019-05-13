FROM flomotlik/awsinfo:latest

RUN apk add --no-cache --update build-base gcc libffi-dev openssl-dev openssl musl-dev python-dev git

RUN git clone https://github.com/toniblyx/prowler.git /prowler

WORKDIR /app

RUN ln -s /prowler/prowler /usr/local/bin/prowler

COPY requirements.txt requirements.txt
RUN pip install -U -r requirements.txt

RUN mkdir -p /etc/bash_completion.d

RUN activate-global-python-argcomplete
RUN  echo 'eval "$(register-python-argcomplete formica)"' >> /root/.bashrc

ENTRYPOINT []