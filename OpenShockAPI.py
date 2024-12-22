#Made by Cloud (aka Scarlett)
#This is a small little libary to control openshock devices
#I'm not responsible for any damage to yourself, be safe and have fun :3

import requests

class OpenShockAPI:
    def __init__(self, token, base_url):
        """
        Initialize the OpenShockAPI with a token and a base URL.

        :param token: The OpenShock API token for authentication.
        :param base_url: The base URL of the API (default is 'https://api.openshock.app').
        """
        self.base_url = base_url
        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'OpenShockToken': token
        }

    def control_device(self, shocks, custom_name):
        """
        Control the shockers with specified parameters.

        :param shocks: A list of dictionaries containing shock details (id, type, intensity, duration, exclusive).
        :param custom_name: Custom name for the request (optional).
        :return: Response from the API.
        """
        url = f"{self.base_url}/2/shockers/control"
        payload = {
            "shocks": shocks,
            "customName": custom_name
        }

        response = requests.post(url, json=payload, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def list_shockers(self):
        """
        List all hubs and their associated shockers belonging to the authenticated user, including hub IDs and device details.

        :return: List of dictionaries, each containing hub ID, hub name, and associated shocker details.
        """
        url = f"{self.base_url}/1/shockers/own"

        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            result = []
            data = response.json().get("data", [])

            for hub in data:
                hub_id = hub['id']
                hub_name = hub['name']
                hub_created_on = hub['createdOn']

                for shocker in hub['shockers']:
                    shocker_info = {
                        "hub_id": hub_id,
                        "hub_name": hub_name,
                        "hub_created_on": hub_created_on,
                        "device_id": shocker['id'],
                        "device_name": shocker['name'],
                        "model": shocker['model'],
                        "rfId": shocker['rfId'],
                        "is_paused": shocker['isPaused'],
                        "created_on": shocker['createdOn']
                    }
                    result.append(shocker_info)

            return result
        else:
            response.raise_for_status()



    def get_shocker_info(self, shocker_id):
        """
        Get detailed information about a specific shocker.

        :param shocker_id: UUID of the shocker.
        :return: Shocker details.
        """
        url = f"{self.base_url}/1/shockers/{shocker_id}"

        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json().get("data", {})
        elif response.status_code == 404:
            return {"error": "Shocker does not exist or access is denied"}
        else:
            response.raise_for_status()