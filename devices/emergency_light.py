"""
Emergency Light Emulator
This module simulates an IoT emergency light device. The device periodically
generates synthetic status updates (on/off) and publishes them as telemetry
events to an MQTT broker. The emergency light is part of the AQUA_SENSE safety
system.

"""
import paho.mqtt.client as mqtt
import time
import random
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
    logger = logging.getLogger("EmergencyLight")
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
# Function to publish emergency light status data
def publish_emergency_light_status():
    global mqtt_client, config, logger, stop_event
    topic = config.get('MQTT', 'topic', fallback='telemetry/emergency_light/{device_id}')
    interval = config.getint('SENSOR', 'interval', fallback=10)
    while not stop_event.is_set():
        status = random.choice(["ON", "OFF"])
        data = {
            "deviceId": config.get('DEVICE', 'id', fallback='emergency-light-01'),
            "deviceType": "emergency_light",
            "timestamp": datetime.utcnow().isoformat(),
            "status": status
        }
        payload = json.dumps(data)
        mqtt_client.publish(topic.format(device_id=data["deviceId"]), payload)
        logger.info(f"Published data: {payload}")
        time.sleep(interval)    

# Handle incoming commands
def on_message(client, userdata, msg):
    global logger
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        action = payload.get("action")
        reason = payload.get("reason", "")
        logger.info(f"Received command: action={action}, reason={reason}")
        print(f"[EmergencyLight] Command received: {action} (reason: {reason})")
    except Exception as exc:
        logger.error(f"Error processing command: {exc}")
# Main function
def main():
    global config, mqtt_client, logger, stop_event
    parser = argparse.ArgumentParser(description='Emergency Light Emulator')
    parser.add_argument('--config', type=str, default='config/emergency_light.ini', help='Path to configuration file')
    args = parser.parse_args()
    config = load_config(args.config)
    log_file = config.get('LOGGING', 'file', fallback='logs/emergency_light.log')
    log_level_str = config.get('LOGGING', 'level', fallback='INFO')
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)
    logger = setup_logging(log_file, log_level)
    broker = config.get('MQTT', 'broker', fallback='localhost')
    port = config.getint('MQTT', 'port', fallback=1883)
    username = config.get('MQTT', 'username', fallback=None)
    password = config.get('MQTT', 'password', fallback=None)
    mqtt_client = connect_mqtt(broker, port, username, password)
    # Subscribe to commands
    command_topic = config.get('MQTT', 'command_topic', fallback='commands/emergency_light/+')
    mqtt_client.subscribe(command_topic)
    mqtt_client.on_message = on_message
    mqtt_client.loop_start()
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    publisher_thread = threading.Thread(target=publish_emergency_light_status)
    publisher_thread.start()
    publisher_thread.join()
    mqtt_client.loop_stop()
# Signal handler for graceful shutdown
def signal_handler(sig, frame):
    global stop_event, logger
    logger.info("Shutdown signal received. Stopping emergency light emulator...")
    stop_event.set()
if __name__ == "__main__":
    main()