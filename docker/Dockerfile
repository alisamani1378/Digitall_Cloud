FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# If you prefer not to mount the bot folder, you can uncomment this line:
# COPY bot/ bot/

CMD ["python", "bot/main.py"]
