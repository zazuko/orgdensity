FROM python:3.9-slim

WORKDIR /app

# install dependencies
RUN apt-get update && apt-get install -y git libgdal-dev g++
RUN pip install gunicorn==20.0.4 poetry==1.1
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install

# get source code
COPY assets /home/magdalena/zazuko/notebooks/notebooks/swisstopo/assets
COPY georegister /home/magdalena/zazuko/notebooks/notebooks/swisstopo/georegister
WORKDIR /home/magdalena/zazuko/notebooks/notebooks/swisstopo/georegister

RUN mkdir -p /mpl
ENV MPLCONFIGDIR /mpl

RUN chown 65534:65534 -R /home/magdalena/zazuko/notebooks/notebooks/swisstopo /mpl

# run as "nobody"
USER 65534:65534

EXPOSE 8080

CMD ["python", \
  "-m", "gunicorn.app.wsgiapp", \
  "--bind=[::]:8080", \
  "--timeout=300", \
  "--access-logfile=-", \
  "main:server"]
