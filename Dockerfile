FROM python:3.12-alpine

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
CMD ["sh", "-c", "while true; do python main.py; sleep 600; done"]
