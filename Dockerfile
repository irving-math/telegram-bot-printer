FROM ubuntu
MAINTAINER Dave Burke "dburke84@gmail.com"

# Install cups
RUN apt-get update
RUN apt-get install --quiet --assume-yes --allow-downgrades --allow-remove-essential --allow-change-held-packages cups printer-driver-gutenprint
RUN useradd admin --system -G root,lpadmin --no-create-home --password $(perl -e'print crypt("admin", "admin")')
COPY cupsd.conf /etc/cups/cupsd.conf

EXPOSE 631

CMD ["/usr/sbin/cupsd", "-f"]

