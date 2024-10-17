# Executed first time the add-on is installed as well as every time the add-on is started. Used to build the add-on container.
#--------------------------------------------------------------------------------
# 1) Build architecture and install requirements
# 2) Prepare venv
# 3) Copy ./SunGather/, config-hassio.yaml 
# 4) Run run.sh
# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile

# 1) Build architecture and install requirements
###############################################################################
# Build time arguments to pass version and architecture to the Docker build process (not available in final image)
ARG BUILD_FROM 
FROM $BUILD_FROM

ARG BUILD_VERSION
ARG BUILD_ARCH

COPY requirements.txt ./
RUN apk add --no-cache py3-pip yq
# pycryptodomex 3.14 currently fails to compile for arm64

# 2) Prepare venv
###############################################################################
RUN python3 -m venv venv

RUN source ./venv/bin/activate && \
    pip install --no-cache-dir --upgrade -r requirements.txt
#RUN pip install --no-cache-dir --upgrade pycryptodomex==3.11.0 -r requirements.txt

# 3) Copy ./SunGather/, config-hassio.yaml and run.sh to the root of the container
###############################################################################
COPY ./SunGather/ /
COPY config-hassio.yaml /
COPY run.sh /

# 4) Run run.sh
RUN chmod a+x /run.sh
CMD ["/run.sh"]

# metadata
LABEL \ 
    io.hass.name="SunGather" \
    io.hass.description="Extract Sungrow data from local Inverter" \
    io.hass.version=${BUILD_VERSION} \
    io.hass.type="addon" \
    io.hass.arch=${BUILD_ARCH}