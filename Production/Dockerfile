FROM alpine:3.9

# Install packages
RUN apk --no-cache add curl sudo jq sshpass python3 bash git openssh

# Updating pip
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install beautifulsoup4
RUN python3 -m pip install requests

# Grab the latest github from the site
RUN mkdir -p /opt/github && cd /opt/github && git clone https://github.com/jncox/stageworkshop.git


COPY stagescript.py /opt/stagescript.py
COPY global.vars.sh /opt/global.vars.sh

VOLUME ["/tmp"]
CMD ["python3","/opt/stagescript.py"]