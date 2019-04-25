import requests
import os
from bs4 import BeautifulSoup
import json
import urllib3

urllib3.disable_warnings()


#####################################################################################################################################################################
# TEMPORARY Function to set parameters. This needs to be changed in the Prod version!!!!!!
#####################################################################################################################################################################
def set_vars():
    PE_Host='10.42.9.37'
    Email_address='willem@nutanix.com'
    #Workshop_nr=get_workshops()
    Network_1='192.168.1.0'
    Network_1_submask='255.255.255.0'
    Network_1_gw='192.168.1.254'
    Network_1_vlan='1'
    Network_2='10.10.10.0'
    Network_2_submask='255.255.255.0'
    Network_2_gw='10.10.10.254'
    Network_2_vlan='10'
    PE_Password='techX2019!'
    Images_server='10.42.194.11' #input("Please provide the IP address of the images server: ")
    Images_loc='workshop_staging' #input("Please provide the share that needs to be used on the image server with IP address: "+Images_server+": ")
    
    #Putting all parameters in a dictionary
    dict_parameters={}
    dict_parameters["Email_address"]=Email_address
    dict_parameters["PE_Host"]=PE_Host
    dict_parameters["PE_Password"]=PE_Password
    dict_parameters["Images_server"]=Images_server
    dict_parameters["Images_loc"]=Images_loc
    dict_parameters["Network_1"]=Network_1
    dict_parameters["Network_1_submask"]=Network_1_submask
    dict_parameters["Network_1_gw"]=Network_1_gw
    dict_parameters["Network_1_vlan"]=Network_1_vlan
    dict_parameters["Network_2"]=Network_2
    dict_parameters["Network_2_submask"]=Network_2_submask
    dict_parameters["Network_2_gw"]=Network_2_gw
    dict_parameters["Network_2_vlan"]=Network_2_vlan

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
# This function is to show the set paramters
#####################################################################################################################################################################
def get_workshops():
    print("Workshop stuff")

#####################################################################################################################################################################
# This function is to show the set paramters
#####################################################################################################################################################################
def show_parameters():
    # Showing the data to the user to agree on the config. If not we need to understand what needs to be done.
    list_parameters=("Email address","Cluster VIP","Cluster admin password","Images server","Images Location","Network 1","Network 1 Subnetmask",
                 "Network 1 Gateway","Network 1 VLAN ID","Network 2","Network 2 Subnetmask","Network 2 Gateway","Network 2 VLAN ID")

    while True:
        print(chr(27) + "[2J")
        print("The script is going to run the following parameters to setup the cluster:")
        print()
        i=0
        for k,v in dict_parameters.items():
            print(list_parameters[i]+":", v)
            i+=1
        print()
        move_forward=input("Are these settings correct? ")
        if move_forward.upper() == "NO":
            print("Ok let's change some stuff")
            change_parameter()
            break
        if move_forward.upper() == "YES":
            print("OK we are going to use these parameters")
            show_parameters_final()
            break
        else:
            print("You can only provide YES or NO as an anwser")
    

#####################################################################################################################################################################
# This function is to change the set paramters
#####################################################################################################################################################################
def change_parameter():
    print(chr(27) + "[2J")
    print(30 * "-","Main change menu",30 * "-")
    print("Select the part you want to change:")
    print("1. PRISM Related settings (Cluster VIP, Password and or email address).")
    print("2. Network 1 settings.")
    print("3. Network 2 settings.")
    print("4. Image related settings.")
    print("5. Back to main menu.")
    print()
    change_object=input("Which object you want to change? [1-5]")
    if change_object="1":
        print(chr(27) + "[2J")
        print(30 * "-","Main change PRISM menu",30 * "-")
        print("Make your selection based on the following provided parameters for PRISM")
        print()
        print("a. Email address: "+dict_parameters["Email_address"])
        print("b. Cluster VIP: "+dict_parameters["PE_Host"])
        print("c. Cluster password: "+dict_parameters["PE_Password"])
        print("q. Back to main menu.")
        print()
    elif change_object="2":
        print(chr(27) + "[2J")
        print(30 * "-","Main change Network 1 menu",30 * "-")
        print("Make your selection based on the following provided parameters for Network 1")
        print()
        print("a. Network 1: "+dict_parameters["Network_1"])
        print("b. Network 1 Subnetmask: "+dict_parameters["Network_1_submask"])
        print("c. Network 1 gateway: "+dict_parameters["Network_1_gw"])
        print("d. Network 1 VLAN ID: "+dict_parameters["Network_1_vlan"])
        print("q. Back to main menu")
        print()
    elif change_object="3":
        print(chr(27) + "[2J")
        print(30 * "-","Main change Network 2 menu",30 * "-")
        print("Make your selection based on the following provided parameters for Network 2")
        print()
        print("a. Network 2: "+dict_parameters["Network_2"])
        print("b. Network 2 Subnetmask: "+dict_parameters["Network_2_submask"])
        print("c. Network 2 gateway: "+dict_parameters["Network_2_gw"])
        print("d. Network 2 VLAN ID: "+dict_parameters["Network_2_vlan"])
        print("q. Back to main menu")
        print()
    elif change_object="4":
        print(chr(27) + "[2J")
        print(30 * "-","Main change Image server menu",30 * "-")
        print("Make your selection based on the following provided parameters for Images")
        print()
        print("a. Images server: "+dict_parameters["Images_server"])
        print("b. Images location: "+dict_parameters["Images_loc"])
        print("q. Back to main menu")
        print()
    elif change_object="5":
        show_parameters()
    else:



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

set_vars()
show_parameters()



# As the anwser has been that we need to change the parameters, we need to show and provide the possibility to change them
# We group them in Network 1 and 2, PRISM and Images
if change_parameter=="YES":
    # Show the four possibilities:
    print(chr(27) + "[2J")
    print("Select the part you want to change:")
    print("1. PRISM Related settings (Cluster VIP, Password and or email address).")
    print("2. Network 1 settings.")
    print("3. Network 2 settings.")
    print("4. Image related settings.")
    print()
    change_object=input("Which object you want to change? ")
    if change_object="1":
        print(chr(27) + "[2J")
        print("Make your selection based on the following provided parameters for Network 1")
        print()
        print("a. Network 1: "+dict_parameters["Network_1"])
        print("b. Network 1 Subnetmask: "+dict_parameters["Network_1_submask"])
        print("c. Network 1 gateway: "+dict_parameters["Network_1_gw"])
        print("d. Network 1 VLAN ID: "+dict_parameters["Network_1_vlan"])
        print()

    



# Get the list if the images from the defined image server and check if we can reach the server and the directory
Images_list=webscrap_image_server(Images_server,Images_loc)

if not Images_list:
    print("We have not received the correct information...")
    exist(1)

# Make the changes to the global.vars.sh file so we use the right parameters
#change_global_vars_sh(Images_list,Images_server,Images_loc)



# Cleaning up what we don't need anymore
clean_up()