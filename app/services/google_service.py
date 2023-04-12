from app import get_google_provider_cfg, client, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from flask import request

import requests
import json
import os


class GoogleService:

    def make_recaptcha_request(self, captcha_token: str) -> bool:
        recaptcha_url = "https://www.google.com/recaptcha/api/siteverify"
        data = {'secret': os.getenv("GOOGLE_CAPTCHA_KEY", default=""), 'response': captcha_token}
        result = requests.post(url=recaptcha_url, params=data)
        data = result.json()

        if not data['success']:
            return False

        return True

    def get_google_redirect_uri(self):
        google_provider_cfg = get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        return client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.base_url + "/callback",
            scope=["openid", "email", "profile"],
        )

    def get_google_user(self):
        code = request.args.get("code")
        google_provider_cfg = get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]

        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code
        )

        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
        )

        client.parse_request_body_response(json.dumps(token_response.json()))
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        return requests.get(uri, headers=headers, data=body)
