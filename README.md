# AutomateMcAfee

This will automate the start & stop of McAfee services in your Linux server environment where you need to run it a limited time. 

## Description

Let's build up a scenario. 

You have a list of production servers which are being maintained under a critical infrastructure.

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

* How/where to download your program
* Any modifications needed to be made to files/folders

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

Contributors names and contact info

* Sangeeth Sankalpa  
[@sangeeth-sankalpa](https://linkedin.com/in/sangeeth-sankalpa)

## Version History

* 0.0.1
    * Initial Release

## Acknowledgments

Inspiration, code snippets:
* [Sathish Bowatta](https://github.com/zathizh)
