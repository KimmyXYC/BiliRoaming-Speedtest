FROM python:3.11
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install ttf-wqy-zenhei && fc-cache -f -v && apt-get install -y wkhtmltopdf && pip install --upgrade --no-cache-dir pip && pip install --no-cache-dir -r requirements.txt
CMD ["python", "docker_main.py"]
