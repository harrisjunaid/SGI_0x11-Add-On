import logging
import json
import paho.mqtt.client as mqtt

# class is blueprint for objects, objects are instances of a class
############################################
# (object): inherited from base object class
## encapsulation: build data attributes and methods
## inheritance: class inherits attributes and methods from another class
class export_mqtt(object):
    def __init__(self): # constructor: __init__ is a special method in Python, known as a constructor. It is automatically called when an object of a class is created (instantiated). The purpose of __init__ is to initialize the object's attributes and set its initial state.
        self.mqtt_client = None # MQTT Client
        self.sensor_topic = None # Topic to publish to
        self.ha_discovery_published = False # Home Assistant Discovery Published for auto discovery
        self.mqtt_queue = [] # Queue of messages to be sent
        # Exclude ones linked to register lookups; unit_of_measurement
        # ha_variables relate to specific features of devices (like lights, fans, temperature, etc.) that HA can manage through MQTT.
        self.ha_variables = ["action_topic", "action_template", "automation_type", "aux_command_topic", "aux_state_template", "aux_state_topic", "available_tones", "availability", "availability_mode", "availability_topic", "availability_template", "away_mode_command_topic", "away_mode_state_template", "away_mode_state_topic", "blue_template", "brightness_command_topic", "brightness_command_template", "brightness_scale", "brightness_state_topic", "brightness_template", "brightness_value_template", "color_temp_command_template", "battery_level_topic", "battery_level_template", "charging_topic", "charging_template", "color_temp_command_topic", "color_temp_state_topic", "color_temp_template", "color_temp_value_template", "color_mode", "color_mode_state_topic", "color_mode_value_template", "cleaning_topic", "cleaning_template", "command_off_template", "command_on_template", "command_topic", "command_template", "code_arm_required", "code_disarm_required", "code_trigger_required", "current_temperature_topic", "current_temperature_template", "device", "device_class", "docked_topic", "docked_template", "encoding", "enabled_by_default", "entity_category", "entity_picture", "error_topic", "error_template", "fan_speed_topic", "fan_speed_template", "fan_speed_list", "flash_time_long", "flash_time_short", "effect_command_topic", "effect_command_template", "effect_list", "effect_state_topic", "effect_template", "effect_value_template", "expire_after", "fan_mode_command_template", "fan_mode_command_topic", "fan_mode_state_template", "fan_mode_state_topic", "force_update", "green_template", "hold_command_template", "hold_command_topic", "hold_state_template", "hold_state_topic", "hs_command_topic", "hs_state_topic", "hs_value_template", "icon", "image_encoding", "initial", "target_humidity_command_topic", "target_humidity_command_template", "target_humidity_state_topic", "target_humidity_state_template", "json_attributes", "json_attributes_topic", "json_attributes_template", "latest_version_topic", "latest_version_template", "last_reset_topic", "last_reset_value_template", "max", "min", "max_mireds", "min_mireds", "max_temp", "min_temp", "max_humidity", "min_humidity", "mode", "mode_command_template", "mode_command_topic", "mode_state_template", "mode_state_topic", "modes", "name", "object_id", "off_delay", "on_command_type", "options", "optimistic", "oscillation_command_topic", "oscillation_command_template", "oscillation_state_topic", "oscillation_value_template", "percentage_command_topic", "percentage_command_template", "percentage_state_topic", "percentage_value_template", "pattern", "payload", "payload_arm_away", "payload_arm_home", "payload_arm_custom_bypass", "payload_arm_night", "payload_arm_vacation", "payload_press", "payload_reset", "payload_available", "payload_clean_spot", "payload_close", "payload_disarm", "payload_home", "payload_install", "payload_lock", "payload_locate", "payload_not_available", "payload_not_home", "payload_off", "payload_on", "payload_open", "payload_oscillation_off", "payload_oscillation_on", "payload_pause", "payload_stop", "payload_start", "payload_start_pause", "payload_return_to_base", "payload_reset_humidity", "payload_reset_mode", "payload_reset_percentage", "payload_reset_preset_mode", "payload_turn_off", "payload_turn_on", "payload_trigger", "payload_unlock", "position_closed", "position_open", "power_command_topic", "power_state_topic", "power_state_template", "preset_mode_command_topic", "preset_mode_command_template", "preset_mode_state_topic", "preset_mode_value_template", "preset_modes", "red_template", "release_summary", "release_url", "retain", "rgb_command_topic", "rgb_command_template", "rgb_state_topic", "rgb_value_template", "rgbw_command_topic", "rgbw_command_template", "rgbw_state_topic", "rgbw_value_template", "rgbww_command_topic", "rgbww_command_template", "rgbww_state_topic", "rgbww_value_template", "send_command_topic", "send_if_off", "set_fan_speed_topic", "set_position_template", "set_position_topic", "position_topic", "position_template", "speed_range_min", "speed_range_max", "source_type", "state_class", "state_closed", "state_closing", "state_off", "state_on", "state_open", "state_opening", "state_stopped", "state_locked", "state_unlocked", "state_topic", "state_template", "state_value_template", "step", "subtype", "supported_color_modes", "support_duration", "support_volume_set", "supported_features", "swing_mode_command_template", "swing_mode_command_topic", "swing_mode_state_template", "swing_mode_state_topic", "temperature_command_template", "temperature_command_topic", "temperature_high_command_template", "temperature_high_command_topic", "temperature_high_state_template", "temperature_high_state_topic", "temperature_low_command_template", "temperature_low_command_topic", "temperature_low_state_template", "temperature_low_state_topic", "temperature_state_template", "temperature_state_topic", "temperature_unit", "tilt_closed_value", "tilt_command_topic", "tilt_command_template", "tilt_invert_state", "tilt_max", "tilt_min", "tilt_opened_value", "tilt_optimistic", "tilt_status_topic", "tilt_status_template", "title", "topic", "unique_id", "value_template", "white_command_topic", "white_scale", "white_value_command_topic", "white_value_scale", "white_value_state_topic", "white_value_template", "xy_command_topic", "xy_state_topic", "xy_value_template"] # Home Assistant Variables used for Discovery

    # Configure MQTT
    # Setup instance of a class using config and inverter parameters
    # self is a reference to the current instance of the class
    # config is a dictionary of configuration parameters
    # inverter is an instance of the inverter class 
    # 1) Retrive inverter model and serial number
    # 2) Retrive MQTT configuration parameters from config-examples.yaml
    # 3) Initialize Home Assistant Sensors
    # 4) Check if [host] is valid or None before creating MQTT Client
    # 5) Create MQTT Client from paho.mqtt.client
    # 5-A) MQTT Client Callbacks
    # 5-B) MQTT Client login credentials
    # 5-C) MQTT Client TLS if port is 8883
    # 6) Connect to MQTT Server
    # 7) Check if Home Assistant integration is enabled
    # 7-A) Add Home Assistant Sensor to ha_sensors list as in the config file
    def configure(self, config, inverter):
        # 1) Retrive inverter model and serial number
        self.model = inverter.getInverterModel(True) # Get Model method in inverter 
        #self.serial_number = inverter.getSerialNumber() # Get Serial Number below in get_valid_serial_number
        # Assuming a valid serial number is non-empty and not None
        def get_valid_serial_number(inverter):
            serial_number = None
            while not serial_number:
                serial_number = inverter.getSerialNumber()
                if serial_number:
                    logging.info(f"Valid serial number received: {serial_number}")
                else:
                    # write code for waiting for a valid serial number
                    logging.info("Invalid serial number, retrying...")
            return serial_number
        self.serial_number = get_valid_serial_number(inverter)



        logging.info(f"INVERTER SERIAL AND MODEL READ BY inverter.get...: Configuring {self.model} {self.serial_number}")
        # 2) Retrive MQTT configuration parameters from config-examples.yaml
        self.mqtt_config = {
            'host': config.get('host', None),
            'port': config.get('port', 1883),
            'username': config.get('username', None),
            'password': config.get('password',None),
            'client_id': config.get('client_id', f'0x01{self.serial_number}'),
            'topic': config.get('topic', f"SunGrow-Inverter-0x01/{self.serial_number}"),
            'homeassistant': config.get('homeassistant',False)
        }
        # 3) Initialize Home Assistant Sensors
        self.ha_sensors = [{}] # define instance variable ha_sensors as a list with one element, an empty dictionary
        self.ha_sensors.pop() # remove the last element from the list
        # 4) Check if [host] is valid or None before creating MQTT Client
        if not self.mqtt_config['host']:
            logging.info(f"MQTT: Host config is required")
            return False
        # 5) Create MQTT Client from paho.mqtt.client
        client_id = self.mqtt_config['client_id']  
        self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id) # Create a new instance of the client
        # 5-A) MQTT Client Callbacks
        self.mqtt_client.on_connect = self.on_connect  
        self.mqtt_client.on_disconnect = self.on_disconnect 
        self.mqtt_client.on_publish = self.on_publish 
        # 5-B) MQTT Client login credentials
        if self.mqtt_config['username'] and self.mqtt_config['password']:
            self.mqtt_client.username_pw_set(self.mqtt_config['username'], self.mqtt_config['password'])
        # 5-C) MQTT Client TLS if port is 8883
        if self.mqtt_config['port'] == 8883:
            self.mqtt_client.tls_set()
        # 6) Connect to MQTT Server
        self.mqtt_client.connect_async(self.mqtt_config['host'], port=self.mqtt_config['port'], keepalive=60)
        self.mqtt_client.loop_start() # Start a new thread to handle network traffic. Starts the background network loop, which allows the MQTT client to handle publishing and subscribing in a non-blocking way.
        # 7) Check if Home Assistant integration is enabled
        if self.mqtt_config['homeassistant']:
            for ha_sensor in config.get('ha_sensors'):
                if not inverter.validateRegister(ha_sensor['register']): # Check if register is valid in inverter
                    logging.error(f"MQTT: Configured to use {ha_sensor['register']} but not configured to scrape this register")
                    return False
                else: # Add Home Assistant Sensor to ha_sensors list
                    self.ha_sensors.append(ha_sensor)    
        return True

    # MQTT Callbacks
    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            logging.info(f"MQTT: Connected to {client._host}:{client._port}")
        if reason_code > 0:
            logging.warn(f"MQTT: FAILED to connect {client._host}:{client._port}")

    def on_disconnect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            logging.info(f"MQTT: Server Disconnected")
        if reason_code > 0:
            logging.warn(f"MQTT: FAILED to disconnect {reason_code}")
    # Remove message from queue when published    
    def on_publish(self, client, userdata, mid, reason_codes, properties):
        try:
            self.mqtt_queue.remove(mid)
        except Exception as err:
            pass
        logging.debug(f"MQTT: Message {mid} Published")
    # name to lower case and replace space with underscore
    def cleanName(self, name):
        return name.lower().replace(' ','_')

    def publish(self, inverter):
        # 1) Check if MQTT Server is connected
        #-------------------------------------------------------------------
        try:
            if not self.mqtt_client.is_connected():
                logging.warning(f'MQTT: Server Disconnected; {self.mqtt_queue.__len__()} messages queued, will automatically attempt to reconnect')
        except Exception as err:
            logging.warning(f'MQTT: Server Error; Server not configured')
            return False
        # qos=0 is set, so no acknowledgment is sent, rending this check useless
        #elif self.mqtt_queue.__len__() > 10:
        #    logging.warning(f'MQTT: {self.mqtt_queue.__len__()} messages queued, this may be due to a MQTT server issue')
       
        # 2) Check if Home Assistant Discovery is enabled and not already published
        #-------------------------------------------------------------------
        if self.mqtt_config['homeassistant'] and not self.ha_discovery_published: # discovery is Fasle on first run
            # Build Device, this will be the same for every message
            # HA discovery message info
            ha_device = { 
                "name": f"0x01 {self.model} {self.serial_number}", 
                "identifiers": [f"0x01{self.serial_number}"], 
                "manufacturer": "Sungrow", 
                "model": self.model, 
                "via_device": "SunGather",  # Ensure this is the correct device identifier
                # Uncomment and verify if needed:
                # "connections": [
                #     ["address", inverter.getHost()],  # Ensure getHost() returns a valid address
                #     ["port", inverter.getPort() or "0x01"]  # Assuming getPort() returns the correct port, otherwise handle it
                # ]
            }

            # 2-A) config_msg (payload) for each sensor in ha_sensors listed in config file
            for ha_sensor in self.ha_sensors: # list provided at the top
                config_msg = {} # define instance variable config_msg as a dictionary
                if not (ha_sensor.get('name', False) and ha_sensor.get('sensor_type', False)):
                    logging.error(f"HomeAssistance Discovery requires at minimum; name, sensor_type")
                    break

                # state_topic is the same as the main topic
                # value_template is the register value
                config_msg['state_topic'] = self.mqtt_config['topic']
                if ha_sensor.get('register', False):
                    config_msg['value_template'] = "{{ value_json." + ha_sensor.get('register') + " }}"
                # Add all HA variables
                for ha_variable in self.ha_variables: # list provided at the top
                    if ha_sensor.get(ha_variable):
                        config_msg[ha_variable] = ha_sensor[ha_variable]

                # Set unique_id, include Serial so is unique
                config_msg['unique_id'] = f"sungather_0x01_{self.cleanName(config_msg['name'])}_{self.serial_number}"

                # Variables with links to registers
                if ha_sensor.get('register', False):
                    if inverter.getRegisterUnit(ha_sensor.get('register')):
                        config_msg['unit_of_measurement'] = inverter.getRegisterUnit(ha_sensor.get('register'))
                
                config_msg['device'] = ha_device
            
                ha_topic = f"homeassistant/{ha_sensor.get('sensor_type')}/0x01{self.serial_number}_{self.cleanName(ha_sensor.get('name'))}/config"  #Discovery Topic: <discovery_prefix>/<component>/<object_id>/config
                logging.debug(f'MQTT: Topic; {ha_topic}, Message: {config_msg}')

                self.mqtt_queue.append(self.mqtt_client.publish(ha_topic, json.dumps(config_msg), qos=2, retain=True).mid) # append to mqtt_queue dictionary message (topic, payload, qos, retain)
            self.ha_discovery_published = True # discovery is True after first run
            logging.info("MQTT: Published Home Assistant Discovery messages")

        payload = json.dumps(inverter.inverter_config | inverter.client_config | inverter.latest_scrape).replace('"', '\"')
        logging.debug(f"MQTT: Publishing Registers: {self.mqtt_config['topic']} : {payload}")
        self.mqtt_queue.append(self.mqtt_client.publish(self.mqtt_config['topic'], payload, qos=0).mid)
        logging.info(f"MQTT: Registers Published")

        return True
