on host:
1. docker run -t -d --privileged --network host --name esp32-comms ubuntu
2. docker exec -it esp32-comms /bin/bash

in container:
1. apt-get update && apt-get upgrade -y && apt autoremove -y
2. DEBIAN_FRONTEND=noninteractive apt install python3 python3-pip git htop nano curl wget python3-serial -y
3. pip3 install esptool --break-system-packages
