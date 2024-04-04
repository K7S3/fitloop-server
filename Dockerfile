# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.2
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "$(pwd)" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Define environment variable
ENV CSV_DIRECTORY=/app/nutrition_info

# Create a directory to store CSV files
RUN mkdir -p $CSV_DIRECTORY

# Change the ownership of the /app directory to appuser
RUN chown -R appuser:appuser /app

# Switch to the non-privileged user to run the application.
USER appuser

# Define the volume for CSV_DIRECTORY
VOLUME $CSV_DIRECTORY

# Set PYTHONUSERBASE for pip to install packages to a directory that appuser has write access to
ENV PYTHONUSERBASE=/app

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install --user -r requirements.txt

COPY . .

EXPOSE 8000

CMD python app.py