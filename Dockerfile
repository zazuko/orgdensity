FROM python:3.9-slim

WORKDIR /app

# install dependencies
RUN apt-get update && apt-get install -y git libgdal-dev g++
RUN pip install gunicorn==20.0.4 poetry==1.1
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install

# get source code
COPY assets /app/orgdensity/assets
RUN ln -s /app/orgdensity/assets /app/assets
COPY orgdensity /app/orgdensity
WORKDIR /app

RUN mkdir -p /mpl
ENV MPLCONFIGDIR /mpl

RUN chown 65534:65534 -R /app /mpl

# run as "nobody"
USER 65534:65534

EXPOSE 8080

CMD ["python", \
  "-m", "gunicorn.app.wsgiapp", \
  "--bind=[::]:8080", \
  "--timeout=300", \
  "--access-logfile=-", \
  "--chdir=/app/orgdensity", \
  "main:server"]
