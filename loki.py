import os
import sys
import subprocess
import time

banner = r"""
.____           __   .__ 

|    |    ____ |  | _|__|
|    |   /  _ \|  |/ /  |
|    |__(  <_> )    <|  |
|_______ \____/|__|_ \__|
        \/          \/   
    coded by 4B2A
"""


def check_root():
    """Ensures the script is run with administrative privileges."""
    if os.geteuid() != 0:
        print(
            "\n[!] ERROR: Loki requires root privileges to manipulate network configurations."
        )
        print("[*] Please run again using: sudo python3 <script_name>.py\n")
        sys.exit(1)


def get_interfaces():
    """Gathers all available physical network interfaces except loopback and virtual links."""
    try:
        interfaces = os.listdir("/sys/class/net/")
        ignored = ["lo", "docker", "vboxnet", "tun", "veth", "br-"]
        return [
            iface for iface in interfaces if not any(ign in iface for ign in ignored)
        ]
    except Exception as e:
        print(f"[!] Critical error reading network interfaces: {e}")
        sys.exit(1)


def change_identity():
    """Executes network shutdown, MAC randomization, IP release, and renewal."""
    print("\n[*] Initiating Loki standalone identity rotation protocol...")
    interfaces = get_interfaces()

    # 1. Release existing DHCP leases (Tells the ISP/Router to drop the current IPs)
    print("[*] Releasing current IP leases from DHCP...")
    for iface in interfaces:
        subprocess.run(
            ["dhclient", "-r", iface],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    time.sleep(1)

    # 2. Shutting down all network interfaces
    print("[*] Disabling all network interfaces...")
    for iface in interfaces:
        subprocess.run(["ip", "link", "set", iface, "down"], check=False)
    time.sleep(1.5)

    # 3. Randomizing MAC addresses
    print("[*] Randomizing MAC addresses via macchanger...")
    for iface in interfaces:
        subprocess.run(
            ["macchanger", "-r", iface],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    time.sleep(1.5)

    # 4. Bringing interfaces back online
    print("[*] Enabling network interfaces with new hardware IDs...")
    for iface in interfaces:
        subprocess.run(["ip", "link", "set", iface, "up"], check=False)
    time.sleep(2)

    # 5. Requesting fresh Local and Public IPs with the new identity
    print("[*] Requesting fresh IP leases from DHCP (Local & Public)...")
    for iface in interfaces:
        subprocess.run(
            ["dhclient", iface],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )

    print("[*] Waiting for network to stabilize (5s)...")
    time.sleep(5)

    print(
        "[+] SUCCESS: Hardware IDs randomized and network addresses renewed successfully.\n"
    )


def main():
    check_root()
    os.system("clear" if os.name == "posix" else "cls")
    print(banner)
    print(" Type 'newid' to rotate identity or 'exit' to terminate the session.\n")

    while True:
        try:
            cmd = input("loki > ").strip().lower()

            if cmd == "newid":
                change_identity()
            elif cmd == "exit":
                print("[*] Terminating session. Stay safe out there.")
                sys.exit(0)
            elif cmd == "":
                continue
            else:
                print(
                    f"[-] Unknown command: '{cmd}'. Available commands: 'newid', 'exit'"
                )
        except (KeyboardInterrupt, EOFError):
            print("\n[*] Session interrupted. Exiting safely.")
            sys.exit(0)


if __name__ == "__main__":
    main()
