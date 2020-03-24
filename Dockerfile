FROM python:3.8-alpine

WORKDIR /xstreamly

ADD . /xstreamly

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "--workers", "1", "--bind", "0.0.0.0:8000", "xstreamly:app"]
