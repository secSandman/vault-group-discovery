#!/usr/bin/env python3
import sys
import requests
import time
import csv
import getpass

def get_namespaces(target, headers):
    """
    List all namespaces using the LIST HTTP method.
    Expects JSON response like: {"data": {"keys": ["namespace1", "namespace2", ...]}}
    """
    url = f"{target}/v1/sys/namespaces"
    try:
        response = requests.request("LIST", url, headers=headers)
        response.raise_for_status()
        data = response.json()
        namespaces = data.get('data', {}).get('keys', [])
        return namespaces
    except Exception as e:
        print(f"Error fetching namespaces: {e}")
        return []

def get_groups_for_namespace(target, token, namespace):
    """
    List all access control groups for the given namespace using the LIST HTTP method.
    Expects JSON response like: {"data": {"keys": ["group1", "group2", ...]}}
    """
    headers = {
        "X-Vault-Token": token,
        "X-Vault-Namespace": namespace
    }
    url = f"{target}/v1/identity/group?list=true"
    try:
        # Use LIST method instead of GET
        response = requests.request("LIST", url, headers=headers)
        response.raise_for_status()
        data = response.json()
        groups = data.get('data', {}).get('keys', [])
        return groups
    except Exception as e:
        print(f"Error fetching groups for namespace '{namespace}': {e}")
        return []

def get_group_details(target, token, namespace, group_id):
    """
    Get the details for a specific group.
    Expects JSON structured as:
    {
      "data": {
         "name": "group_name",
         "policies": ["policy1", "policy2"]
      }
    }
    """
    headers = {
        "X-Vault-Token": token,
        "X-Vault-Namespace": namespace
    }
    url = f"{target}/v1/identity/group/{group_id}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        group_data = data.get('data', {})
        return group_data
    except Exception as e:
        print(f"Error fetching details for group '{group_id}' in namespace '{namespace}': {e}")
        return {}

def main():
    if len(sys.argv) < 2:
        print("Usage: python ad-group-namespace-discovery.py <target_url>")
        sys.exit(1)
    
    target = sys.argv[1].rstrip('/')  # Remove any trailing slash

    # Prompt securely for the Vault token
    token = getpass.getpass(prompt="Enter Vault Token: ")

    # Global headers for calls that don't require a namespace header
    headers = {
        "X-Vault-Token": token,
    }
    
    # Get list of namespaces using the LIST method
    namespaces = get_namesp
