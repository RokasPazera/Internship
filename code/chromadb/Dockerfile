FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir chromadb==0.5.20 pypdf

COPY db.py seeding.py ./

CMD ["python", "db.py"]
