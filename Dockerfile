FROM python:3.6

WORKDIR /app

RUN apt-get update -y -qq
RUN apt-get install -y -qq groff pandoc

COPY requirements.txt requirements.txt
RUN pip install -U -r requirements.txt
RUN activate-global-python-argcomplete
RUN  echo 'eval "$(register-python-argcomplete formica)"' >> /root/.bashrc
