# Web Crawler

A Python-based web crawler that systematically browses websites and generates a comprehensive CSV report of all discovered URLs along with their HTTP status codes.

## Features

-   Crawls all pages within a specified domain
-   Respects same-origin policy (only crawls URLs from the same domain)
-   Generates a CSV report with URLs and their HTTP status codes
-   Handles relative and absolute URLs
-   Implements polite crawling with built-in delays
-   Filters out non-web schemes and fragments
-   Robust error handling for failed requests

## Prerequisites

-   Python 3.x
-   Linux/Unix environment (for apt-get)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:

```bash
sudo apt-get install python3-venv
python3 -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Usage

1. Run the script:

```bash
python index.py
```

2. When prompted:

    - Enter the website URL you want to crawl (e.g., https://example.com)
    - Specify the output CSV filename (e.g., links.csv)

3. The crawler will:
    - Start crawling from the provided URL
    - Save discovered URLs to the specified CSV file
    - Record HTTP status codes for each URL
    - Print progress information to the console

## Output Format

The script generates a CSV file with the following columns:

-   `URL`: The discovered URL
-   `Status_Code`: HTTP status code (only recorded if ≥ 300 or if the request failed)

## Features in Detail

### URL Processing

-   Removes URL fragments (#) and query parameters (?)
-   Converts relative URLs to absolute URLs
-   Validates URLs against the original domain

### Error Handling

-   Timeout handling for slow responses
-   Graceful handling of connection errors
-   Records failed requests with status code 0

### Rate Limiting

-   Implements a 1-second delay between requests to prevent server overload

## Contributing

Feel free to submit issues and enhancement requests.
