FROM python:3.8

COPY requirements.txt /adaptor/

RUN pip3 install --upgrade pip
RUN pip3 install -r /adaptor/requirements.txt
RUN apt-get update && apt-get install -y netcat

COPY main_adaptor.py start_adaptor.sh /adaptor/
WORKDIR /adaptor

RUN chmod +x start_adaptor.sh

CMD ["./start_adaptor.sh"]
