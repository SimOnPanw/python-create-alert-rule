__author__ = "Simon Melotte"

import os
import json
import requests
import argparse
import logging
from dotenv import load_dotenv

# Create a logger object
logger = logging.getLogger()


def add_alert_rule(base_url, token):
    url = f"{base_url}/alert/rule"
    headers = {"content-type": "application/json; charset=UTF-8", "x-redlock-auth": token}

    
    payload = json.dumps({
        "name": "Auto Dismiss Monitor IAM policy changes",
        "description": "",
        "enabled": True,
        "scanAll": False,
        "alertRuleNotificationConfig": [],
        "delayNotificationMs": 0,
        "notifyOnOpen": True,
        "policies": [
            "8bef368e-7b79-4828-a9cd-xxxx"
        ],
        "target": {
            "alertRulePolicyFilter": {
            "cloud.type": [
                "aws"
            ]
            },
            "accountGroups": [
                "88780bdf-d49c-4b06-add1-xxx",
                "5e01b79c-9ff6-4775-ac94-yyy"
            ],
            "excludedAccounts": [],
            "regions": [],
            "tags": [],
            "targetResourceList": {
            "action": "AUTO_DISMISS",
            "enabled": True,
            "additionalNotes": "",
            "approver": "",
            "ids": None,
            "reason": "Auto Dismiss the alert and send an email notifications",
            "requestor": ""
            }
        }
    })

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
    except requests.exceptions.RequestException as err:
        logger.error("Oops! An exception occurred in add_alert_rule, ", err)
        logger.error(f"{response.text}")
        return None

    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response headers: {response.headers}")
    logger.debug(f"Response text: {response.text}")
    return response.json()

def get_compute_url(base_url, token):
    url = f"https://{base_url}/meta_info"
    headers = {"content-type": "application/json; charset=UTF-8", "Authorization": "Bearer " + token}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
    except requests.exceptions.RequestException as err:
        logger.error("Oops! An exception occurred in get_compute_url, ", err)
        return None

    response_json = response.json()
    return response_json.get("twistlockUrl", None)


def login_saas(base_url, access_key, secret_key):
    url = f"https://{base_url}/login"
    payload = json.dumps({"username": access_key, "password": secret_key})
    headers = {"content-type": "application/json; charset=UTF-8"}
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
    except Exception as e:
        logger.info(f"Error in login_saas: {e}")
        return None

    return response.json().get("token")


def login_compute(base_url, access_key, secret_key):
    url = f"{base_url}/api/v1/authenticate"

    payload = json.dumps({"username": access_key, "password": secret_key})
    headers = {"content-type": "application/json; charset=UTF-8"}
    response = requests.post(url, headers=headers, data=payload)
    return response.json()["token"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Enable debug logging.")    

    args = parser.parse_args()

    if args.debug:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO

    logging.basicConfig(level=logging_level,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filename='app.log',
                        filemode='a')
    
    # Create a console handler
    console_handler = logging.StreamHandler()

    # Add the console handler to the logger
    logger.addHandler(console_handler)

    logger.info(f"======================= START =======================")
    if args.debug: 
        logger.info(f"======================= DEBUG MODE =======================")


    load_dotenv()
    url = os.environ.get("PRISMA_API_URL")
    identity = os.environ.get("PRISMA_ACCESS_KEY")
    secret = os.environ.get("PRISMA_SECRET_KEY")

    if not url or not identity or not secret:
        logger.error(
            "PRISMA_API_URL, PRISMA_ACCESS_KEY or PRISMA_SECRET_KEY environment variables are not set."
        )
        return

    token = login_saas(url, identity, secret)
    compute_url = get_compute_url(url, token)
    compute_token = login_compute(compute_url, identity, secret)
    logger.debug(f"Compute url: {compute_url}")

    if token is None:
        logger.error("Unable to authenticate.")
        return

    add_alert_rule(url, token)

    logger.info(f"======================= END =======================")


if __name__ == "__main__":
    main()
