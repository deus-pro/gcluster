#!/usr/bin/env python3
import requests
import os
import argparse

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
def destroy_cluster(ws_name: str, org_name: str, destroy: bool = False):
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
    return response

# Main #
parser = argparse.ArgumentParser()
parser.add_argument("-w", "--workspace", type=str, help = "Provide the workspace name")
parser.add_argument("-o", "--org", type = str, help = "Provide the organisation name")
parser.add_argument("-d", "--destroy", action="store_true")
args = parser.parse_args()

result = destroy_cluster(args.workspace, args.org, args.destroy)
print(result.text)
