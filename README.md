# MACForge
MACForge is a Python-based utility designed to help users view and modify MAC addresses for network interfaces on their machines. This tool supports macOS and Linux, with only basic functionality for Windows right now, allowing users to easily manage their MAC addresses. It also includes features like searching for vendor prefixes, generating random MAC addresses, and identifying the vendor of a given MAC address using the macvendors.com API.

## Features
View Current MAC Addresses: Displays a list of all active network interfaces and their MAC addresses.  

View Specific Interface MAC Address: Allows the user to view the MAC address of a specific interface by name.  

Change MAC Address: Provides an option to manually change the MAC address of a selected network interface.  

Search for Vendor MAC Prefixes: Allows searching for MAC address prefixes associated with specific vendors.  

Generate MAC Address: Generates a random MAC address based on a vendor's MAC address prefix.  

Vendor Lookup: Queries the macvendors.com API to identify the vendor associated with a given MAC address.  

## Requirements
Python 3.x
requests module (used for querying the macvendors API)
mac-vendors.csv file containing MAC address vendor prefixes (included in the repository)

## Usage
The program will prompt you to enter a command from the list of available options:

1. Display a list of your current interfaces and their MAC addresses.
2. Display the MAC address of a specific interface.
3. Manually change the MAC address of an interface (Linux/macOS only).
4. Search the database for vendor prefixes associated with specific vendors.
5. Generate a valid MAC address for a specific vendor.
6. Check the MAC address vendor identity of your current interfaces.
0. Exit the program.

## Manual
You can view the manual at any time by typing ?. The manual provides detailed information on each command, its functionality, and how to use the program effectively.

## Supported Operating Systems
Windows: Limited functionality, mainly for viewing MAC addresses.  
macOS: Full functionality, including changing MAC addresses.  
Linux: Full functionality, including changing MAC addresses.  
