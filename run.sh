#!/bin/bash

name="printerbot"
cid="$(docker ps -q --filter "name=${name}")"
if [ -n "${cid}" ]; then
	echo "Stopping container..."
	docker stop "${name}" > /dev/null
fi
cid="$(docker ps -a -q --filter "name=${name}")"
if [ -n "${cid}" ]; then
	echo "Removing container..."
	docker rm "${name}" > /dev/null
fi

echo "Running container..."
docker run --name ${name} --detach --restart=always --privileged --volume /dev/bus/usb:/dev/bus/usb --mount source=cups-conf,destination=/etc/cups --publish 631:631 ${name}
