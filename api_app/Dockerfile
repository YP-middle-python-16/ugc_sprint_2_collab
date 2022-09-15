FROM python:3.10-slim

ENV APP_HOME=/home/app

# set work directory
WORKDIR $APP_HOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "$APP_HOME"

RUN pip install --upgrade pip

RUN addgroup --system app && adduser --system --no-create-home --group app
RUN chown -R app:app /home/app && chmod -R 755 /home/app
USER app

WORKDIR /home/app
COPY --chown=app:app ./requirements.txt requirements.txt
RUN pip install --user -r requirements.txt

ENV PATH="/home/app/.local/bin:${PATH}"

COPY --chown=app:app ./src .
COPY --chown=app:app ./tests tests
RUN ls
