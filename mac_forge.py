#!/usr/bin/env python3

import subprocess
import random
import platform
import os
import re
import csv
import requests

class macforge:
    def __init__(self):
        self.title = (r"""             __  __    _    ____ _____                    
            |  \/  |  / \  / ___|  ___|__  _ __ __ _  ___ 
            | |\/| | / _ \| |   | |_ / _ \| '__/ _` |/ _ \
            | |  | |/ ___ \ |___|  _| (_) | | | (_| |  __/
            |_|  |_/_/   \_\____|_|  \___/|_|  \__, |\___|
                                               |___/      """)
        self.os_name = ""
        self.mac_address = []
        self.csv = "mac-vendors.csv"
        self.request_check = False

    def detect_os(self):
        system_platform = platform.system().lower()
        return system_platform

    def display_edition(self):
        system_platform = self.detect_os()
        subtitle = ""
        if system_platform == "windows":
            subtitle = "Windows Edition - Barely Functional!"
        elif system_platform == "darwin":
            subtitle = "macOS Edition"
        elif system_platform == "linux":
            subtitle = "Linux Edition"
        else:
            subtitle = "Error: Unknown OS Detected. Errors may occur."

        total_padding = ((70 - len(subtitle)) // 2)
        if total_padding >= 0:
            padding = total_padding * ' '
        else:
            padding = ''

        self.os_name = f"{padding}{subtitle}"

    def see_current_mac(self):
        self.mac_address = []
        
        if os.name == "nt":
            result = subprocess.check_output("ipconfig /all", shell=True, text=True)
            lines = result.splitlines()

            interface = None
            for line in lines:
                if "adapter" in line:
                    interface = re.sub(r"^(.*adapter\s*)(\S.*)", r"\2", line).strip()
                elif "Physical" in line:
                    mac = line.split(":")[1].strip()
                    if mac and interface:
                        self.mac_address.append(f"{interface} {mac}")
                        interface = None 

        else: 
            result = subprocess.check_output(
                "ifconfig | grep -E '^[a-zA-Z0-9]+|ether' | awk 'NR % 2 == 1 { iface = $1 } NR % 2 == 0 { print iface, $2 }'",
                shell=True, text=True)

            mac_regex = r'([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})'

            for line in result.splitlines():
                parts = line.split()
                
                if len(parts) == 2 and re.match(mac_regex, parts[1]):
                    self.mac_address.append(line)

        return self.mac_address


    def see_specific_mac(self):
        interface = input("Which interface would you like to view?: ")
        for line in self.mac_address:
            parts = line.split()
            interface_name = parts[0].rstrip(":")
            if interface_name == interface:
                print(f"Interface: {interface_name} | MAC Address: {parts[1]}")
                print("")
                return
        print(f"Interface {interface} not found")

    def is_valid_mac(self, mac):
        mac_pattern = r'^([0-9a-fA-F]{2}[:]){5}[0-9a-fA-F]{2}$'
        return re.match(mac_pattern, mac) is not None

    def set_mac_address(self, new_mac, interface):
        if not self.is_valid_mac(new_mac):
            raise ValueError(f"{new_mac} is not a valid MAC address format. A valid format looks like: XX:XX:XX:XX:XX:XX")
        if os.name == "nt":
            subprocess.call(f'netsh interface set interface "{interface}" newmac={new_mac}', shell=True)

        else:
            subprocess.call(f"ifconfig {interface} down", shell=True)
            subprocess.call(f"ifconfig {interface} hw ether {new_mac}", shell=True)
            subprocess.call(f"ifconfig {interface} up", shell=True)

    def user_change_mac(self):
        invalid_attempts = 0
        while True:
            interface = input("Which interface would you like to change?: ")
            interface_found = False

            for line in self.mac_address:
                parts = line.split()
                interface_name = parts[0].rstrip(":")
                if interface_name == interface:
                    interface_found = True
                    break

            if interface_found:
                new_mac = input("What would you like the new MAC address to be?: ")

                try:
                    self.set_mac_address(new_mac, interface)
                    print(f"MAC address for {interface} successfully changed to {new_mac}!")
                    break

                except ValueError as e:
                    print(f"An error occurred: {e}")
                    print("")
                    continue

            else:
                print("That is not a valid interface name. Try again.")
                invalid_attempts += 1

                if invalid_attempts >= 3:
                    input("[!] Too many invalid attempts. Press Enter to view the interface options: ")
                    self.see_current_mac()
                    print("")

                    for line in self.mac_address:
                        print(line)
                    invalid_attempts = 0
                    print("")
                    print("[+] Resetting invalid attempts counter.")

    def display_mac_prefixes(self, mac_prefixes):
        if mac_prefixes:
            batch_size = 5
            for i in range(0, len(mac_prefixes), batch_size):
                batch = mac_prefixes[i:i + batch_size]
                for prefix in batch:
                    print(prefix)

                if i + batch_size < len(mac_prefixes):
                    print("")
                    user_input = input("Would you like to see more? (y/n): ").lower()
                    print("")
                    if user_input != 'y':
                        break
                else:
                    print("[+] End of list")

    def search_mac_vendor(self):
        search_term = input("Choose a vendor: ")
        mac_prefixes = []

        with open(self.csv, mode='r') as file:
            csv_reader = csv.reader(file, delimiter=',')

            for row in csv_reader:
                if len(row) >= 5:
                    mac_address, vendor, _, _, _ = row
                    if search_term.lower() in mac_address.lower() or search_term.lower() in vendor.lower():
                        mac_prefix = mac_address.split(':')[:3]
                        mac_prefix_str = ':'.join(mac_prefix)

                        mac_prefixes.append(f"{vendor}: {mac_prefix_str}")
        if mac_prefixes:
            return mac_prefixes
        else:
            print(f"Error: no prefixes found for {search_term}")

    def sift_vendor_prefixes(self):
        mac_prefixes = self.search_mac_vendor()

        if mac_prefixes:
            print("")
            print(f"Found the following MAC prefixes:")
            print("")
            self.display_mac_prefixes(mac_prefixes)
        else:
            print(f"No MAC prefixes found.")

    def random_vendor_mac(self):
        mac_prefixes = self.search_mac_vendor()
        mac_prefixes_stripped = [mac.split(": ")[-1] for mac in mac_prefixes if ": " in mac]

        if mac_prefixes_stripped:
            random_mac = random.choice(mac_prefixes_stripped)
            return random_mac
        else:
            return None

    def mac_to_hex_list(self, mac_prefix):
        mac_parts = mac_prefix.split(':')
        hex_list = [f"0x{int(part, 16):02X}" for part in mac_parts]

        return hex_list

    def generate_mac_address(self):
        vendor_mac = self.random_vendor_mac()
        mac_prefix = self.mac_to_hex_list(vendor_mac)

        mac_prefix = [int(x, 16) for x in mac_prefix]

        mac_suffix = [random.randint(0, 255) for _ in range(3)]
        mac_suffix[-1] = random.randint(1, 255)
        mac = mac_prefix + mac_suffix
        mac_address = ':'.join(f'{x:02x}' for x in mac)
        return mac_address

    def set_vendor_mac(self):
        invalid_attempts = 0
        while True:
            interface = input("Which interface would you like to change?: ")
            interface_found = False

            for line in self.mac_address:
                parts = line.split()
                interface_name = parts[0].rstrip(":")
                if interface_name == interface:
                    interface_found = True
                    break

            if interface_found:
                new_mac = self.generate_mac_address()

                try:
                    self.set_mac_address(new_mac, interface)
                    print(f"MAC address for {interface} successfully changed to {new_mac}!")
                    break

                except ValueError as e:
                    print(f"An error occurred: {e}")
                    print("")
                    continue

            else:
                print("That is not a valid interface name. Try again.")
                invalid_attempts += 1

                if invalid_attempts >= 3:
                    input("[!] Too many invalid attempts. Press Enter to view the interface options: ")
                    self.see_current_mac()
                    print("")

                    for line in self.mac_address:
                        print(line)
                    invalid_attempts = 0
                    print("")
                    print("[+] Resetting invalid attempts counter.")


    def check_mac_address(self):
        interface = input("Which interface would you like to view?: ")
        current_mac = ""
        import requests

        for line in self.mac_address:
            parts = line.split()
            interface_name = parts[0].rstrip(":")
            if interface_name == interface:
                current_mac = parts[1] 
                break

        if not current_mac:
            print(f"Interface {interface} not found.")
            return 

        url = f"https://api.macvendors.com/{current_mac}"

        try:
            response = requests.get(url)

            if response.status_code == 200:
                print(f"Your machine, with MAC address {current_mac}, appears to be a(n) {response.text} device")
            elif response.status_code == 404:
                print(f"Vendor not found for MAC address {current_mac}.")
            else:
                print(f"Error: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def start(self):
        print("[1] Display a list of your current interfaces and their MAC addresses.")
        print("[2] Display the MAC address of a specific interface.")
        if os.name != "nt":
            print("[3] Manually change the MAC address of an interface.")
            print("[4] Search the database for vendor prefixes associated with specific vendors.")
            print("[5] Generate a valid MAC address for a specific vendor.")
        print("[*] Check the MAC address vendor identity of your current interfaces.")
        print("[0] Exit the program.")

    def manual(self):
        print("MACForge Manual")
        print("[1] Displays all active interfaces with their current MAC addresses.")
        print("[2] Enter the name of an interface to see its MAC address.")
        if os.name != "nt":
            print("[3] Select an interface and change its MAC address to a desired value.")
            print(
                "[4] Search for a vendor in the attached list and display the MAC address prefixes associated with that vendor.")
            print("[5] Choose an interface and generate a valid MAC address from a random vendor in the attached list.")
        print("[*] Query macvendors.com to identify the vendor associated with the MAC address of an interface.")
        print("[0] Exit the program.")

    def execute(self):
        print("")
        self.display_edition()
        print(self.title)
        print(self.os_name)
        self.see_current_mac()
        print("")
        self.start()
        while True:
            print("")
            print("Type '?' for the manual. Type 'c' to reprint the list of commands.")
            command = input("Enter a command: ")
            if command == "0":
                print("Goodbye!")
                break
            if command == "1":
                self.see_current_mac()
                for line in self.mac_address:
                    print(line)
            if command == "2":
                self.see_specific_mac()
            if command == "3":
                self.user_change_mac()
            if command == "4":
                self.sift_vendor_prefixes()
            if command == "5":
                self.set_vendor_mac()
            if command == "*":
                self.check_mac_address()
            if command == "c":
                self.start()


application = macforge()
application.execute()