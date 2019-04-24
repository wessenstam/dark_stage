import requests
import os
from bs4 import BeautifulSoup
import json
import urllib3

urllib3.disable_warnings()
#####################################################################################################################################################################
# Scrape the images from the webserver that has been defined in the input by the user
#####################################################################################################################################################################
def webscrap_image_server(image_server,images_dir):
    # Start the search of images we can use on the images server
    url="http://"+image_server+"/"+images_dir+"/"

    # Use BeatifullSoup to scrape the webserver of the images
    page=requests.get(url,verify=False)
    soup=BeautifulSoup(page.content, 'html.parser')
    page_status=page.status_code

    # If the reply was 200 from the server, we know that the server and "share" are accessible. Moving on...
    if int(page_status) == 200:

        # Get all the the data from the share
        images_list=soup.find_all('a')

        # Sort on only iso and qcow2 files and put them in a list
        count=1
        images_list_items=[]
        for image_name in images_list:
            if "qcow2" in image_name.text or "iso" in image_name.text:
                images_list_items.append(image_name.text)
                count+=1
        err_value=images_list_items
        return err_value
    else:
        err_value=False
        return err_value


#####################################################################################################################################################################
# This function is to make the changes needed to the glabal_vars.sh file. We are now in none HPOC and need to set the right parameters
#####################################################################################################################################################################
def change_global_vars_sh(Images_list,Images_server,Images_loc):

    # Need to pull the latest from github
    git_command='mkdir -p /opt/github && cd /opt/github && git clone https://github.com/nutanixworkshops/stageworkshop.git'
    command = os.popen(git_command)
    print(command.read())
    print(command.close())

    # Open the file and replace



#####################################################################################################################################################################
# This function is to get the workshops form the staging_workshop.sh so we show the correct workshop.
#####################################################################################################################################################################
def get_workshops():
    # open /opt/github/stageworkshop/stage_workshop.sh and read the lines that starts with "WORKSHOPS=(\"" and ends with ")"
    file=open("/opt/github/stageworkshop/stage_workshop.sh","r")
    file_text=file.read()
    return workshop_nr

#####################################################################################################################################################################
# This function is to make the changes needed to the glabal_vars.sh file. We are now in none HPOC and need to set the right parameters
#####################################################################################################################################################################
def clean_up():
    clean_command='rm -Rf /opt/github'
    command = os.popen(clean_command)
    print(command.read())
    print(command.close())


#####################################################################################################################################################################
# __main__
#####################################################################################################################################################################
PE_Host='10.42.8.37'
Email_address=''
#Workshop_nr=get_workshops()
Network_1=''
Network_1_submask=''
Network_1_gw=''
Network_2=''
Network_2_submask=''
Network_2_gw=''
PE_Password='techX2019!'
Images_server='10.42.194.11' #input("Please provide the IP address of the images server: ")
Images_loc='workshop_staging' #input("Please provide the share that needs to be used on the image server with IP address: "+Images_server+": ")
#print("Checking the images server...")

# Use the clutster details to connect to the cluster and retrieve cluster details
url_prism='https://'+PE_Host+':9440/PrismGateway/services/rest/v2.0/cluster'
response = requests.request("GET", url_prism, auth=('admin', PE_Password),verify=False)
cluster_data=json.loads(response.text)
print(cluster_data["name_servers"])


# Get the list if the images from the defined image server and check if we can reach the server and the directory
Images_list=webscrap_image_server(Images_server,Images_loc)

if not Images_list:
    print("We have not received the correct information...")
    exist(1)

# Make the changes to the global.vars.sh file so we use the right parameters
change_global_vars_sh(Images_list,Images_server,Images_loc)



# Cleaning up what we don't need anymore
clean_up()