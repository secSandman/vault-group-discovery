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
    namespaces = get_namespaces(target, headers)
    if not namespaces:
        print("No namespaces found or error retrieving namespaces.")
        sys.exit(1)
    
    # Open CSV file for writing output
    csv_filename = "ad_group_namespace_discovery.csv"
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ["namespace", "AD group name", "group policies"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        # Process each namespace
        for ns in namespaces:
            print(f"Processing namespace: {ns}")
            groups = get_groups_for_namespace(target, token, ns)
            
            # Wait 2 seconds after each namespace API query
            time.sleep(2)
            
            if not groups:
                print(f"No groups found in namespace '{ns}'.")
                continue
            
            # For each group, get details and write to CSV
            for group_id in groups:
                group_details = get_group_details(target, token, ns, group_id)
                if not group_details:
                    continue
                # Use the 'name' from the details or fallback to the group_id
                group_name = group_details.get("name", group_id)
                policies = group_details.get("policies", [])
                # Convert list of policies to a comma-separated string
                policies_str = ", ".join(policies) if isinstance(policies, list) else str(policies)
                
                writer.writerow({
                    "namespace": ns,
                    "AD group name": group_name,
                    "group policies": policies_str
                })
    
    print(f"CSV output written to {csv_filename}")

if __name__ == "__main__":
    main()
