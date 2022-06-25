# AutomateMcAfee

This will automate the start & stop of McAfee services in your Linux server environment where you need to run it a limited time. 

## Description

Let's build up a scenario. 

You have a list of production servers which are being maintained under a critical infrastructure. Your management/client team has decided to deploy an endpoint solution (Assume **McAfee** as the AV) in all of the production servers. But you cannot run the AV services in the production hours. And direct root access via SSH is disabled as well. Below are list of concerns what your management/client has. 


* Creating a cronjob in a management server to start at a specific time (Assume 8:30 PM) to run a shell script to start McAfee Antivirus services which include
```
1.	Checking required status files of the Task1 & Task2 to fetch the final status.

Task1 STATUS FILE LOCATION: userTask1@managementserver:/use/the/path/to/some/task1/STATUS/
Task1 STATUS FILE NAME:  StatusFile
Check if EVENT_RESET is DONE

Task2 STATUS FILE LOCATION: userTask2@managementserver:/use/the/path/to/some/task2/STATUS/
Task2 STATUS FILE NAME: StatusFile
Check if TASK_CLEAN is DONE
 
2.	Upon fetching the done status only, get access to remote production servers accordingly via SSH.
 
3.	After login to the first remote server, it will Start the two services related to McAfee Antivirus by executing below commands.

/opt/McAfee/ens/esp/init/mfeespd-control.sh start
/opt/McAfee/ens/tp/init/mfetpd-control.sh start
 
4.	Then executing below two commands it will fetch the current status of the McAfee Antivirus services.

/opt/McAfee/ens/tp/init/mfetpd-control.sh status
/opt/McAfee/ens/esp/init/mfeespd-control.sh status
 
5.	Fetched status will be kept by assigning it to a variable in the script.
 
6.	Step 3 – 5 will be executed in remaining servers accordingly.
 
7.	If and only if all the status fetched from all servers are qual to service active, then it will be recorded in a log file in the management server with other necessary details.
 
8.	Otherwise, it will generate an E-mail to notify us by including all servers which have failed to start the McAfee Antivirus services successfully in order to take necessary actions further.
``` 
 
* Creating a cronjob in a management server to stop at a specific time (Assume 7:30 AM) to run a shell script to stop McAfee Antivirus services which include
``` 
1.	Get access to remote production servers accordingly via SSH to stop the McAfee Antivirus services.
 
2.	Login to the first remote server, to Stop the two services related to McAfee Antivirus by executing below commands.

/opt/McAfee/ens/tp/init/mfetpd-control.sh stop
/opt/McAfee/ens/esp/init/mfeespd-control.sh stop
 
3.	Then executing below two commands it will fetch the current status of the McAfee Antivirus services.

/opt/McAfee/ens/tp/init/mfetpd-control.sh status
/opt/McAfee/ens/esp/init/mfeespd-control.sh status
 
4.	Fetched status will be kept by assigning it to a variable in the script.
 
5.	Step 2 – 4 will be executed in remaining servers accordingly.
 
6.	If and only if all the status fetched from all servers are qual to service inactive, then it will be recorded in a log file in the management server with other necessary details.
 
7.	Otherwise, it will generate an E-mail to notify us by including all servers which have failed to stop the McAfee Antivirus services successfully in order to take necessary actions further.
```

##### Screenshots of the active status of both AV services
![image](https://user-images.githubusercontent.com/36575796/175768354-5252671e-7ff8-4d00-aa51-62278df80ed5.png)

![image](https://user-images.githubusercontent.com/36575796/175768367-cb8bda2b-500a-417e-81a3-90c07b1e0dae.png)


## Getting Started

### Tested environment

* Operating System: Red Hat Enterprise Linux Server 7.8 (Maipo)
* CPE OS Name: cpe:/o:redhat:enterprise_linux:7.8:GA:server
* Kernel: Linux 3.10.0-1127.19.1.el7.x86_64
* Architecture: x86-64 
* McAfee Endpoint Security for Linux Threat Prevention
  * Version : 10.7.8.12
  * License : Full
  * DAT Version : 4978.0
  * Engine Version : 6300.9389
  * Exploit Prevention Content Version : 10.7.0.00079

### Installing

* Make a directory named **McAfee_Antivirus** as below
```
$mkdir -p /home/McAfee_Antivirus_san/scripts/McAfee_Antivirus
```
* Download the files to a server which act as a management server in your infrastructure.
* Below listed commands require sudo privileges to run on a system. You may need to add below commands to sudoers file to be executed by the particular user (**sangeeth** user is used to access all servers) with sudo privilages, since the direct root access via SSH is disabled on the system servers.
```
To stop the ENSLTP service, add the following commands to sudoers file:

# /opt/McAfee/ens/tp/init/mfetpd-control.sh stop
# /opt/McAfee/ens/esp/init/mfeespd-control.sh stop

To start the ENSLTP service, add the following commands to sudoers file:

# /opt/McAfee/ens/esp/init/mfeespd-control.sh start
# /opt/McAfee/ens/tp/init/mfetpd-control.sh start
```

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```

## Help

Issue below command to get the usage
```
$ /home/McAfee_Antivirus_san/scripts/McAfee_Antivirus/AntivirusStart.py

Usage : Antivirus.py
	--start	<start the AV services>
	--stop	<stop the AV services>
```
<img width="641" alt="image" src="https://user-images.githubusercontent.com/36575796/175769092-cabf88d4-ad96-464f-8202-22f78ba5cb1d.png">


## Authors

* Sangeeth Sankalpa  
[@sangeeth-sankalpa](https://linkedin.com/in/sangeeth-sankalpa)

## Version History

* 0.0.1
    * Initial Release

## Acknowledgments

Inspiration, code snippets:
* [Sathish Bowatta](https://github.com/zathizh)
