# Notes from https://www.embeddedonlineconference.com/theatre/Advantages_of_Docker_For_Firmware_Development

FROM ubuntu:20.04

LABEL maintainer="nathancharlesjones@gmail.com"

WORKDIR /app

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update

# Get GNU tools
RUN apt-get install -y build-essential gdb

# Get LLVM tools
RUN apt-get install -y clang lld llvm clang-tools

# Get gdbgui
# Usage: Start container with "-p 5000:5000" to expose port 5000 (the default port for gdbgui) to the
# host machine. Run gdbgui from inside container with "gdbgui -r ./myprogram" to expose the gdbgui server 
# to the host machine. Then you can connect to gdbgui from the host machine by navigating to 
# "localhost:5000" from a web browser. If port 5000 doesn't work, you can tell gdbgui to use a different
# port with "gdbgui --port ####". Make sure to start the container with this new port number, if you do.
RUN apt-get install -y python3-pip
RUN pip3 install gdbgui

# Get Arm GCC toolchain and add to PATH
RUN apt-get install -y wget
RUN cd /opt && wget -qO- https://developer.arm.com/-/media/Files/downloads/gnu-rm/10.3-2021.10/gcc-arm-none-eabi-10.3-2021.10-x86_64-linux.tar.bz2 | tar -xj
ENV PATH "/opt/gcc-arm-none-eabi-10.3-2021.10/bin:$PATH"
RUN apt-get install -y libncurses5  # Required for arm-none-eabi-gdb

# Get CMake
RUN apt-get install -y python3-pip
RUN pip3 install cmake

# Get Ninja
RUN apt-get install -y ninja-build
RUN pip3 install ninja_syntax

# Get other useful tools
RUN apt-get install -y zip
RUN apt-get install -y git
#RUN apt-get install -y docker

# Get sample dependency (mpaland/printf)
# User must copy this folder (and any others) to the correct location once a container is built and started
# Note to self: "cp -a /tmp/. /app" copies all files and directories (recursively) from inside tmp to app
RUN cd /tmp && git clone https://github.com/mpaland/printf.git

# 1) Build docker image with:
#  - "cd /folder/where/Dockerfile/lives"
#  - "docker build -f Dockerfile -t <NAME> .", where NAME is something like "devenv-simple-build-system"
# 2) Start the container, run a command, and stop the container with:
#  - "docker run -it --rm -v ${PWD}:/app <NAME> /bin/bash -c "<CMD>""
#  - Or "docker run -it --rm -v ${PWD}:/app -p 5000:5000 <NAME> /bin/bash -c "<CMD>"" if you're intending
#    to connect to gdbgui.
#  - "/app" should match the value of WORKDIR defined in the Dockerfile above
#  - Use the same NAME as in the first step; CMD is the shell command you want executed like "ls" or "make"
#  - This starts the container in interactive mode, mounting the current working directory on the host
#    machine to "/app", the working directory, in the container.
# 3) Alternatively, you can start the container and get to a shell (without closing) with:
#  - "docker run -it --rm -v ${PWD}:/app <NAME> /bin/bash"

# From: https://nolambda.stream/posts/docker-startup-script/
# If you need to run a command each time the container starts up AND ALSO would like to run commands from
# the interactive mode, like above, then add the following two lines to the Dockerfile:
# COPY entrypoint.sh /bin/entrypoint.sh
# ENTRYPOINT [ "entrypoint.sh" ]
# Create a file in the same folder as your Dockerfile with the following contents:

# #!/usr/bin/env bash
# set -e

# Run startup command, such as: 
# echo "Hello"

# Running passed command
# if [[ "$1" ]]; then
#	eval "$@"
# fi

# Setting the entrypoint of the container to this script means that it runs every time the container 
# starts. It's written in such a way that it will execute the startup command (every time), and also 
# another command if one was specified.
