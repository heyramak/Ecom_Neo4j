from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("BOLT_URI")
username = os.getenv("BOLT_USERNAME")
password = os.getenv("BOLT_PASSWORD")
driver = GraphDatabase.driver(uri, auth=(username, password))

cypher_query = """
WITH 'https://raw.githubusercontent.com/heyramak/neo4j-trail/main/products_sample_01.json' AS url 
CALL apoc.load.json(url) YIELD value AS products

UNWIND products AS product

MERGE (p:Product {id: product._id})
SET p.page_title = product.page_title

FOREACH (feature IN product.`product-features` |
  MERGE (pf:ProductFeature {name: feature})
  MERGE (p)-[:HAS_FEATURE]->(pf)
)

MERGE (spec:Specification {product_id: product._id})
SET spec += product.specifications
MERGE (p)-[:HAS_SPECIFICATION]->(spec)

MERGE (s:Schema {product_id: product._id})
SET s += {image: product.schema.image, description: product.schema.description}
MERGE (p)-[:HAS_SCHEMA]->(s)

MERGE (m:Manufacturer {name: product.specifications.Manufacturer})
MERGE (p)-[:MANUFACTURED_BY]->(m)

MERGE (cg:ProductGroup {id: product.categoryId})
MERGE (p)-[:BELONGS_TO_GROUP]->(cg)

FOREACH (brandName IN CASE WHEN product.specifications.Brand IS NULL THEN ['Unknown'] ELSE [product.specifications.Brand] END |
  MERGE (b:Brand {name: brandName})
  MERGE (p)-[:BELONGS_TO_BRAND]->(b))
"""
with driver.session() as session:
    result = session.run(cypher_query)