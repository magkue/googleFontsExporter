FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ENV FETCHING_INTERVAL_SECONDS 10
ENV EXPORTER_PORT 9877

RUN playwright install
RUN playwright install-deps
CMD [ "python3", "./exporter.py"]
