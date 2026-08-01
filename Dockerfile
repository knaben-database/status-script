FROM python:3.12-alpine

WORKDIR /app
COPY . .

# The script will write to /shared-data/status.json
# We'll mount a volume at /shared-data in Kubernetes
CMD ["sh", "-c", "while true; do python main.py; sleep 600; done"]
