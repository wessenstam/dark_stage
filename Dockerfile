FROM alpine:3.9

# Install packages
RUN apk --no-cache add curl sudo jq sshpass python3

# Updating pip
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install sphinx

COPY test.py /opt/test.py
CMD ["python3","/opt/test.py"]