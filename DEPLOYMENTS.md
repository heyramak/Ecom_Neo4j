# One stop medical shop
# Deployment Guide for Neo4j DB, Woocommerce-WordPress on Docker

This guide will walk you through the steps to deploy Neo4j DB and WordPress containers and configure them to communicate with each other using the wordpree-network Docker network.

## Prerequisites
- Docker installed on your system.
- Docker Compose installed on your system.

## Setup

### Clone the project

Clone the repository
```bash
  git clone https://gitlab.com/heyramak/one-stop-medical-shop
```
### Deploy the Containers

- Open a terminal or command prompt and navigate to the one_stop_medical_shop directory where you created the docker-compose.yml file.
- Run the following command to deploy the containers:
```bash
docker-compose up -d
```
This will pull the necessary Docker images and start the MariaDB, WordPress, and Neo4j containers.
### Accessing the Services 
- WordPress: You can access WordPress by visiting ```http://localhost:8080``` in your web browser. The default login credentials are:
      - ```Username: user```
      - ```Password: bitnami```
- Neo4j Browser: You can access the Neo4j Browser by visiting ```http://localhost:7474``` in your web browser.
      - ```Username: neo4j```
      - ```Password: bitnami1```
  
### User and Site default configuration
For WordPress, you can configure the following environment variables in the docker-compose.yml file to customize the default setup:
- APACHE_HTTP_PORT_NUMBER: Port used by Apache for HTTP. Default: 8080
- APACHE_HTTPS_PORT_NUMBER: Port used by Apache for HTTPS. Default: 8443
- WORDPRESS_USERNAME: WordPress application username. Default: user
- WORDPRESS_PASSWORD: WordPress application password. Default: bitnami
- WORDPRESS_EMAIL: WordPress application email. Default: user@example.com
