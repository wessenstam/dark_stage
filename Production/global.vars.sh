#!/usr/bin/env bash

RELEASE='release.json'
PC_DEV_VERSION='5.10.2'
PC_DEV_METAURL='http://download.nutanix.com/pc/one-click-pc-deployment/5.10.2/pcdeploy-5.10.2.json'
PC_DEV_URL=''
PC_CURRENT_VERSION='5.10.2'
PC_STABLE_VERSION='5.8.2'
FILES_VERSION='3.2.0.1'
NTNX_INIT_PASSWORD='nutanix/4u'
PRISM_ADMIN='admin'
SSH_PUBKEY="${HOME}/.ssh/id_rsa.pub"
STORAGE_POOL='SP01'
STORAGE_DEFAULT='Default'
STORAGE_IMAGES='Images'

QCOW2_IMAGES=(\
   CentOS7.qcow2 \
   Windows2016.qcow2 \
   Windows2012R2.qcow2 \
   Windows10-1709.qcow2 \
   ToolsVM.qcow2 \
   ERA-Server-build-1.0.1.qcow2 \
   'http://download.nutanix.com/karbon/0.8/acs-centos7.qcow2' \
)

ISO_IMAGES=(\
   CentOS7.iso \
   Windows2016.iso \
   Windows2012R2.iso \
   Windows10.iso \
   Nutanix-VirtIO-1.1.3.iso \
   SQLServer2014SP3.iso \
   XenApp_and_XenDesktop_7_18.iso \
)

OCTET=(${PE_HOST//./ }) # zero index
IPV4_PREFIX=${OCTET[0]}.${OCTET[1]}.${OCTET[2]}
DATA_SERVICE_IP=${IPV4_PREFIX}.$((${OCTET[3]} + 1))
PC_HOST=${IPV4_PREFIX}.$((${OCTET[3]} + 2))
DNS_SERVERS='8.8.8.8'
NTP_SERVERS='0.us.pool.ntp.org,1.us.pool.ntp.org,2.us.pool.ntp.org,3.us.pool.ntp.org'

# Network related settings
NW1='NETWORK1'
NW1_OCTET=(${NW1//./ })
NW1_IPV4_PREFIX=${NW1_OCTET[0]}.${NW1_OCTET[1]}.${NW1_OCTET[2]}
NW1_NAME='Primary'
NW1_VLAN='0'
NW1_SUBNET="${NW1}/NW_1_SUBNET"
NW1_DHCP_START="${NW1_IPV4_PREFIX}.50"
NW1_DHCP_END="${NW1_IPV4_PREFIX}.70"

NW2='NETWORK2'
NW2_OCTET=(${NW2//./ })
NW2_IPV4_PREFIX=${NW2_OCTET[0]}.${NW2_OCTET[1]}.${NW2_OCTET[2]}
NW2_NAME='Secondary'
NW2_VLAN='NW_2_VLAN'
NW2_SUBNET="${NW2}/NW_2_SUBNET"
NW2_DHCP_START="${NW2_IPV4_PREFIX}.150"
NW2_DHCP_END="${NW2_IPV4_PREFIX}.170"


# https://sewiki.nutanix.com/index.php/Hosted_POC_FAQ#I.27d_like_to_test_email_alert_functionality.2C_what_SMTP_server_can_I_use_on_Hosted_POC_clusters.3F
#SMTP_SERVER_ADDRESS='nutanix-com.mail.protection.outlook.com'
#SMTP_SERVER_ADDRESS='mxb-002c1b01.gslb.pphosted.com'
#SMTP_SERVER_FROM='NutanixHostedPOC@nutanix.com'
#SMTP_SERVER_PORT=25

# Authentication settings
AUTH_SERVER='AutoDC' # default; TODO:180 refactor AUTH_SERVER choice to input file
AUTH_HOST="${IPV4_PREFIX}.$((${OCTET[3]} + 3))"
LDAP_PORT=389
AUTH_FQDN='ntnxlab.local'
AUTH_DOMAIN='NTNXLAB'
AUTH_ADMIN_USER='administrator@'${AUTH_FQDN}
AUTH_ADMIN_PASS='nutanix/4u'
AUTH_ADMIN_GROUP='SSP Admins'

# PRISM Central settings
PC_CURRENT_METAURL='http://IMAGE_SERVER/IMAGE_LOCATION/pcdeploy-5.10.2.json'
PC_CURRENT_URL='http://IMAGE_SERVER/IMAGE_LOCATION/euphrates-5.10.2-stable-prism_central.tar'
PC_STABLE_METAURL='http://IMAGE_SERVER/IMAGE_LOCATION/pc_deploy-5.8.2.json'
PC_STABLE_URL='http://IMAGE_SERVER/IMAGE_LOCATION/euphrates-5.8.2-stable-prism_central.tar'
FILES_METAURL='http://IMAGE_SERVER/IMAGE_LOCATION/nutanix-afs-el7.3-release-afs-3.2.0.1-stable-metadata.json'
FILES_URL='http://IMAGE_SERVER/IMAGE_LOCATION/nutanix-afs-el7.3-release-afs-3.2.0.1-stable.qcow2'
JQ_REPOS=(\
         'http://IMAGE_SERVER/IMAGE_LOCATION/jq-linux64.dms' \
         'https://s3.amazonaws.com/get-ahv-images/jq-linux64.dms' \
)
SSHPASS_REPOS=(\
       'http://IMAGE_SERVER/IMAGE_LOCATION/sshpass-1.06-2.el7.x86_64.rpm' \
)
QCOW2_REPOS=(\
       'http://IMAGE_SERVER/IMAGE_LOCATION/' \
       'https://s3.amazonaws.com/get-ahv-images/jq-linux64.dms' \
)
AUTODC_REPOS=(\
     'http://IMAGE_SERVER/IMAGE_LOCATION/AutoDC.qcow2' \
  'http://IMAGE_SERVER/IMAGE_LOCATION/AutoDC2.qcow2' \
  'https://s3.amazonaws.com/get-ahv-images/AutoDC.qcow2' \
  'https://s3.amazonaws.com/get-ahv-images/AutoDC2.qcow2' \
)

# General parameters for the script
HTTP_CACHE_HOST='localhost'
HTTP_CACHE_PORT=8181

   ATTEMPTS=40
      SLEEP=60 # pause (in seconds) between ATTEMPTS

     CURL_OPTS='--insecure --silent --show-error' # --verbose'
CURL_POST_OPTS="${CURL_OPTS} --max-time 5 --header Content-Type:application/json --header Accept:application/json --output /dev/null"
CURL_HTTP_OPTS="${CURL_POST_OPTS} --write-out %{http_code}"
      SSH_OPTS='-o StrictHostKeyChecking=no -o GlobalKnownHostsFile=/dev/null -o UserKnownHostsFile=/dev/null'
     SSH_OPTS+=' -q' # -v'

# Find operating system and set dependencies
if [[ -e /etc/lsb-release ]]; then
  # Linux Standards Base
  OS_NAME="$(grep DISTRIB_ID /etc/lsb-release | awk -F= '{print $2}')"
elif [[ -e /etc/os-release ]]; then
  # CPE = https://www.freedesktop.org/software/systemd/man/os-release.html
  OS_NAME="$(grep '^ID=' /etc/os-release | awk -F= '{print $2}')"
elif [[ $(uname -s) == 'Darwin' ]]; then
  OS_NAME='Darwin'
fi

WC_ARG='--lines'
if [[ ${OS_NAME} == 'Darwin' ]]; then
  WC_ARG='-l'
fi
if [[ ${OS_NAME} == 'alpine' ]]; then
  WC_ARG="-l"
fi
