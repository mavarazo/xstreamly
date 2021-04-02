FROM python:3.9.2-slim-buster

RUN apt-get update \
  && apt-get install -y build-essential curl --no-install-recommends \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean 

ENV FLASK_APP="xstreamly" \
    FLASK_SKIP_DOTENV="true" \
    PYTHONUNBUFFERED="true" \
    PYTHONPATH="."

WORKDIR /xstreamly

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

ENV DATABASE_URL=sqlite:////config/xstreamly.db

EXPOSE 8000

VOLUME /config

RUN flask db upgrade

CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:8000", "xstreamly:app"]
