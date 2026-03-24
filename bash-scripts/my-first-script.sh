#!/bin/bash

NAME="ubuntu_admin"
ROLE="DevOps Engineer"
DISK_LIMIT=80
LOG_FILE="/home/ubuntu_admin/DevOpsAcademy/bash-scripts/disk-check.log"

DISK_USED=$(df / | awk 'NR==2 {print $5}' | tr -d '%')
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] 👤 $NAME | 💼 $ROLE | 💾 Disk: $DISK_USED%" | tee -a $LOG_FILE

if [ $DISK_USED -gt $DISK_LIMIT ]; then
    echo "[$TIMESTAMP] ⚠️  WARNING: Disk ${DISK_USED}% exceeds limit of ${DISK_LIMIT}%" | tee -a $LOG_FILE
else
    echo "[$TIMESTAMP] ✅ Disk healthy at ${DISK_USED}%" | tee -a $LOG_FILE
fi
