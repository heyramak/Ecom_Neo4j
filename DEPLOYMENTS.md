# One stop medical shop
# Deployment Guide for Neo4j DB, Woocommerce-WordPress on Docker

This guide will walk you through the steps to deploy Neo4j DB and WordPress containers and configure them to communicate with each other using the wordpree-network Docker network.

## Prerequisites
- Docker installed on your system.
- Python 3.9

## Create a Docker network
Using Docker container networking, a different server running inside a container can easily be accessed by your application containers and vice-versa.
Containers attached to the same network can communicate with each other using the container name as the hostname.
We'll start by creating a custom Docker network named `wordpress-network`.

```bash
docker network create wordpress-network
```
## Deploy MariaDB Container
In this steps, we will deploy the MariaDB container using Docker

### Step 1: Pull the image from docker repository
```bash
docker pull bitnami/mariadb:latest
```
### Step 2: Create a volume for MariaDB persistence 
```bash
docker volume create --name mariadb_data
```
### Step 3: Create a MariaDB container
```bash
docker run -d --name mariadb \
  --env ALLOW_EMPTY_PASSWORD=yes \
  --env MARIADB_USER=bn_wordpress \
  --env MARIADB_PASSWORD=bitnami \
  --env MARIADB_DATABASE=bitnami_wordpress \
  --network wordpress-network \
  --volume mariadb_data:/bitnami/mariadb \
  bitnami/mariadb:latest
```
## Deploy Wordpress Container
In this steps, we will deploy the Wordpress container using Docker

### Step 1: Pull the image from docker repository
```bash
docker pull bitnami/wordpress:latest
```
### Step 2: Create a volume for Wordpress persistence 
```bash
docker volume create --name wordpress_data
```
### Step 3: Create a Wordpress container
```bash
docker run -d --name wordpress \
  -p 8080:8080 -p 8443:8443 \
  --env ALLOW_EMPTY_PASSWORD=yes \
  --env WORDPRESS_DATABASE_USER=bn_wordpress \
  --env WORDPRESS_DATABASE_PASSWORD=bitnami \
  --env WORDPRESS_DATABASE_NAME=bitnami_wordpress \
  --network wordpress-network \
  --volume wordpress_data:/bitnami/wordpress \
  bitnami/wordpress:latest
```

### User and Site default configuration
- APACHE_HTTP_PORT_NUMBER: Port used by Apache for HTTP. Default: 8080
- APACHE_HTTPS_PORT_NUMBER: Port used by Apache for HTTPS. Default: 8443
- WORDPRESS_USERNAME: WordPress application username. Default: user
- WORDPRESS_PASSWORD: WordPress application password. Default: bitnami
- WORDPRESS_EMAIL: WordPress application email. Default: user@example.com
  
## Neo4j Docker Deployment
In this steps, we will deploy the Neo4j container using Docker
### Step 1: Pull the Bitnami Neo4j Docker Image
```
bash
docker pull bitnami/neo4j:latest
```

### Step 2: Create a Docker volume for Neo4j data
```
bash
docker volume create neo4j_data
```

### Step 3: Deploy Bitnami Neo4j Container
```
bash

docker run -d \
  --name neo4j \
  -p 7474:7474 \
  -p 7687:7687 \
  -v neo4j_data:/bitnami/neo4j/data \
  --network wordpress-network\
  bitnami/neo4j:latest
```