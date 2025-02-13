import os
from fastapi import HTTPException
import requests
import json
from dotenv import load_dotenv

load_dotenv()


class ZohoDeskClient:
    def __init__(
            self,
            client_id: str = os.environ.get("ZOHO_CLIENT_ID", None),
            client_secret: str = os.environ.get("ZOHO_CLIENT_SECRET", None),
            code: str = os.environ.get("ZOHO_CODE", None),
            dept_id: int = os.environ.get("ZOHO_DEPT_ID", None),
            org_id: int = os.environ.get("ZOHO_ORG_ID", None),
    ):
        self._client_id = client_id
        self._client_secret = client_secret
        token = ZohoDeskClient._get_tokens()
        self._access_token = token.get('access_token', None)
        self._refresh_token = token.get('refresh_token', None)
        self._dept_id = dept_id
        self._org_id = org_id
        self._code = code
        if code:
            self._update_refresh_token()

    def _update_refresh_token(self):
        try:
            # Read existing JSON data from file
            with open('db/token.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            # If the file doesn't exist, create a new dictionary
            data = {}

        # Update values
        self._generate_tokens()
        data['refresh_token'] = self._refresh_token
        data['access_token'] = self._access_token

        # Write the updated JSON data back to the file
        with open('db/token.json', 'w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def _get_tokens():
        try:
            # Read existing JSON data from file
            with open('db/token.json', 'r') as file:
                data: json = json.load(file)
            return data
        except FileNotFoundError:
            return {}

    def raise_ticket(self, data: json):
        print("------------------ ticket -------------\n", data)
        if not self._access_token:
            self._refresh_access_token()

        url = "https://desk.zoho.com/api/v1/tickets"

        payload = json.dumps({
            "departmentId": self._dept_id,
            "subject": data.get("subject", "MySportsDriver Customer Support Chat"),
            "category": data.get("category", "Chatbot"),
            "subCategory": data.get("subCategory", ""),
            "description": data.get("description", "No Description Given"),
            "channel": "Chatbot",
            "contact": {
                "email": data.get("email", "")
            },
            "status": data.get("status", "open"),
            "email": data.get("email", "")
        })

        headers = {
            'orgId': self._org_id,
            'Authorization': f'Zoho-oauthtoken {self._access_token}',
            'Content-Type': 'application/json',
        }

        response = requests.post(url=url, headers=headers, data=payload)
        if response.status_code == 201 or response.status_code == 200:
            return [{
                "text": "We've received your ticket and will address it promptly. 🎫 Please expect to hear back from us within the next 24 business hours.🕒 "},
                {
                    "text": "Thank you and have a great rest of your day!"}]
        if response.status_code == 401:
            self._refresh_access_token()
            return self.raise_ticket(data)
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

    def _refresh_access_token(self):
        url = (f"https://accounts.zoho.com/oauth/v2/token?grant_type=refresh_token&"
               f"refresh_token={self._refresh_token}&"
               f"client_id={self._client_id}&"
               f"client_secret={self._client_secret}")

        response = requests.post(url)

        if response.status_code == 200:
            token_data = response.json()
            self._access_token = token_data["access_token"]
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

    def _generate_tokens(self):
        url = (f"https://accounts.zoho.com/oauth/v2/token?"
               f"grant_type=authorization_code&"
               f"code={self._code}&"
               f"client_id={self._client_id}&"
               f"client_secret={self._client_secret}")

        response = requests.post(url)
        if response.status_code == 200:
            token_data = response.json()
            if token_data.get("error", False):
                return
            self._access_token = token_data["access_token"]
            self._refresh_token = token_data["refresh_token"]
