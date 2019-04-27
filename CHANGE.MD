<H2>Dark site stage script container</H2>


This repo is holding all the information, and WIP stuff for:<BR>
* Container based running stage workshop script (github.com/jncox/stageworkshop)
* Uses a text file, if available, to read the parameters
* If no text file is available, questions will be asked to get the parameters needed
* Manipulation of the variables, used by the staging script, to install/stage a Nutanix cluster

---
<H3>Usage</H3>


After the container is created using docker build, or pull from wessenstam/dark_site, run the container using the following command:<BR>


<B>docker run -i -v <LOCATION LOCAL MACHINE>:/tmp --name <CONTAINER_NAME> --rm wessenstam/dark_site</B><BR>


The <B><LOCATION LOCAL MACHINE></B> is pointing to a local directory, <B>using an absolute path</B>, where a <B>.txt</B> file is available that holds the parameters to be used
Naming of the container can be done using the <B>--name</B> parameter.


After the script has run the following will be running from a network POV:
* Two networks, Primary and Secondary, running in the provided subnet and network range
* Primary network is using .50 till .70 as the DHCP pool
* Secondary network is using .150 till .170 as the DHCP pool
* Cluster information:
    * .38 for the DATA SERVICES
    * .39 for the PRISM Central environment
* AutoDC2, Lunix based DC on .40
    
---
<H3>Changes</H3>


27-04-2019: Willem Essenstam: First Beta version available and tested on a Nutanix HPOC Cluster

---
<H3>To Do</H3>


* After the last check, if not ok, the menu structure/flow is not working as expected
* Get the DHCP settings for the networks 1 and 2 in the parameters. They are now static.

