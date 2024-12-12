FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ENTRYPOINT ["python", "main.py"]
# ENTRYPOINT ["pytest", "--verbose", "tests/"]
# CMD ["python", "main.py", "--project-path", "/app/project"]
