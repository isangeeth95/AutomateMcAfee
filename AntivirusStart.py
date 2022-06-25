#! /usr/bin/python

import paramiko
import ConfigParser
import smtplib
import json
import os
import getopt
import sys
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- STATIC VARIABLES ---
_VERSION = "0.0.1"
_CONFIG_FILE = "AntivirusStart.cfg"

# --- GLOBALS ---
config = ""
hostconfig = ""
userconfig = ""
username = ""
password = ""
start_shellscript = ""
stop_shellscript = ""
LOCAL_LOGDIR="/home/McAfee_Antivirus_san/scripts/McAfee_Antivirus/logs"
MONTH = datetime.now().strftime("%B")
DATE_TIME = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")

os.path.exists (LOCAL_LOGDIR) or os.makedirs (LOCAL_LOGDIR)
os.path.exists (LOCAL_LOGDIR+'/'+MONTH) or os.makedirs (LOCAL_LOGDIR+'/'+MONTH)
LOG_FILE = LOCAL_LOGDIR+'/'+MONTH+'/'+DATE_TIME+'.log'
logging.basicConfig(filename=LOG_FILE, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def loadconfig():
	global config, hostconfig, userconfig, username, password, start_scriptname, stop_scriptname, start_shellscript, stop_shellscript,_CONFIG_FILE
	config = ConfigParser.ConfigParser()
	config.read(_CONFIG_FILE)
	username = config.get('CONFIG', 'USER')
	password  = config.get('CONFIG', 'PASSWORD')
	start_scriptname = config.get('CONFIG', 'START_SCRIPT')
	stop_scriptname = config.get('CONFIG', 'STOP_SCRIPT')
	start_shellscript = open(start_scriptname, 'r').read()
	stop_shellscript = open(stop_scriptname, 'r').read()
	hostconfig =  config.options('HOSTS')
	userconfig =  config.options('USERS')

def processResults(results, arg):
	host_dict = {} #All services status
	inactive_host_dict = {} #inactive(dead) state and active(exited) state
	active_host_dict = {} #active(running) state
	final_host_dict = {}
	out_json_obj = ""
	inactive_out_json_obj = ""
	active_out_json_obj = ""
	if (arg == '--start'):	
		for line in results:
			host, service, status= line.split()
			if host in host_dict.keys():
				host_dict[host] = dict(host_dict[host].items() + {service:status}.items())
				if status != "active(running)":
					if host in inactive_host_dict.keys():
						inactive_host_dict[host]= dict(inactive_host_dict[host].items() + {service:status}.items())
					else:
	                                        inactive_host_dict[host]={service:status}
			else:
				host_dict[host]={service:status}
				if status != "active(running)":
	                                if host in inactive_host_dict.keys():
	                                        inactive_host_dict[host]= dict(inactive_host_dict[host].items() + {service:status}.items())
	                                else:
	                                        inactive_host_dict[host]={service:status}
		out_json_obj=(json.dumps(host_dict, indent=4, sort_keys=True))
		inactive_out_json_obj=(json.dumps(inactive_host_dict, indent=4, sort_keys=True))
		final_host_dict = inactive_host_dict
		logging.warning('#### Both AV services status after attempting to start them ####'+out_json_obj)
		logging.warning('#### AV services which are in inactive(dead) state and active(exited) state after attempting to start them ####'+inactive_out_json_obj)


	elif(arg == '--stop'):
		for line in results:
	                host, service, status= line.split()
	                if host in host_dict.keys():
	                        host_dict[host] = dict(host_dict[host].items() + {service:status}.items())
	                        if status != "inactive(dead)" and status != "failed(Result:":
	                                if host in active_host_dict.keys():
	                                        active_host_dict[host]= dict(active_host_dict[host].items() + {service:status}.items())
	                                else:
	                                        active_host_dict[host]={service:status}
	                else:
	                        host_dict[host]={service:status}
	                        if status != "inactive(dead)" and status != "failed(Result:":
	                                if host in active_host_dict.keys():
	                                        active_host_dict[host]= dict(active_host_dict[host].items() + {service:status}.items())
	                                else:
	                                        active_host_dict[host]={service:status}
		out_json_obj=(json.dumps(host_dict, indent=4, sort_keys=True))
		active_out_json_obj=(json.dumps(active_host_dict, indent=4, sort_keys=True))
		final_host_dict = active_host_dict
		logging.warning('#### Both AV services status after attempting to stop them ####'+out_json_obj)
		logging.warning('#### AV services which are in active(running) state after attempting to stop them ####'+active_out_json_obj)

	else:
		logging.warning('#### Both AV services status are empty due to passed cmd line argument ####')
		logging.warning('#### AV services which are in inactive(dead) state and active(exited) state are empty due to passed cmd line argument ####')
		sys.exit(2)

	return out_json_obj,final_host_dict

def handleSSHRequest(server, arg):
	global username, password, start_shellscript, stop_shellscript
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(server, username=username, password=password)
	logging.warning("SSH to "+server)
	if(arg == '--start'):
		stdin, stdout, stderr = ssh.exec_command(start_shellscript)
		logging.warning("AV services START script has been executed")
	elif(arg == '--stop'):
		stdin, stdout, stderr = ssh.exec_command(stop_shellscript)
		logging.warning("AV services STOP script has been executed")
	else:
		print("Argument not valid")
		sys.exit(2)
	result = stdout.read().decode()
	return str(result)

def generateExcel(error_service_info, headers):
        table = headers
        for key in error_service_info:
                table += str("<tr><th>")
                table += str(key)
                table += str("</th><th>")
                table += str(error_service_info[key])
                table += str("</th></tr>")
        table += str("</table></html>")
        return table
			
def send_email(error_host_details, arg):
	global config, userconfig
	mail_server = config.get('CONFIG', 'EMAILHOST')
	mail_from = config.get('CONFIG', 'EMAIL_SENDING_ADDRESS')

	header_info = config.get('CONFIG', 'HEADER').split()

	table_header = "<html><head><style>table, th, td { border: 1px solid black; border-collapse: collapse;}th, td {  padding: 5px; }th { text-align: left; }</style></head><table style=\"width:30%\"><tr><th>" + str(header_info[0]) + "</th><th>" + str(header_info[1]) + "</th></tr>"

	#for inactive_host in inactive_host_details:
		#if user in userconfig:
	mail_to = config.get('USERS', 'sangeeth')
	message = MIMEMultipart("alternative")
	if(arg == '--start'):
		message["Subject"] =  "START FAILED : Client1 McAFee services"
	elif(arg == '--stop'):
		message["Subject"] =  "STOP FAILED : Client1 McAFee services"
	else:
		sys.exit(2)
	message["From"] = mail_from
	message["To"] = mail_to

	table = generateExcel(error_host_details, table_header)
		
	mail_body = MIMEText(table, "html")
	message.attach(mail_body)

	email = smtplib.SMTP(mail_server)
	email.sendmail(mail_from, mail_to, message.as_string())
	email.quit()

"""
--Let's assume--
Tasks' names are sEOD & eEOD.
Check "EVENT_RESET" line in file "/use/the/path/to/some/task1/STATUS/StatusFile" is containing "DONE".
Check "TASK_CLEAN" line in file  "/use/the/path/to/some/task2/STATUS/StatusFile" is containing "DONE".
"""
def check_sEOD_eEOD():
        sEOD_eEOD_status=""
        s_Job_complete='grep -v "#" /use/the/path/to/some/task1/STATUS/StatusFile | grep "\<EVENT_RESET\>" | grep "DONE"' #change accordingly
        e_Job_complete='grep -v "#" /use/the/path/to/some/task2/STATUS/StatusFile | grep "\<TASK_CLEAN\>" | grep "DONE"' #change accordingly

        if os.popen(s_Job_complete).read().strip() and os.popen(e_Job_complete).read().strip():
                sEOD_eEOD_status="DONE"

        else:
                sEOD_eEOD_status="NOT DONE"

        return sEOD_eEOD_status

def send_start_error_email(arg):
        global config, userconfig
        mail_server = config.get('CONFIG', 'EMAILHOST')
        mail_from = config.get('CONFIG', 'EMAIL_SENDING_ADDRESS')

        header_info = config.get('CONFIG', 'HEADER').split()

        mail_to = config.get('USERS', 'infra')
        message = MIMEMultipart("alternative")
        if(arg == '--start'):
                message["Subject"] = "Tasks STATUS ERROR : Client1 McAFee services"
        else:
                sys.exit(2)

        message["From"] = mail_from
        message["To"] = mail_to

        body = "<html><head><h2 style=\"color: #ff0000;\">Tasks STATUS ERROR : Client1 McAFee services</h2><p><strong>One of the Task1 or Task2 jobs is not completed yet or both jobs are not completed yet.</strong><br /><strong style=\"color: #ff0000;\">Please investigate..!</strong></p><p><strong>&nbsp;</strong></p></head></html>"      
        mail_body = MIMEText(body, "html")
        message.attach(mail_body)

        email = smtplib.SMTP(mail_server)
        email.sendmail(mail_from, mail_to, message.as_string())
        email.quit()

def main():
	try:
		args=sys.argv[1]
	except IndexError:
		print ("Usage : Antivirus.py\n\t--start\t<start the AV services>\n\t--stop\t<stop the AV services>")
		sys.exit(2)
	os.chdir("/home/McAfee_Antivirus_san/scripts/McAfee_Antivirus") #change accordingly
	global config, hostconfig
	loadconfig()
	results = ""
	
	if check_sEOD_eEOD() == 'DONE':
		for server in hostconfig:
			results += handleSSHRequest(server, args)
		results = filter(None, results.split('\n'))
		host_details, error_host_details = processResults(results, args)

	else:
		send_start_error_email(args)
		logging.warning("One of the task1 or task2 jobs is not completed yet or both jobs are not completed yet\nexiting main()...")
		sys.exit(2)
		
	if len(error_host_details) > 0:
		send_email(error_host_details, args)

if __name__ == '__main__':
	main()

