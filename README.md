# Worm
Network Security Assignment #1 <br>
Professor Manabat - CPSC 456 - F 9-11:45AM <br>

# Author
Dan Ortiz (dbortiz@csu.fullerton.edu) <br></br>
<strong> SKELETON CODE CREDIT: PROFESSOR MANABAT </STRONG>

# Language
Python

# How to Execute
You first must choose a VM, within the internal network of VMs, which you want to execute the worm from. Once selected, you execute by typing:<br>
<strong>python worm.py</strong>

After the worm has been executed, it will begin to propagate through the network and begin infecting other VM systems.

# Before Execution
<strong>I decided to choose this VM (lubuntu) as my point of execution. As you will see, other VMs will become infected, but not this one because I shouldn't be able to infect myself!</strong>
<img src="images/LUBUNTU_BEFORE.PNG" width="800" height="300"/>
<img src="images/KALI_BEFORE.PNG" width="550" height="400"/>
<img src="images/XUBUNTU_BEFORE.PNG" width="550" height="400"/>

# After Execution
<strong>As stated before, these VMs have now been infected with the worm and is stored onto their systems.</strong>
<img src="images/LUBUNTU_AFTER.PNG" width="800" height="300"/>
<img src="images/KALI_AFTER.PNG" width="550" height="400"/>
<img src="images/XUBUNTU_AFTER.PNG" width="550" height="400"/>

# Explanation
The purpose of this assignment was to create a worm that would be able to propagate through a network and infect it.
I first set up a virtual network, using VirtualBox VMs, and gave said VMs credentials and configured them to the same subnet.
After the network was properly configured, I executed the worm program on one of the VMs.
The worm first scans the network and checks for all IPs on the network with port 22 (SSH) open.
After the list of networks are found, the worm will attempt a "dictionary" attack against the open port with the predefined credentials.
Once the SSH connected is established, the worm will check if it has already infected the system.
If it has, then it will kill its execution; but if it hasn't, it will add itself to the system, change it's permissions, and execute itself.
Once all identified systems have been infected, the worm will cease execution and will inform the user of its completed infection.

# Extra Credit
I have implemented the extra credit which is to clean all infected VMs by removing the worm file.
In order to execute the clean function, type:<br>
<strong>python worm.py -c</strong><br>
or<br>
<strong>python worm.py --clean</strong>

<strong>As you can see, after executing the clean up function, the worm has been removed from the systems.</strong>
<img src="images/LUBUNTU_CLEAN.PNG" width="800" height="300"/>
<img src="images/KALI_CLEAN.PNG" width="550" height="400"/>
<img src="images/XUBUNTU_CLEAN.PNG" width="550" height="400"/>
