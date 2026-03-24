#!/usr/bin/env python3

import psutil
import subprocess
import datetime

# ─────────────────────────────────────
# FUNCTIONS — reusable blocks of code
# ─────────────────────────────────────

def get_timestamp():
    """Returns current date and time as a string"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def print_header():
    """Prints the report header"""
    print(f"\n{'='*50}")
    print(f"  SYSTEM HEALTH REPORT")
    print(f"  {get_timestamp()}")
    print(f"{'='*50}")

def check_disk():
    """Checks disk usage and returns a status"""
    disk = subprocess.run(['df', '-h', '/'], capture_output=True, text=True)
    lines = disk.stdout.strip().split('\n')
    disk_info = lines[1].split()

    used_pct = int(disk_info[4].replace('%',''))
    used = disk_info[2]
    total = disk_info[1]

    print(f"\n💾 DISK")
    print(f"   Used: {used} of {total} ({used_pct}%)")

    if used_pct > 80:
        print(f"   ⚠️  WARNING: Disk critical!")
        return "CRITICAL"
    elif used_pct > 60:
        print(f"   🟡 NOTICE: Disk filling up")
        return "WARNING"
    else:
        print(f"   ✅ Healthy")
        return "OK"

def check_memory():
    """Checks memory usage and returns a status"""
    mem = subprocess.run(['free', '-h'], capture_output=True, text=True)
    mem_info = mem.stdout.strip().split('\n')[1].split()

    total = mem_info[1]
    used = mem_info[2]
    free = mem_info[3]

    print(f"\n🧠 MEMORY")
    print(f"   Total: {total} | Used: {used} | Free: {free}")
    print(f"   ✅ Healthy")
    return "OK"

def check_cpu():
    """Checks CPU usage percentage"""
    cpu_pct = psutil.cpu_percent(interval=1)
    cpu_cores = psutil.cpu_count()

    print(f"\n⚡ CPU")
    print(f"   Cores: {cpu_cores} | Usage: {cpu_pct}%")

    if cpu_pct > 90:
        print(f"   ⚠️  WARNING: CPU overloaded!")
        return "CRITICAL"
    elif cpu_pct > 70:
        print(f"   🟡 NOTICE: CPU working hard")
        return "WARNING"
    else:
        print(f"   ✅ Healthy")
        return "OK"


def check_uptime():
    """Checks how long system has been running"""
    uptime = subprocess.run(['uptime', '-p'], capture_output=True, text=True)
    print(f"\n⏱️  UPTIME")
    print(f"   {uptime.stdout.strip()}")

def print_summary(results):
    """Prints overall system summary based on all checks"""
    print(f"\n{'─'*50}")
    print(f"  SUMMARY")
    print(f"{'─'*50}")

    if "CRITICAL" in results:
        print(f"  🔴 SYSTEM STATUS: CRITICAL — Action needed!")
    elif "WARNING" in results:
        print(f"  🟡 SYSTEM STATUS: WARNING — Keep an eye on this")
    else:
        print(f"  🟢 SYSTEM STATUS: ALL GOOD")

    print(f"{'='*50}\n")

# ─────────────────────────────────────
# MAIN — this is where the script runs
# ─────────────────────────────────────

def main():
    """Main function — runs all checks"""
    print_header()

    results = []
    results.append(check_disk())
    results.append(check_memory())
    results.append(check_cpu())
    check_uptime()

    print_summary(results)

# Entry point — only runs if called directly
if __name__ == "__main__":
    main()
