
FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir chainlit openai

EXPOSE 80

CMD ["chainlit", "run", "main.py", "--host", "0.0.0.0", "--port", "8080"]