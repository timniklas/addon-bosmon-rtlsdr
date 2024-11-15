# Use an official Ubuntu base image
FROM ubuntu:22.04

# Avoid warnings by switching to noninteractive for the build process
ENV DEBIAN_FRONTEND=noninteractive

ENV USER=root

# Updates packages
RUN apt-get update

# Install XFCE, VNC server, dbus-x11, and xfonts-base, wget, Xvfb, Xte, jq
RUN apt-get install -y \
    jq \
    rtl-sdr \
    python3-aiohttp \
    multimon-ng

# clean up installers
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set the working directory in the container
WORKDIR /app

# Copy Bosmon
COPY bosmon.py bosmon.py
COPY bosmon.sh bosmon.sh
RUN chmod +x bosmon.sh

HEALTHCHECK --interval=5s \
  CMD pgrep -f "bosmon.py" || exit 1

ENTRYPOINT ["/app/bosmon.sh"]
