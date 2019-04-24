FROM alpine:3.9

# Install packages
RUN apk --no-cache add curl sudo jq sshpass python3 bash git

# Updating pip
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install beautifulsoup4
RUN python3 -m pip install requests

COPY test.py /opt/test.py
COPY global.vars.sh /opt/global.vars.sh
VOLUME ["/opt/"]
CMD ["python3","/opt/test.py"]