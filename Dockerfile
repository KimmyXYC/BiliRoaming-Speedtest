FROM python:3.11-slim
WORKDIR /app
RUN apt-get update -y && \
apt-get install ttf-wqy-zenhei -y --no-install-recommends && \
fc-cache -f -v && \
apt-get install wkhtmltopdf -y --no-install-recommends && \
rm -rf /var/lib/apt/lists/*
COPY . /app
RUN pip install --upgrade --no-cache-dir pip && \
pip install --no-cache-dir -r requirements.txt
CMD ["python", "docker_main.py"]
