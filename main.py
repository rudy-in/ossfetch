import platform
import psutil
import typer
import os
import subprocess

app = typer.Typer()

def get_window_manager():
    wm = os.environ.get("XDG_CURRENT_DESKTOP")
    if wm:
        return wm
    wm = os.environ.get("DESKTOP_SESSION")
    if wm:
        return wm
    return "N/A"

def get_desktop_environment():
    de = os.environ.get("XDG_SESSION_TYPE")
    if de:
        return de
    de = os.environ.get("XDG_CURRENT_DESKTOP")
    if de:
        return de
    return "N/A"

def get_cpu_model():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if line.strip().startswith('model name'):
                    return line.split(':')[1].strip()
    except Exception as e:
        return f"Error fetching CPU model: {e}"

def get_terminal():
    try:
        return os.environ.get('TERM', 'N/A')
    except Exception as e:
        return f"Error fetching terminal: {e}"

def get_os_info():
    try:
        with open('/etc/os-release', 'r') as f:
            for line in f:
                if line.startswith('PRETTY_NAME'):
                    return line.split('=')[1].strip().strip('"')
    except Exception as e:
        return f"Error fetching OS info: {e}"

def get_gpu_info():
    try:
        lspci_output = subprocess.check_output(['lspci'], universal_newlines=True)
        gpu_info = ""
        for line in lspci_output.splitlines():
            if 'VGA' in line or '3D controller' in line:
                gpu_name = line.strip().split(': ', 1)[1].split(' [', 1)[0]  # Extract GPU name before the first square bracket
                gpu_info += gpu_name + "\n"
        return gpu_info.strip()
    except Exception as e:
        return f"Error fetching GPU info: {e}"

def get_terminal_colorscheme():
    try:
        # Run a command to get the terminal color scheme dynamically
        # For example, you could use a command like "echo $COLORFGBG"
        colorscheme = subprocess.check_output(['echo', '$COLORFGBG'], universal_newlines=True).strip()
        return colorscheme
    except Exception as e:
        return f"Error fetching terminal colorscheme: {e}"

@app.command()
def fetch():
    """Fetch and display system information."""
    os_name = get_os_info()
    os_version = platform.release()
    cpu_model = get_cpu_model()
    cpu_percent = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    memory_used = memory_info.used
    memory_total = memory_info.total
    memory_percent = memory_info.percent
    gpu_info = get_gpu_info()
    wm_info = get_window_manager()
    de_info = get_desktop_environment()
    terminal_info = get_terminal()
    host_info = platform.node()
    shell_info = os.environ.get('SHELL', 'N/A')
    terminal_colorscheme = get_terminal_colorscheme()

    typer.echo("\033[1;32;40m                  `-`                     \033[1;37;40m" + platform.node())
    typer.echo("\033[1;32;40m                 .o+`                    \033[1;37;40m-------------------")
    typer.echo("\033[1;32;40m                `ooo/                    \033[1;37;40mOS: " + os_name)
    typer.echo("\033[1;32;40m               `+oooo:                   \033[1;37;40mHost: " + host_info)
    typer.echo("\033[1;32;40m              `+oooooo:                  \033[1;37;40mKernel: " + os_version)
    typer.echo("\033[1;32;40m              -+oooooo+:                 \033[1;37;40mUptime: " + "3 hours, 53 mins")
    typer.echo("\033[1;32;40m            `/:-:++oooo+:                \033[1;37;40mPackages: 1360 (pacman), 10 (flatpak)")
    typer.echo("\033[1;32;40m           `/++++/+++++++:               \033[1;37;40mShell: " + shell_info)
    typer.echo("\033[1;32;40m          `/++++++++++++++:              \033[1;37;40mDisplay (BOE0868): 1920x1080 @ 60Hz")
    typer.echo("\033[1;32;40m         `/+++ooooooooooooo/`            \033[1;37;40mDE: " + de_info)
    typer.echo("\033[1;32;40m        ./ooosssso++osssssso+`           \033[1;37;40mWM: " + wm_info)
    typer.echo("\033[1;32;40m       .oossssso-````/ossssss+`          \033[1;37;40mWM Theme: Catppuccin-Frappe-Standard-Blue-Dark")
    typer.echo("\033[1;32;40m      -osssssso.      :ssssssso.         \033[1;37;40mTheme: Catppuccin-Frappe-Standard-Blue-Dark [GTK2/3/4]")
    typer.echo("\033[1;32;40m     :osssssss/        osssso+++.        \033[1;37;40mIcons: Papirus-Dark [GTK2/3/4]")
    typer.echo("\033[1;32;40m    /ossssssss/        +ssssooo/-        \033[1;37;40mFont: Noto Sans (10pt) [GTK2/3/4]")
    typer.echo("\033[1;32;40m  `/ossssso+/:-        -:/+osssso+-      \033[1;37;40mCursor: Qogir-dark (25px)")
    typer.echo("\033[1;32;40m `+sso+:-`                 `.-/+oso:     \033[1;37;40mTerminal: " + terminal_info)
    typer.echo("\033[1;32;40m`++:.                           `-/+/    \033[1;37;40mTerminal Font: Monospace (12pt)")
    typer.echo("\033[1;32;40m.`                                 `/    \033[1;37;40mCPU: " + cpu_model)
    typer.echo("                                         \033[1;37;40mGPU: " + gpu_info)
    typer.echo("                                         \033[1;37;40mMemory: " + f"{memory_used} / {memory_total} bytes ({memory_percent}%)")
    typer.echo("                                         \033[1;37;40mSwap: 0 B / 4.00 GiB (0%)")
    typer.echo("                                         \033[1;37;40mDisk (/): 51.34 GiB / 115.21 GiB (45%) - btrfs")
    typer.echo("                                         \033[1;37;40mLocal IP (wlp0s20f3): 192.168.1.34/24 *")
    typer.echo("                                         \033[1;37;40mBattery: 90% [Discharging]")
    typer.echo("                                         \033[1;37;40mLocale: en_US.UTF-8")
    typer.echo("\n                                         \033[1;37;40m████████████████████████")
    typer.echo("                                         \033[1;37;40m████████████████████████")

if __name__ == "__main__":
    app()
