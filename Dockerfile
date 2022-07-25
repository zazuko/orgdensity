FROM python:3.9-slim

WORKDIR /app

# install dependencies
RUN apt-get update && apt-get install -y git
# libgdal-dev g++
RUN pip install poetry==1.1
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install

# get source code
COPY orgdensity /app/orgdensity
WORKDIR /app/orgdensity

RUN mkdir -p /mpl
ENV MPLCONFIGDIR /mpl

RUN chown 65534:65534 -R /app /mpl

# run as "nobody"
USER 65534:65534

EXPOSE 8050

CMD ["python", "main.py"]
