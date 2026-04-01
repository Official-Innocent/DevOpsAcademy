#!/usr/bin/env python3
import os
import psutil
import datetime

# Read from environment variables
dev_name = os.getenv('DEVELOPER_NAME', 'Unknown')
environment = os.getenv('ENVIRONMENT', 'unknown')
version = os.getenv('APP_VERSION', '0.0')

print(f"{'='*50}")
print(f"  DevOps Monitor v{version}")
print(f"  Developer: {dev_name}")
print(f"  Environment: {environment}")
print(f"  Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"{'='*50}")

cpu = psutil.cpu_percent(interval=1)
mem = psutil.virtual_memory()

print(f"\n⚡ CPU Usage: {cpu}%")
print(f"🧠 Memory: {mem.percent}% used")
print(f"\n✅ Container is healthy!")
print(f"{'='*50}\n")
# comment
