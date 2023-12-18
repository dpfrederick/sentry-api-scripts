import requests
import urllib3


def check_team_exists(team_slug: str, backstage_base_url: str):
    url = f"{backstage_base_url}/api/catalog/entities/by-name/Group/default/{team_slug}"

    payload = {}
    headers = {}

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    if response.status_code == 200:
        return True
    else:
        return False
