"""
Notification Hub Actuator

This actuator module simulates an IoT notification hub device. That recive alert messages, simulates 
the sent of messages via email/SMS/App. Only prints a single and simple message. The use of MQTT
as communication protocol allows easy integration with other AQUA_SENSE components.
Used as part of the AQUA_SENSE alerting system to notify users of critical events.
"""
import paho.mqtt.client as mqtt
import time
import json
import threading
import logging
from configparser import ConfigParser
from datetime import datetime
import signal
import argparse
from logging.handlers import RotatingFileHandler
# Global variables
config = None
mqtt_client = None
logger = None
stop_event = threading.Event()
# Function to load configuration
def load_config(config_file):
    parser = ConfigParser()
    parser.read(config_file)
    return parser
# Function to setup logging
def setup_logging(log_file, log_level):
    logger = logging.getLogger("NotificationHub")
    logger.setLevel(log_level)
    handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=3)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
# Function to connect to MQTT broker
def connect_mqtt(broker, port, username, password):
    client = mqtt.Client()
    if username and password:
        client.username_pw_set(username, password)
    client.connect(broker, port, 60)
    return client
# Callback function to handle incoming messages
def on_message(client, userdata, msg):
    global logger
    try:
        payload = msg.payload.decode('utf-8')
        data = json.loads(payload)
        device_id = data.get("deviceId", "unknown")
        alert_type = data.get("alertType", "general")
        message = data.get("message", "")
        logger.info(f"Notification received from {device_id} - Type: {alert_type} - Message: {message}")
        print(f"[{datetime.utcnow().isoformat()}] Notification from {device_id}: {message} (Type: {alert_type})")
    except Exception as e:
        logger.error(f"Error processing message: {e}")
# Function to start listening for notifications
def start_listening():
    global mqtt_client, config, logger, stop_event
    topic = config.get('MQTT', 'topic', fallback='alerts/#')
    mqtt_client.subscribe(topic)
    mqtt_client.on_message = on_message
    logger.info(f"Subscribed to topic: {topic}")
    while not stop_event.is_set():
        mqtt_client.loop(timeout=1.0)
# Signal handler for graceful shutdown
def signal_handler(sig, frame):
    global stop_event, logger
    logger.info("Shutdown signal received. Stopping Notification Hub...")
    stop_event.set()
# Main function
def main():
    global config, mqtt_client, logger, stop_event
    parser = argparse.ArgumentParser(description="Notification Hub Actuator")
    parser.add_argument('--config', type=str, default='config/notification_hub.ini', help='Path to configuration file')
    args = parser.parse_args()
    config = load_config(args.config)
    log_file = config.get('LOGGING', 'file', fallback='logs/notification_hub.log')
    log_level_str = config.get('LOGGING', 'level', fallback='INFO').upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    logger = setup_logging(log_file, log_level)
    broker = config.get('MQTT', 'broker', fallback='localhost')
    port = config.getint('MQTT', 'port', fallback=1883)
    username = config.get('MQTT', 'username', fallback=None)
    password = config.get('MQTT', 'password', fallback=None)
    mqtt_client = connect_mqtt(broker, port, username, password)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    logger.info("Starting Notification Hub Actuator...")
    try:
        start_listening()
    except Exception as e:
        logger.error(f"Error in main loop: {e}")
    finally:
        mqtt_client.disconnect()
        logger.info("Notification Hub Actuator stopped.")
if __name__ == "__main__":
    main()