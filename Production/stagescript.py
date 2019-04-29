import requests
import os
from bs4 import BeautifulSoup
import json
import urllib3
import time
import subprocess

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
def check_file(file_name="cluster.txt"):
    global dict_parameters
    dict_parameters={}
    list_from_file=()
    list_key=("PE_Host",
              "PE_Password",
              "Email_address",
              "Network_1",
              "Network_1_submask",
              "Network_1_gw",
              "Network_1_vlan",
              "Network_2",
              "Network_2_submask",
              "Network_2_gw",
              "Network_2_vlan",
              "Images_server",
              "Images_loc",
              "Workshop_nr"
              )
    try:
        # Trying to see if we have a file called cluster.txt in the /opt location
        file="/tmp/"+file_name
        with open(file,"r") as file_holder:
            for line in file_holder:
                if not "#" in line:
                    # Put the variables in a list
                    lst_from_file=line.split("|")
        # Assign the items in the list to the corresponding dict_parameters using a loop and a helper list (dict_key)
        i=0
        while i < len(lst_from_file):
            dict_parameters[list_key[i]]=lst_from_file[i]
            i+=1
        return

    except FileNotFoundError:
        # As we have not found the file we need to ask for the parameters or maybe for the file.
        response=input("Do you have a file that holds the parameters needed for the script to work? [yes/no] ")
        if response.upper()=="YES":
            # Get the filel name
            response_file=input("Please provide the name of the file in the /tmp location... ")
            check_file(response_file)
        elif response.upper=="NO":
            # OK proceed with the ask of the parameters
            print("Please provide the value for the following parameters:")
            print()
            dict_parameters={}
            dict_parameters["Email_address"]=input("Provide the email address that needs to be used: ")
            dict_parameters["PE_Host"]=input("Provide the IP address of the cluster that needs to be staged: ")
            dict_parameters["PE_Password"]=input("Provide the PRISM/admin password for the cluster: ")
            dict_parameters["Images_server"]=input("Provide the IP address of the webserver that holds the images: ")
            dict_parameters["Images_loc"]=input("Provide the location on the webserver ("+response_Images_server+") that holds the images: ")
            dict_parameters["Network_1"]=input("Provide network 1 IP network (example: 10.10.10.0): ")
            dict_parameters["Network_1_submask"]=input("Provide the subnetmask for network 1 (example: 255.255.255.0): ")
            dict_parameters["Network_1_gw"]=input("Provide the default gateway for the network 1 (example: 10.10.10.254): ")
            dict_parameters["Network_1_vlan"]=input("Provide the VLAN ID for network 1 (example: 10): ")
            dict_parameters["Network_2"]=input("Provide network 2 IP network (example: 10.10.20.0): ")
            dict_parameters["Network_2_submask"]=input("Provide the subnetmask for network 2 (example: 255.255.255.0): ")
            dict_parameters["Network_2_gw"]=input("Provide the default gateway for the network 2 (example: 10.10.20.254): ")
            dict_parameters["Network_2_vlan"]=input("Provide the VLAN ID for network 2 (example: 20): ")
            dict_parameters["Workshop_nr"]=input("Provide the workshop number to have staged on cluster"+dict_parameters["PE_Host"]+": ")
            return
        else:
            print("Only yes/Yes/YES or no/No/NO is allowed")

#####################################################################################################################################################################
# This function is to make the changes needed to the glabal_vars.sh file. We are now in none HPOC and need to set the right parameters
#####################################################################################################################################################################
def change_global_vars_sh():


    # Open the file and replace
    # default location is /opt/github/stageworkshop/scripts/global.vars.sh

    file_tmp="/opt/global.vars.sh"
    file_final="/opt/github/stageworkshop/scripts/global.vars.sh"

    file1 = open(file_tmp, 'r')
    file2 = open(file_final, 'w')

    # Words we need to change
    checkWords=("NETWORK1","NW_1_VLAN","NW_1_SUBNET","NETWORK2","NW_2_VLAN","NW_2_SUBNET","IMAGE_SERVER","IMAGE_LOCATION")
    # Words to be replaced with
    repWords=(dict_parameters["Network_1_gw"],dict_parameters["Network_1_vlan"],dict_parameters["Network_1_submask"],dict_parameters["Network_2_gw"],
              dict_parameters["Network_2_vlan"],dict_parameters["Network_2_submask"],dict_parameters["Images_server"],dict_parameters["Images_loc"])
    for line in file1:
        for check, rep in zip(checkWords, repWords):
            line = line.replace(check, rep)
        file2.write(line)
    file1.close()
    file2.close()

    # Copy the template we use into the github cloned location

#####################################################################################################################################################################
# This function is to create the batch command that needs to be run to stage the cluster
#####################################################################################################################################################################
def create_batch_command():
    # We needto create a file stage_cluster.txt to have that in the command stage_workshop.sh -f stage_cluster.txt -w workshop_nr if we haven't got one...
    file_name=open("/opt/github/stageworkshop/stage_cluster.txt","w+")
    file_name.write(dict_parameters["PE_Host"]+"|"+dict_parameters["PE_Password"]+"|"+dict_parameters["Email_address"])
    file_name.close()

#####################################################################################################################################################################
# This function is to show a last check and then run if yes or return to the show paramters when no
#####################################################################################################################################################################
def last_check():
    list_parameters = ("Cluster VIP", "Cluster admin password", "Email address", "Network 1", "Network 1 Subnetmask(CIDR)",
    "Network 1 Gateway", "Network 1 VLAN ID", "Network 2", "Network 2 Subnetmask (CIDR)", "Network 2 Gateway",
    "Network 2 VLAN ID", "Images server", "Images Location")

    print(chr(27) + "[2J")
    print(30 * "*","LAST CHECK",30 * "*")
    print()
    print("We are going to use the following parameters to stage the cluster:")
    print(72 * "-")
    i = 0
    for k, v in dict_parameters.items():
        print(list_parameters[i] + ":", v)
        if i == len(dict_parameters) - 2:
            break
        else:
            i += 1
    print("Workshop: " + list_workshop[int(dict_parameters["Workshop_nr"]) - 1])
    print()
    print(30 * "*","LAST CHECK",30 * "*")
    print()
    response = input("All good to go? If yes, we will start the staging script...")
    if response.upper()=="YES":
        # Create the command to run and run it....
        batch_command='cd /opt/github/stageworkshop && /bin/bash stage_workshop.sh -f stage_cluster.txt -w '+dict_parameters["Workshop_nr"]
        command = os.popen(batch_command)
        print(command.read())
        print(command.close())
    elif response.upper()=="NO":
        exit(0) # Need a way to get back to the Show parameters overview....
    else:
        last_check()

#####################################################################################################################################################################
# This function is to show the set paramters
#####################################################################################################################################################################
def show_parameters():
    # Showing the data to the user to agree on the config. If not we need to understand what needs to be done.
    list_parameters=("Cluster VIP","Cluster admin password","Email address","Network 1","Network 1 Subnetmask(CIDR)",
                 "Network 1 Gateway","Network 1 VLAN ID","Network 2","Network 2 Subnetmask (CIDR)","Network 2 Gateway",
                 "Network 2 VLAN ID","Images server","Images Location")
    while True:
        print(chr(27) + "[2J")
        print(30 * "*","Overview",30 * "*")
        print()
        print("The script is going to run the following parameters to setup the cluster:")
        print()
        i=0
        for k,v in dict_parameters.items():
            print(list_parameters[i]+":", v)
            if i == len(dict_parameters)-2:
                break
            else:
                i+=1
        print("Workshop: "+list_workshop[int(dict_parameters["Workshop_nr"])-1])
        print(30 * "*","Overview",30 * "*")
        move_forward=input("Are these settings correct? ")
        if move_forward.upper() == "NO":
            change_parameter()
            break
        if move_forward.upper() == "YES":
            return
        else:
            print("You can only provide yes/Yes/YES or no/No/NO as an anwser...")
            show_parameters()

#####################################################################################################################################################################
# This function block is to change the set parameters menu and submenus
#####################################################################################################################################################################
# Main menu
def change_parameter():
    print(chr(27) + "[2J")
    print(30 * "*","Main change menu",30 * "*")
    print("Select the part you want to change:")
    print("1. PRISM Related settings (Cluster VIP, Password and or email address).")
    print("2. Network 1 settings.")
    print("3. Network 2 settings.")
    print("4. Image related settings.")
    print("5. Change the workshop")
    print()
    print("6. Back ")
    print()
    change_object=input("Which object you want to change? [1-6] ")
    if change_object=="1":
        change_prism()
    elif change_object=="2":
        change_network_1()
    elif change_object=="3":
        change_network_2()
    elif change_object=="4":
        change_images()
    elif change_object=="5":
        change_workshop()
    elif change_object=="6":
        show_parameters()
    else:
        change_parameters()

# Change PRISM Sub Menu
def change_prism():
    print(chr(27) + "[2J")
    print(30 * "-","Sub change PRISM menu",30 * "-")
    print("Make your selection based on the following provided parameters for PRISM")
    print()
    print("a. Email address: "+dict_parameters["Email_address"])
    print("b. Cluster VIP: "+dict_parameters["PE_Host"])
    print("c. Cluster password: "+dict_parameters["PE_Password"])
    print("q. Back to main menu.")
    print()
    print(30 * "-","Sub change PRISM menu",30 * "-")
    print()
    response=input("Please make your selection [a,b,c or q]: ")
    if response.upper()=="Q":
        change_parameter()
    elif response.upper()=="A":
        change_value("prism","email")
    elif response.upper()=="B":
        change_value("prism","pe_host")
    elif response.upper()=="C":
        change_value("prism","pe_passwd")
    else:
        change_prism()

# Change network 1 Sub Menu
def change_network_1():
    print(chr(27) + "[2J")
    print(30 * "-","Sub change Network 1 menu",30 * "-")
    print("Make your selection based on the following provided parameters for Network 1")
    print()
    print("a. Network 1: "+dict_parameters["Network_1"])
    print("b. Network 1 Subnetmask(CIDR): "+dict_parameters["Network_1_submask"])
    print("c. Network 1 gateway: "+dict_parameters["Network_1_gw"])
    print("d. Network 1 VLAN ID: "+dict_parameters["Network_1_vlan"])
    print("q. Back to main menu")
    print()
    print(30 * "-","Sub change Network 1 menu",30 * "-")
    print()
    response=input("Please make your selectiopn [a,b,c,d or q]: ")
    if response.upper()=="Q":
        change_parameter()
    elif response.upper()=="A":
        change_value("nw1","nw1")
    elif response.upper()=="B":
        change_value("nw1","nw1_sub")
    elif response.upper()=="C":
        change_value("nw1","nw1_gw")
    elif response.upper()=="D":
        change_value("nw1","nw1_vlan")
    else:
        change_network_1()

# Change network 2 Sub Menu        
def change_network_2():
    print(chr(27) + "[2J")
    print(30 * "-","Sub change Network 2 menu",30 * "-")
    print("Make your selection based on the following provided parameters for Network 2")
    print()
    print("a. Network 2: "+dict_parameters["Network_2"])
    print("b. Network 2 Subnetmask:(CIDR) "+dict_parameters["Network_2_submask"])
    print("c. Network 2 gateway: "+dict_parameters["Network_2_gw"])
    print("d. Network 2 VLAN ID: "+dict_parameters["Network_2_vlan"])
    print("q. Back to main menu")
    print()
    print(30 * "-","Sub change Network 2 menu",30 * "-")
    print()
    response=input("Please make your selectiopn [a,b,c,d or q]: ")
    if response.upper()=="Q":
        change_parameter()
    elif response.upper()=="A":
        change_value("nw2","nw2")
    elif response.upper()=="B":
        change_value("nw2","nw2_sub")
    elif response.upper()=="C":
        change_value("nw2","nw2_gw")
    elif response.upper()=="D":
        change_value("nw2","nw2_vlan")
    else:
        change_network_2()

# Change images Sub Menu
def change_images():
    print(chr(27) + "[2J")
    print(30 * "-","Sub change Image server menu",30 * "-")
    print("Make your selection based on the following provided parameters for Images")
    print()
    print("a. Images server: "+dict_parameters["Images_server"])
    print("b. Images location: "+dict_parameters["Images_loc"])
    print("q. Back to main menu")
    print()
    print(30 * "-","Sub change Image server menu",30 * "-")
    print()
    response=input("Please make your selectiopn [a,b or q]: ")
    if response.upper()=="Q":
        change_parameter()
    elif response.upper()=="A":
        change_value("imgages","img_server")
    elif response.upper()=="B":
        change_value("images","img_loc")
    else:
        change_images()

# Chnage workshop
def change_workshop():
    print(chr(27) + "[2J")
    print(30 * "-","Sub change workshop menu",30 * "-")
    print("Make your selection based on the following provided parameters for the workshops")
    print()
    print("a. Workshop: "+list_workshop[int(dict_parameters["Workshop_nr"])-1])
    print("q. Back to main menu")
    print()
    print(30 * "-","Sub change workshop menu",30 * "-")
    print()
    response=input("Please make your selectiopn [a or q]: ")
    if response.upper()=="Q":
        change_parameter()
    elif response.upper()=="A":
        change_value("workshop","workshop")
    else:
        change_workshop()    

#####################################################################################################################################################################
# This function is to change the parameter to the new value and call the sub module menus again
#####################################################################################################################################################################
def change_value(module,submod):
    dict_text={"email":"email address",
              "pe_host":"Cluster VIP",
              "pe_passwd":"Cluster password",
              "nw1":"network 1",
              "nw1_sub":"network 1 subnetmask(CIDR)",
              "nw1_gw":"network 1 gateway",
              "nw1_vlan":"network 1 VLAN ID",
              "nw2":"network 2",
              "nw2_sub":"network 2 subnetmask(CIDR)",
              "nw2_gw":"network 2 gateway",
              "nw2_vlan":"network 2 VLAN ID",
              "img_server":"images server",
              "img_loc":"imges location",
              "workshop":"workshop naam"
              }
    dict_key={"email":"Email_address",
              "pe_host":"PE_Host",
              "pe_passwd":"PE_Password",
              "nw1":"Network_1",
              "nw1_sub":"Network_1_submask",
              "nw1_gw":"Network_1_gw",
              "nw1_vlan":"Network_1_vlan",
              "nw2":"Network_2",
              "nw2_sub":"Network_2_submask",
              "nw2_gw":"Network_2_gw",
              "nw2_vlan":"Network_2_vlan",
              "img_server":"Images_server",
              "img_loc":"Images_loc",
              "workshop":"Workshop_nr"
              }
    # If we are chanig the workshop, we need to get teh possible workshops printed first so we can change the value 
    if module =="workshop":
        print("The following workshop are possible:")
        print()
        i=0
        while i <= len(list_workshop)-1:
            print(str(i+1)+"."+list_workshop[i])
            i+=1
        print()

    response=input("Provide the new value for "+dict_text[submod]+" ["+dict_parameters[dict_key[submod]]+"]: ")
    if not response:
        if module=="prism":
            change_prism()
        elif module=="nw1":
            change_network_1()
        elif module=="nw2":
            change_network_2()
        elif module=="workshop":
            change_workshop()
        else:
            change_images()
    else:
        dict_parameters[dict_key[submod]]=response
        if module=="prism":
            change_prism()
        elif module=="nw1":
            change_network_1()
        elif module=="nw2":
            change_network_2()
        elif module=="workshop":
            change_workshop()
        else:
            change_images()

#####################################################################################################################################################################
# This function is to check the parameters with values and call the sub module menus again if fail
#####################################################################################################################################################################
def check_parameters():

    # Get the list if the images from the defined image server and check if we can reach the server and the directory
    Images_list=webscrap_image_server(dict_parameters["Images_server"],dict_parameters["Images_loc"])

    if not Images_list:
        print("We have not received the correct information for the image server...")
        time.sleep(1)
        change_images()

#####################################################################################################################################################################
# This function is to get the workshops form the staging_workshop.sh so we show the correct workshop.
#####################################################################################################################################################################
def get_workshops():
    # Get the workshop from the github repo
    git_command='cd /opt/github/stageworkshop && git pull'
    command = os.popen(git_command)
    print(command.read())
    print(command.close())
    # open /opt/github/stageworkshop/stage_workshop.sh and read the lines that starts with "WORKSHOPS=(\"" and ends with ")"
    list_workshops=[]
    with open("/opt/github/stageworkshop/stage_workshop.sh","r") as file:
        for line in file:
            if "WORKSHOPS=(" in line:
                for line in file:
                    if ") # A" in line:
                        return list_workshops
                    else:
                        list_workshops.append(line.strip('\"')[:-4])
                        print(len(list_workshops))

#####################################################################################################################################################################
# This function is to cleanup all the stuff we temporary used/created
#####################################################################################################################################################################
def clean_up():
    clean_command='rm -Rf /opt/github'
    command = os.popen(clean_command)
    print(command.read())
    print(command.close())

#####################################################################################################################################################################
# __main__
#####################################################################################################################################################################
# Take the SSL warning out of the screen
urllib3.disable_warnings()

# Check to see if we can use a file for the paramters
check_file()

# Get the workshops that are defined in the script and put them in a list so we can use them later
list_workshop=get_workshops()

# Call the parameters show function to have the user check the parameters
show_parameters()

# Make the changes to the global.vars.sh file so the stage_script.sh uses the right parameters
change_global_vars_sh()

# Call the create batchfile command and run the command
create_batch_command()

# Call the last check
last_check()

# Just let the user knwo that we are ready and nothing to do anymore.....
print("Staging script has been started. As the staging script runs autonomous, we are going to shutdown.....")

input("Waiting...")

# Cleaning up what we don't need anymore
clean_up()