FROM python:3.8-slim

RUN mkdir /app
WORKDIR /app

RUN useradd -m nonroot
USER nonroot

ENV PATH $PATH:/home/nonroot/.local/bin

COPY requirements.txt .

RUN pip install --user -r requirements.txt

COPY downloader.py .
CMD ["python", "downloader.py"]
