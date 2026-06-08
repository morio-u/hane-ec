# Production-Focused EC Application (Work in Progress)

This repository contains a personal project to build an e-commerce
application using Python and FastAPI, with a strong focus on
production readiness and operational considerations.

The goal of this project is not only to implement application features,
but also to progressively incorporate infrastructure, deployment,
and operational best practices commonly required in real production environments.

## Current Status

* Core EC application implemented (API + admin functionality)
* Local development environment using Docker
* Database schema management with Alembic
* AWS infrastructure configured (VPC, Subnets, Route Tables, Security Groups, EC2)
* Application deployed to Amazon EC2
* Nginx configured as a web server
* Live demo environment available for testing

## Planned (In Progress)

* Amazon RDS integration
* Reverse proxy and service management improvements
* CI/CD pipeline integration
* Automated testing
* Production deployment and operational validation

## Technology Stack

* Backend: Python, FastAPI
* Templating: Jinja2
* Database: PostgreSQL
* Infrastructure: AWS (VPC, EC2, Security Groups)
* Web Server: Nginx
* Containerization: Docker
* Migration: Alembic
* Version Control: GitHub

## Notes

* This project is currently under active development.
* The live environment is intended for learning and demonstration purposes.
* All configurations, data, and examples are non-production and for demonstration purposes only.
* No proprietary or confidential information is included.

## Purpose

This project serves as a learning and demonstration platform to show how
application development can evolve toward production-ready and
operationally sustainable systems.
