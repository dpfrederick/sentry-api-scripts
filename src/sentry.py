import json
import os

import requests


def list_projects_for_org(
    org_slug: str, sentry_api_token: str, sentry_base_url: str = "https://sentry.io"
):
    url = f"{sentry_base_url}/api/0/organizations/{org_slug}/projects/"

    payload = {}
    headers = {
        "Authorization": f"Bearer {sentry_api_token}",
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)
