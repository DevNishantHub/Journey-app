#!/usr/bin/env python
"""
Background Worker Script for DevOps Journey App
This script runs in an infinite loop and is suitable for deployment
as a Render background worker.

Can be used to run periodic tasks without relying on Flask's scheduler.
"""

import os
import sys
import time
import signal
import logging
from datetime import datetime
import traceback

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("journey_worker")

# Flag to control the main loop
running = True

def signal_handler(sig, frame):
    """Handle termination signals to exit gracefully"""
    global running
    logger.info("Signal received. Worker shutting down...")
    running = False

# Register signal handlers for graceful shutdown
signal.signal(signal.SIGINT, signal_handler)  # Handles Ctrl+C
signal.signal(signal.SIGTERM, signal_handler)  # Handles termination signal

def run_tasks():
    """
    Run scheduled tasks here.
    This function is called every cycle of the worker.
    """
    try:
        # Import here to avoid circular imports and ensure fresh imports each time
        from src.main import send_daily_reminder

        now = datetime.now()
        
        # Example: Run daily reminder at 8 AM
        if now.hour == 8 and now.minute < 10:
            logger.info("Running daily email reminder task...")
            send_daily_reminder()
            logger.info("Daily reminder task completed.")
        
        # You can add more scheduled tasks here
        
    except Exception as e:
        logger.error(f"Error running tasks: {e}")
        logger.error(traceback.format_exc())

def main():
    """Main worker function that runs in a loop"""
    logger.info("Journey App Worker starting...")
    
    try:
        cycle_count = 0
        
        while running:
            cycle_count += 1
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Worker running... [Cycle: {cycle_count}, Time: {current_time}]")
            
            # Run scheduled tasks
            run_tasks()
            
            # Sleep for 10 seconds before next cycle
            # Using small sleep intervals to check running flag frequently
            for _ in range(10):
                if not running:
                    break
                time.sleep(1)
                
    except Exception as e:
        logger.error(f"Unexpected error in worker: {e}")
        logger.error(traceback.format_exc())
        return 1
    
    logger.info("Worker has stopped.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
