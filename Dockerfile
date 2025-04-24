FROM python:slim-bullseye

COPY . /home/

WORKDIR /home

RUN pip install -r requirements.txt

LABEL org.opencontainers.image.description="PowerPlay Assistant is a flask web app to help Elite: Dangerous commanders with PowerPlay 2.0 tasks."
LABEL org.opencontainers.image.authors="Niceygy (Ava Whale)"

# Start 
CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]