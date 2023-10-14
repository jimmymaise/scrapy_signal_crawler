# scrapy_signal_crawler

## Contents

- [Overview](#overview)
- [Setup](#setup)
  - [Native Setup](#native-setup)
  - [Docker Setup](#docker-setup)
- [Usage](#usage)
- [Codebase Explanation](#codebase-explanation)
  - [Spider Modules](#spider-modules)
  - [Request Middleware](#request-middleware)
  - [Data Models](#data-models)
  - [Data Pipelines](#data-pipelines)
  - [Configurations](#configurations)
  - [Tor IP Rotator](#tor-ip-rotator)
- [Docker Deployment Guide](#docker-deployment-guide)
- [How to Contribute](#how-to-contribute)
- [Licensing](#licensing)

---

## Overview

Welcome to `scrapy_signal_crawler`, your one-stop solution for gathering trading signals from diverse platforms. Experience features such as IP rotation, data serialization, and a modular pipeline designed for efficient data harvesting and management.

---

## Setup

### Native Setup

1. **Repository Clone**: Get the repository on your local system.
2. **Project Directory**: Use the `cd` command to move into the project folder.
3. **Dependency Installation**: Run `pip install -r requirements.txt` to set up the required Python packages.
4. **Spider Execution**: To start a Scrapy spider, use `scrapy crawl <SPIDER_NAME>`.

### Docker Setup

1. **Docker Image Creation**: 
    ```bash
    docker build . -t bot_runner
    ```
2. **Docker Container Launch**: 
    ```bash
    docker run --net="host" --log-opt max-size=10m --log-opt max-file=3 -e CONTROLLER_BASE_URL="http://40.78.1.149:8000" -d bot_runner --runner-name zulu_runner_ubuntu_server --bot-type zulu_api
    docker run --net="host" --log-opt max-size=10m --log-opt max-file=3 -e CONTROLLER_BASE_URL="http://40.78.1.149:8000" -d bot_runner --runner-name exness_runner_ubuntu_server --bot-type exness_api --tor
    ```
    > **Note**: Include `--tor` to use Tor.

---

## Codebase Explanation

### Spider Modules

Different trading signal source spiders are in the `spiders/` directory. They are derived from the `BaseCrawlSignalSpider` class in `base_spider.py`.

### Request Middleware

Check `middlewares.py` for the middleware handling HTTP request and response processing.

### Data Models

You'll find data schema for the scraped items in `items.py`.

### Data Pipelines

The `pipelines.py` file includes pipelines to process and forward scraped data via `SendAPIPipeline`.

### Configurations

`settings.py` holds Scrapy and project-specific configurations.

### Tor IP Rotator

IP rotation is handled by the `TorProxyMiddleware` class located in `scrapy_tor_rotation`.

---

## Docker Deployment Guide

For details on building and running Docker containers, please refer to the [Docker Setup](#docker-setup) section.

---

## How to Contribute

Kindly refer to the `CONTRIBUTING.md` document if you're interested in making contributions.

---

## Licensing

The project is under the MIT License. For further information, consult the `LICENSE` file.
