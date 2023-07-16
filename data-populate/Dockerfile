FROM python:3.9

RUN mkdir /Data Injection
WORKDIR /Data Injection

COPY . .

RUN pip install requests python-dotenv neo4j

CMD ["python3", "neo4jDB.py"]