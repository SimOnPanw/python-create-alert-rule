# Prisma Cloud Create Alert Rule

## Requirements

- Python 3.x
- Requests library
- Dotenv library (for managing environment variables)

## Installation and Setup

Before running the script, ensure you have Python 3 installed on your system. 

### Setting Up a Virtual Environment
It's recommended to run this script in a Python virtual environment to manage dependencies effectively.

1. **Create and activate a Virtual Environment**: 
```bash
python3 -m virtualenv venv && source venv/bin/activate
```

2. **Installing Dependencies**:  
Install the required Python libraries in your virtual environment:  
```bash
pip install -r requirements.txt
```


## Configuration
Create a .env file in the same directory as your script with the following environment variables:

```bash
PRISMA_API_URL=your_prisma_api_url
PRISMA_ACCESS_KEY=your_access_key
PRISMA_SECRET_KEY=your_secret_key
```

Replace your_prisma_api_url, your_access_key, and your_secret_key with your actual Prisma Cloud API URL, access key, and secret key.

## Usage


```bash
python3 main.py 
```

### Debugging
Enable debug logging to get more detailed output:

```bash
python3 main.py --debug
```


