FROM ubuntu:latest
MAINTAINER Irving Flores "superirv@gmail.com"

# Args
ARG USER_CUPS=admin
ARG PASS_CUPS=admin
ARG PORT_CUPS=631

# Install dependencies
RUN apt-get update
RUN apt-get upgrade --assume-yes
RUN apt-get install --quiet --assume-yes cups printer-driver-gutenprint cups-bsd
RUN apt-get install --quiet --assume-yes python3-pip

# Config users
COPY scripts/encrypt_pass.pl encrypt_pass.pl
RUN useradd -m $USER_CUPS --system -G root,lpadmin --password $(perl encrypt_pass.pl $USER_CUPS $PASS_CUPS)
RUN usermod -a -G lpadmin root
#Config cups
VOLUME /etc/cups
COPY configuration_files/cupsd.conf /etc/cups/cupsd.conf

# Install TelegramBotPrinter
RUN mkdir /home/documents_downloaded
COPY TelegramBotPrinter/ /home/TelegramBotPrinter/
WORKDIR /home/TelegramBotPrinter
RUN pip3 install .

EXPOSE $PORT_CUPS

# Start
COPY scripts/start.sh start.sh
RUN chmod +x start.sh
CMD ["/bin/bash", "./start.sh"]
