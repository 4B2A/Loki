# Loki ⚡

Loki is a standalone, high-performance privacy and identity rotation tool designed exclusively for Ubuntu and Debian-based Linux distributions. It allows tactical operators and privacy analysts to instantly obfuscate their local hardware presence and trigger complete network identity rotation after completing an operation—all without relying on external proxies, VPNs, or the Tor network.

## 🛠️ How It Works

When the `newid` command is executed, Loki safely isolates the system and performs the following operations sequentially:
1. **DHCP Lease Release:** Signals the local gateway/ISP router to terminate the current network footprint.
2. **RF/Data Leak Prevention:** Instantly brings down all physical network interfaces to prevent data and packet leakage during mutation.
3. **Hardware Spoofing:** Randomizes the MAC addresses of all interfaces using a vendor-independent scheme.
4. **Interface Mutation:** Brings interfaces back online under entirely new hardware identities.
5. **Fresh Lease Acquisition:** Forces a zero-state DHCP renegotiation to lease fresh local and public network addresses.

---

## 📋 Prerequisites

Loki requires `macchanger` and the default Linux network management utilities to perform lower-layer network manipulation.

Before running the tool, ensure your package index is updated and the core dependency is installed:

```bash
sudo apt update && sudo apt install macchanger isc-dhcp-client -y
```

---

## 🚀 Execution & Usage

Because Loki directly manipulates hardware kernel links, network sockets, and system interface states, it **must** be executed with root administrative privileges.

1. **Launch the environment:**
   ```bash
   sudo python3 loki.py
   ```

2. **Available Operations:**
   * `newid` : Initiates the interface isolation, hardware MAC randomization, and complete IP lease renewal process.
   * `exit`  : Safely purges temporary volatile session data and terminates the interactive shell prompt.

---

## ⚠️ Operational Notes

* **Interface Filtering:** Loki automatically isolates and ignores loopback (`lo`), virtual bridges (`br-`, `virbr`), container endpoints (`docker`, `veth`), and hypervisor links (`vboxnet`), ensuring only your physical network hardware is mutated.
* **Network Stability:** The identity rotation takes approximately 10-12 seconds to stabilize as the DHCP server assigns a new network lease.

---

## ⚖️ License & Disclaimer

This project is created for authorized penetration testing, security auditing, and forensic privacy research purposes only. The author (`4B2A`) holds no responsibility for unauthorized deployment or malicious abuse of this infrastructure utility.
