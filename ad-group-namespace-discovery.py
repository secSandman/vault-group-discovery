#!/usr/bin/env python3
import sys
import requests
import time
import csv
import getpass

def get_namespaces(target, headers):
    """
    List all namespaces.
    Assumes the API returns JSON like: {"data": {"keys": ["namespace1", "namespace2", ...]}}
    """
    url = f"{target}/v1/sys/namespaces"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        namespaces = data.get('data', {}).get('keys', [])
        return namespaces
    except Exception as e:
        print(f"Error fetching namespaces: {e}")
        return []

def get_groups_for_namespace(target, token, namespace):
    """
    List all access control groups for the given namespace.
    Assumes the API returns JSON like: {"data": {"keys": ["group1", "group2", ...]}}
    """
    headers = {
        "X-Vault-Token": token,
        "X-Vault-Namespace": namespace
    }
    url = f"{target}/v1/identity/group?list=true"
    try:
        response = requests.get(url, headers=headers)
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
    Assumes the group details JSON is structured like:
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

    # Prompt securely for the Vault t
