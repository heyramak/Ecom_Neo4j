import random
from woocommerce import API
from neo4j import GraphDatabase
import requests
import random
import string
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

# Establish a connection to the Neo4j database
uri = os.getenv("BOLT_URI")
username = os.getenv("BOLT_USERNAME")
password = os.getenv("BOLT_PASSWORD")
driver = GraphDatabase.driver(uri, auth=(username, password))

# WooCommerce API credentials
wc_url = os.getenv("WC_URL")
wc_consumer_key = os.getenv("WC_CONSUMER_KEY")
wc_consumer_secret = os.getenv("WC_CONSUMER")

# WooCommerce API instance
wcapi = API(
    url=wc_url,
    consumer_key=wc_consumer_key,
    consumer_secret=wc_consumer_secret,
    wp_api=True,
    version="wc/v3"
)

#Category Mapping
def map_category_id(category_id):
    
    category_mapping = {
        7162: 16,
        38628: 17,
        353765: 18,
        37475: 19,
        1537374: 20,
        25972406: 21,
        1001221: 22,
        1412952: 23,
        37472: 24
    }

    # get() method of the dictionary to retrieve the new category ID
    new_category_id = category_mapping.get(category_id, 15)
    return new_category_id

#Product SKU Generator
def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choices(characters, k=length))
    return random_string.upper()

"""def get_image_links(query,image):
    api_key = os.getenv("GOOGLE_API")
    search_engine_id = os.getenv("GOOGLE_SEARCH_ID")


    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&searchType=image&q={query}"
    response = requests.get(url)
    data = response.json()

    img_links = []
    img_links.append(image)

    if "items" in data:
        items = data["items"]
        for item in items:  
            img_link = item["link"]
            img_links.append(img_link)

    return img_links"""

# Define the Cypher query to retrieve product details
cypher_query = """
MATCH (p:Product)
WITH p.id AS productId, p
ORDER BY rand()
MATCH (p)-[:HAS_SCHEMA]->(s:Schema)
MATCH (p)-[:HAS_FEATURE]->(pf:ProductFeature)
MATCH (p)-[:MANUFACTURED_BY]->(m:Manufacturer)
MATCH (p)-[:HAS_SPECIFICATION]->(spec:Specification)
MATCH (p)-[:BELONGS_TO_GROUP]->(g:ProductGroup)
RETURN productId, s.image AS image, s.description AS description, m.name AS manufacturer, g.id as categoryId,
       p.page_title AS pageTitle, COLLECT(pf.name) AS productFeatures,
       {
         manufacturerNumber: spec.`Manufacturer #`,
         mckessonNumber: spec.`McKesson #`,
         unspscCode: spec.`UNSPSC Code`,
         dimensions: spec.Dimensions,
         countryoforgin: spec.`Country of Origin`,
         application: spec.Application,
         capacity: spec.Capacity,
         filtertype: spec.`Filter Type`,
         speed: spec.Speed
       } AS specifications
"""

# Execute the query and create products in WooCommerce
with driver.session() as session:
    result = session.run(cypher_query)
    for record in result:
        product_id = record["productId"]
        description = record["description"]
        manufacturer = record["manufacturer"]
        page_title = record["pageTitle"]
        product_features = record["productFeatures"]
        specifications = record["specifications"]
        category_id = record["categoryId"]
        new_category_id = map_category_id(category_id)

        # Generate a random regular price between 10 and 100
        regular_price = round(random.uniform(1000, 2500), 2)

        # Get the image links
        title = record["pageTitle"] if record["pageTitle"] is not None else ""
        description = record["description"] if record["description"] is not None else ""
        title_description = title + " " + description

        #image_links = get_image_links(title_description, record["image"])

        image_links = record["image"]
        
        # Generate unique string
        random_string = generate_random_string(10)
    

        # Prepare product data for WooCommerce
        data = {
            "sku":  random_string,
            "name": page_title,
            "type": "simple",
            "regular_price": str(regular_price),
            "description": ' '.join(product_features),
            "short_description": description,
            "categories": [
                {
                    "id": new_category_id
                }
            ],  # Set the appropriate category IDs here
            "images": [
                {"src": image_links} 
            ],
            "attributes": [
                {
                    "name": "Manufacturer Number",
                    "position": 0,
                    "visible": True,
                    "variation": False,
                    "options": [
                        specifications["manufacturerNumber"]
                    ]
                },
                {
                    "name": "UNSPSC Code",
                    "position": 0,
                    "visible": True,
                    "variation": False,
                    "options": [
                        specifications["unspscCode"]
                    ]
                },
                {
                    "name": "Application",
                    "position": 0,
                    "visible": True,
                    "variation": False,
                    "options": [
                        specifications["application"]
                    ]
                },
                {
                    "name": "McKesson Number",
                    "position": 1,
                    "visible": True,
                    "variation": False,
                    "options": [
                        specifications["mckessonNumber"]
                    ]
                },
                # Add more attributes as needed
            ]
        }

        # Create the product in WooCommerce
        response = wcapi.post("products", data)
        print("Product ID:", product_id)
        print("Response:", response.json())
        print("---")

# Close the database connection
driver.close()