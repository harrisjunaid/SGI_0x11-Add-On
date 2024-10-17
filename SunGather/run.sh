#!/usr/bin/with-contenv bashio
# 1) Setup directories and copying config-0x01.yaml on HAOS
# 2) Get configuration from the add-on and apply to config-0x01.yaml
# 2-A) Inverter, hassio, log_console, log_file, webserver, mqtt
# 3) Activate the virtual environment and run the script sungather.py
#--------------------------------------------------

# 1) Setup directories and copying config-0x01.yaml on HAOS
#--------------------------------------------------
if [ ! -d /share/SunGather ]; then
  mkdir -p /share/SunGather
fi

if [ ! -f /share/SunGather/config-0x01.yaml ]; then
    cp config-hassio.yaml /share/SunGather/config-0x01.yaml
fi

# Reading config.yaml and setting up the variables. config.yaml is Add-on specific and is used to set up the configuration for the script
#--------------------------------------------------
INVERTER_HOST=$(bashio::config 'host')
CONNECTION=$(bashio::config 'connection')
INVERTER_PORT=$(bashio::config 'port')
MODEL=$(bashio::config 'model')
INTERVAL=$(bashio::config 'scan_interval')
SMART_METER=$(bashio::config 'smart_meter')
CUSTOM_MQTT_SERVER=$(bashio::config 'custom_mqtt_server')
LOG_CONSOLE=$(bashio::config 'log_console')
LOG_FILE=$(bashio::config 'log_file')

# yq is a tool to manipulate yaml files similar to jq for json files
# .section.variable = value
# -i is for inplace editing of the file specified
yq -i "
  .inverter.host = \"$INVERTER_HOST\" |
  .inverter.connection = \"$CONNECTION\" |
  .inverter.port = $INVERTER_PORT |
  .inverter.model = \"$MODEL\" |
  .inverter.smart_meter = $SMART_METER |
  .inverter.scan_interval = $INTERVAL |
  .inverter.log_console = \"$LOG_CONSOLE\" |
  .inverter.log_file = \"$LOG_FILE\"
" /share/SunGather/config-0x01.yaml

yq -i "
  (.exports[] | select(.name == \"hassio\") | .enabled) = True |
  (.exports[] | select(.name == \"hassio\") | .api_url) = \"http://supervisor/core/api\" |
  (.exports[] | select(.name == \"hassio\") | .token) = \"$SUPERVISOR_TOKEN\"
" /share/SunGather/config-0x01.yaml

# .exports[] to access the array of exports in the config file, | is used to chain commands, select() is used to filter the array based on the name of the export, .variable = value is used to set the value of the variable
yq -i "
  (.exports[] | select(.name == \"webserver\") | .enabled) = True |
  (.exports[] | select(.name == \"webserver\") | .port) = 8099
" /share/SunGather/config-0x01.yaml

if [ $CUSTOM_MQTT_SERVER = true ]; then #custom MQTT details are in /share/SunGather/config-0x01.yaml
   echo "Skipping auto MQTT set up, please ensure MQTT settings are configured in /share/SunGather/config-0x01.yaml"
else
  # In case CUSTOM_MQTT_SERVER is not set, we will use the internal MQTT broker
  if ! bashio::services.available "mqtt"; then
    bashio::exit.nok "No internal MQTT Broker found. Please install Mosquitto broker."
  else # if MQTT is available and no custom MQTT
    # Utility functions in Home Assistant OS
    # Assign values from bashio
    # Retrieve custom configuration settings specified by the user in the add-on
    MQTT_HOST=$(bashio::services mqtt "host")
    MQTT_PORT=$(bashio::services mqtt "port")
    MQTT_USER=$(bashio::services mqtt "username")
    MQTT_PASS=$(bashio::services mqtt "password")
    MQTT_DEVICE_MODEL=$(bashio::services mqtt "model")
    MQTT_DEVICE_IDENTIFIERS=$(bashio::services mqtt "serial")

    # Update the config in one yq command
    yq -i "
      (.exports[] | select(.name == "mqtt") | .enabled) = true |
      (.exports[] | select(.name == "mqtt") | .host) = \"$MQTT_HOST\" |
      (.exports[] | select(.name == "mqtt") | .port) = $MQTT_PORT |
      (.exports[] | select(.name == "mqtt") | .username) = \"$MQTT_USER\" |
      (.exports[] | select(.name == "mqtt") | .password) = \"$MQTT_PASS\" |
      (.exports[] | select(.name == "mqtt") | .homeassistant) = true |
      (.exports[] | select(.name == "mqtt") | .mqtt.device.model) = \"$MQTT_DEVICE_MODEL\" |
      (.exports[] | select(.name == "mqtt") | .mqtt.device.identifiers) = \"$MQTT_DEVICE_IDENTIFIERS\"
    " /share/SunGather/config-0x01.yam

      fi
    fi



# Activate the virtual environment and run the script
#--------------------------------------------------
source ./venv/bin/activate
exec python3 /sungather.py -c /share/SunGather/config-0x01.yaml -l /share/SunGather/ # -c is for config file, -l is for log file