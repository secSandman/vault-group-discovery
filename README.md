# AD Group Namespace Discovery

This Python script queries the HashiCorp Vault Enterprise API to discover namespaces and list all associated access control groups along with their attached policies. The output is pre-processed and exported to a CSV file.

## Features

- **Namespace Discovery:** Retrieves all namespaces from the Vault API.
- **Group Listing:** For each namespace, lists all access control (AD) groups.
- **Group Details:** Fetches details for each group, including attached policies.
- **CSV Export:** Writes output to a CSV file with columns:
  - **namespace**
  - **AD group name**
  - **group policies**
- **Secure Token Input:** Accepts the Vault token as a command-line argument or securely prompts for it.
- **Error Handling:** Catches and prints errors for each API call.
- **API Throttling:** Introduces a 2-second wait after processing each namespace to avoid overwhelming the API.

## Requirements

- Python 3.x
- [Requests library](https://pypi.org/project/requests/)  
  Install via pip:
  ```bash
  pip install requests

# Installation

Clone the repository or download the script:

```bash
git clone https://github.com/yourusername/ad-group-namespace-discovery.git
cd ad-group-namespace-discovery
```

# Ensure all dependencies are installed:

bash
Copy
pip install requests
Usage
Run the script from the command line with the Vault token and target URL as arguments.

# Command-Line Arguments
```
<Vault_Token|->: Supply your Vault token directly, or use a dash (-) to be prompted securely.
<target_url>: The URL of your HashiCorp Vault instance (e.g., https://test.vault.com).
```

#Examples

```
Prompt for Token Securely:

python ad-group-namespace-discovery.py - https://test.vault.com
Provide Token Directly:

python ad-group-namespace-discovery.py myVaultToken https://test.vault.com
```

The script generates a CSV file named ad_group_namespace_discovery.csv in the current directory with the following columns:

-namespace
-AD group name
-group policies
-Customization
-API Endpoints & JSON Parsing
-The script assumes specific JSON structures returned by the Vault API. Adjust the endpoints or JSON parsing logic in the script if your Vault configuration differs.

Wait Time

The script waits for 2 seconds after processing each namespace. Adjust the time.sleep(2) call as needed.

Error Handling

Each API call is wrapped in a try-except block. In case of an error (e.g., network issues or invalid token), the error is printed to the console and the script continues processing the next item.

# Contributing
Contributions are welcome! Please open issues or submit pull requests to enhance this project.

# License
This project is licensed under the MIT License.

# Disclaimer
This script is provided "as-is" without any warranty. Use it at your own risk.


