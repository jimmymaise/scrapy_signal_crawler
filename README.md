## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
  - [Local Installation](#local-installation)
  - [Docker Installation](#docker-installation)
- [How to Run](#how-to-run)
- [Project Structure](#project-structure)
- [Technical Overview](#technical-overview)
  - [Spiders](#spiders)
  - [Middleware](#middleware)
  - [Items](#items)
  - [Pipelines](#pipelines)
  - [Settings](#settings)
  - [Tor Proxy Rotation](#tor-proxy-rotation)
- [Docker Deployment](#docker-deployment)
- [Contributing](#contributing)
- [License](#license)

---

## Introduction

Welcome to `scrapy_signal_crawler`, a Scrapy-based project focused on collecting trading signals from various sources. This project offers advanced features like IP rotation, data serialization, and a well-structured pipeline for effective data extraction and processing.

---

## Installation

### Local Installation

1. **Clone the Repository**: Clone the repository onto your local machine.
2. **Navigate to Project Directory**: Use `cd` to enter the project directory.
3. **Install Dependencies**: Execute `pip install -r requirements.txt` to install the necessary Python packages.
4. **Run the Scrapy Spiders**: Start the Scrapy spiders using the command `scrapy crawl <SPIDER_NAME>`.

### Docker Installation

1. **Build the Docker Image**: 
    ```bash
    docker build . -t bot_runner
    ```
2. **Run the Docker Container**: 
    ```bash
    docker run --net="host" --log-opt max-size=10m --log-opt max-file=3 -e CONTROLLER_BASE_URL="http://40.78.1.149:8000" -d bot_runner --runner-name zulu_runner_ubuntu_server --bot-type zulu_api
    docker run --net="host" --log-opt max-size=10m --log-opt max-file=3 -e CONTROLLER_BASE_URL="http://40.78.1.149:8000" -d bot_runner --runner-name exness_runner_ubuntu_server --bot-type exness_api --tor
    ```
    > **Note**: Add the `--tor` parameter to run with Tor.

---

## Technical Overview

### Spiders

The project includes spiders for different trading signal sources. These spiders reside in the `spiders/` directory and inherit from the `BaseCrawlSignalSpider` class, which is defined in `base_spider.py`.

### Middleware

Middleware for processing HTTP requests and responses is located in `middlewares.py`.

### Items

Data models for the items that are scraped can be found in `items.py`.

### Pipelines

`pipelines.py` contains pipelines for processing and sending the scraped data to a controller via the `SendAPIPipeline` class.

### Settings

Settings specific to Scrapy and the project are located in `settings.py`.

### Tor Proxy Rotation

The `TorProxyMiddleware` class in the `scrapy_tor_rotation` directory implements IP rotation functionality.

---

## Docker Deployment

Please refer to the [Docker Installation](#docker-installation) section for details on building and running the Docker container.

---

## Contributing

If you wish to contribute to this project, please refer to the `CONTRIBUTING.md` file.

---

## License

This project is licensed under the MIT License. For more details, see the `LICENSE` file.
