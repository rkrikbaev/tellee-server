#flowserver configuration

FROM python:3.7

# enable utf-8 locale
ENV PYTHONUNBUFFERED 1

#create folder for the service
RUN mkdir /service
WORKDIR /service

#COPY ./install_modules_py_agent.sh /tmp
#RUN sh /tmp/install_modules_py_agent.sh

# add core script
ADD ./agent/agent.py /service/app/agent.py
COPY ./agent/images /service/images
ADD  ./agent/abylay_rsa /service/app

RUN curl -O https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py && \
    rm get-pip.py

COPY ./requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

RUN chmod +x /service/app/agent.py

ENTRYPOINT ["python3", "./app.py"]
