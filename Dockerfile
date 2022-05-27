### From https://www.embeddedonlineconference.com/theatre/Advantages_of_Docker_For_Firmware_Development

FROM ubuntu:20.04

LABEL maintainer="nathancharlesjones@gmail.com"

WORKDIR /app

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update

### Get GNU tools
RUN apt-get install -y build-essential gdb

### Get LLVM tools
RUN apt-get install -y clang lld llvm clang-tools

### Get gdbgui
RUN apt-get install -y python3-pip
RUN pip3 install gdbgui

### Get Arm GCC toolchain and add to PATH
RUN apt-get install -y wget
RUN cd /opt && wget -qO- https://developer.arm.com/-/media/Files/downloads/gnu-rm/10.3-2021.10/gcc-arm-none-eabi-10.3-2021.10-x86_64-linux.tar.bz2 | tar -xj
ENV PATH "/opt/gcc-arm-none-eabi-10.3-2021.10/bin:$PATH"
RUN apt-get install -y libncurses5  # Required for arm-none-eabi-gdb

### Get Ninja
RUN apt-get install -y python3-pip
RUN apt-get install -y ninja-build
RUN pip3 install ninja_syntax

###################################################
##                                               ##
##    Notes                                      ##
##                                               ##
###################################################

### Get other useful tools, like CMake or zip
# RUN pip3 install cmake
# RUN apt-get install -y zip

### Get sample dependency (mpaland/printf)
# RUN apt-get install -y git
# RUN cd /tmp && git clone https://github.com/mpaland/printf.git
### User must then copy that folder (and any others) to the correct location once a container is built and started
### Note: "cp -a /tmp/. /app" copies all files and directories (recursively) from inside tmp to app

### Run a command/program on Docker startup
### From: https://nolambda.stream/posts/docker-startup-script/
### If you need to run a command each time the container starts up AND ALSO would like to run commands from
### the interactive mode, like above, then add the following two lines to the Dockerfile:
# COPY entrypoint.sh /bin/entrypoint.sh
# ENTRYPOINT [ "entrypoint.sh" ]
### Create a file in the same folder as your Dockerfile with the following contents:

# #!/usr/bin/env bash
# set -e

# Run startup command, such as: 
# echo "Hello"

# Running passed command
# if [[ "$1" ]]; then
#	eval "$@"
# fi

### Setting the entrypoint of the container to this script means that it runs every time the container 
### starts. It's written in such a way that it will execute the startup command (every time), and also 
### another command if one was specified.