FROM alpine:3.9

# Install packages
RUN apk --no-cache add curl sudo jq sshpass python3 bash git openssh

# Updating pip
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install beautifulsoup4
RUN python3 -m pip install requests
RUN python3 -m pip install flask
RUN python3 -m pip install flask-wtf


VOLUME ["/opt"]
CMD ["python3","/opt/start.py"]