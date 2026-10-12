#!/usr/bin/env bash

# --- ANSI COLOR CODES ---
C_BLUE="\033[94m"
C_GREEN="\033[92m"
C_YELLOW="\033[93m"
C_RED="\033[91m"
C_CYAN="\033[96m"
C_WHITE="\033[97m"
F_BOLD="\033[1m"
F_END="\033[0m"

log_info() { echo -e "${C_BLUE}[*]${C_WHITE} $1${F_END}"; }
log_success() { echo -e "${C_GREEN}[+]${C_WHITE} $1${F_END}"; }
log_warn() { echo -e "${C_YELLOW}[!]{C_WHITE} $1${F_END}"; }
log_error() { echo -e "${C_RED}[-]${C_WHITE} $1${F_END}"; }

echo -e "${C_CYAN}${F_BOLD}"
echo "  ██╗      ██████╗ ██╗  ██╗██╗"
echo "  ██║     ██╔═══██╗██║ ██╔╝██║"
echo "  ██║     ██║   ██║█████╔╝ ██║"
echo "  ██║     ██║   ██║██╔═██╗ ██║"
echo "  ███████╗╚██████╔╝██║  ██╗██║"
echo "  ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝"
echo -e "   Loki Installer | coded by 4B2A${F_END}\n"

# 1. Root Privilege Verification
if [ "$EUID" -ne 0 ]; then
    log_error "Loki installation requires administrative privileges."
    echo -e "${C_YELLOW}[*] Please execute using:${C_WHITE} sudo ./setup.sh${F_END}\n"
    exit 1
fi

# 2. Source File Verification
if [ ! -f "loki.py" ]; then
    log_error "Error: 'loki.py' not found in the current directory!"
    log_warn("Please run setup.sh from inside the project directory containing loki.py.")
    exit 1
fi

# 3. Dependency Deployment via APT Package Manager
log_info "Updating system package index and deploying dependencies..."
apt-get update -y && apt-get install macchanger isc-dhcp-client python3 -y

if [ $? -ne 0 ]; then
    log_error "Failed to install dependencies. Please verify your internet connection or package repository configuration."
    exit 1
fi
log_success "Core dependencies successfully deployed."

# 4. Installation and Binary Integration
log_info "Integrating Loki binaries into system binaries..."

# Copy loki.py to system path and drop the extension for clean execution
cp loki.py /usr/local/bin/loki

# Ensure the Python 3 shebang header is present at the first line
if ! grep -q "#!/usr/bin/env python3" /usr/local/bin/loki; then
    sed -i '1s/^/#!\/usr/bin/env python3\n/' /usr/local/bin/loki
fi

# Set executable execution permissions
chmod +x /usr/local/bin/loki

if [ $? -eq 0 ]; then
    echo ""
    log_success "LOKI HAS BEEN SUCCESSFULLY INSTALLED!"
    echo -e "${C_WHITE}You can now instantiate the framework from any terminal directory by invoking:${F_END}"
    echo -e "${C_GREEN}${F_BOLD}sudo loki${F_END}\n"
else
    log_error "An unexpected filesystem error occurred during automated deployment."
    exit 1
fi
