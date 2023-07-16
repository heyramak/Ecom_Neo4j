FROM python:3.9

RUN mkdir /Backend
WORKDIR /Backend

COPY . .

RUN pip install requests beautifulsoup4 python-dotenv woocommerce neo4j

CMD ["python3", "main.py"]