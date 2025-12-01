# FROM astrocrpublic.azurecr.io/runtime:3.1-2

FROM quay.io/astronomer/astro-runtime:12.6.0

# Install required system tools
USER root
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*
USER astro

# Add psycopg2-binary before everything else AND block psycopg2
RUN pip install "psycopg2-binary>=2.9" && pip install --no-binary=:all: --only-binary psycopg2-binary apache-airflow-providers-google