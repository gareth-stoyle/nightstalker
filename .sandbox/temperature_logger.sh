#!/bin/bash


mkdir -p logs

log_file="logs/$(date +"%Y-%m-%d")-temperature_log.txt"

while true; do
    temperature=$(vcgencmd measure_temp | cut -d "=" -f2)
    voltage=$(vcgencmd measure_volts)
    arm_clock=$(vcgencmd measure_clock arm)
    gpu_memory=$(vcgencmd get_mem gpu)
    throttled=$(vcgencmd get_throttled)

    timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    log_entry="$timestamp - Temperature: $temperature, Voltage: $voltage, ARM Clock: $arm_clock, GPU Memory: $gpu_memory, Throttled: $throttled"

    echo "$log_entry" >> "$log_file"
    echo "System information logged."

    # Log temperature every 2 minutes
    sleep 120
done
