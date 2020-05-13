#!/usr/bin/env python3
import requests
import os

# Constants for Terraform
token = os.getenv("TF_API_TOKEN")
headers = {
    'Content-Type': "application/vnd.api+json",
    'Authorization': "Bearer {}".format(token)
    }

# Terraform API URL
def get_api_url(org_name: str) -> str:
    return "https://app.terraform.io/api/v2/organizations/{}/workspaces".format(org_name)

# Find workspace id from workspace name
def get_ws_id(ws_name: str, org_name: str) -> str:
    payload = ""
    url = get_api_url(org_name)
    response = requests.request("GET", url, data=payload, headers=headers)
    ws_id = next(filter(
        lambda it: it['attributes']['name'] == ws_name,response.json()['data']))['id']
    return ws_id

# Initiate run in the workspace
def destroy_cluster(destroy: bool, ws_name: str, org_name: str):
    ws_id = get_ws_id(ws_name, org_name)
    url = "https://app.terraform.io/api/v2/runs"
    payload_tupple = ("{ \"data\": { \"attributes\": { \"is-destroy\":",
        "true" if destroy else "false",
        ", \"message\": \"Custom message\" }, \"type\":\"runs\", ",
        "\"relationships\": { \"workspace\": { \"data\": { \"type\": ",
        "\"workspaces\", \"id\": \"",
        ws_id,
        "\" } } } } }")
    payload = "".join(payload_tupple)
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
