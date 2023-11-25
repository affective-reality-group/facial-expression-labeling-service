FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=fer_labeler/app.py

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
