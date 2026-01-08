"""
Rain sensor Emulator that publishes rain data to an MQTT broker.

This modlue imulates an IOT rain sensor. The device periodically generates systhetic rainfall
mesurements and publish them as a telemetry events to an MQTT broker. The sensro is 
a fundamental part os athe AQUA_SENSE project, which aims to monitor and manage water resources  


"""
import paho.mqtt.client as mqtt
import time
import random
import json
import threading
import logging
from configparser import ConfigParser
import os
from datetime import datetime
import sys
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
    logger = logging.getLogger("RainSensor")
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
# Function to publish rain data
def publish_rain_data():
    global mqtt_client, config, logger, stop_event
    topic = config.get('MQTT', 'topic', fallback='telemetry/rain/{device_id}')
    interval = config.getint('SENSOR', 'interval', fallback=10)
    while not stop_event.is_set():
        rain_mm = random.randint(0, 100)
        data = {
            "deviceId": config.get('DEVICE', 'id', fallback='rain-01'),
            "deviceType": "rain_sensor",
            "timestamp": datetime.utcnow().isoformat(),
            "rain_mm": rain_mm
        }
        payload = json.dumps(data)
        mqtt_client.publish(topic.format(device_id=data["deviceId"]), payload, qos=1)
        logger.info(f"Published rain data: {payload} to topic: {topic}")
        stop_event.wait(interval)
# Signal handler for graceful shutdown
def signal_handler(sig, frame):
    global stop_event, logger
    logger.info("Shutdown signal received. Stopping rain sensor...")
    stop_event.set()
# Main function         
def main():
    global config, mqtt_client, logger
    parser = argparse.ArgumentParser(description='Rain Sensor MQTT Publisher')
    parser.add_argument('--config', type=str, default='config.ini', help='Path to configuration file')
    args = parser.parse_args()
    config_file = args.config
    config = load_config(config_file)
    log_file = config.get('LOGGING', 'log_file', fallback='rain_sensor.log')
    log_level_str = config.get('LOGGING', 'log_level', fallback='INFO').upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    logger = setup_logging(log_file, log_level)
    mqtt_broker = config.get('MQTT', 'broker', fallback='localhost')
    mqtt_port = config.getint('MQTT', 'port', fallback=1883)
    mqtt_username = config.get('MQTT', 'username', fallback=None)
    mqtt_password = config.get('MQTT', 'password', fallback=None)
    mqtt_client = connect_mqtt(mqtt_broker, mqtt_port, mqtt_username, mqtt_password)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    logger.info("Starting rain sensor...")
    publish_thread = threading.Thread(target=publish_rain_data)
    publish_thread.start()
    publish_thread.join()
    logger.info("Rain sensor stopped.")
if __name__ == "__main__":
    main()
    