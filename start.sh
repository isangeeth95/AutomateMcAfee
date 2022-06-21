#! /usr/bin/bash

#EARLY_HTTPD_STATUS=$(/usr/bin/systemctl status httpd | grep Active | awk '{print $2}')
#EARLY_CMA_STATUS=$(/usr/bin/systemctl status cma | grep Active | awk '{print $2}')
EARLY_mfetpd_STATUS=$(/opt/McAfee/ens/tp/init/mfetpd-control.sh status | grep Active | awk '{print $2}')
EARLY_mfeespd_STATUS=$(/opt/McAfee/ens/esp/init/mfeespd-control.sh status | grep Active | awk '{print $2}')
#NUM_HTTPD=1
NUM_mfetpd=1
#NUM_CMA=1
NUM_mfeespd=1

if [[ $EARLY_mfetpd_STATUS == "active" ]];
then
	break
else
#	sudo /usr/bin/systemctl start httpd
	sudo /opt/McAfee/ens/tp/init/mfetpd-control.sh start
#	LATER_HTTPD_STATUS=$(/usr/bin/systemctl status httpd | grep Active | awk '{print $2}')
	LATER_mfetpd_STATUS=$(/opt/McAfee/ens/tp/init/mfetpd-control.sh status | grep Active | awk '{print $2}')
	if [[ $LATER_mfetpd_STATUS == "inactive" ]];
	then
		while [ $NUM_mfetpd -le 5]
		do
#			sudo /usr/bin/systemctl start httpd
			sudo /opt/McAfee/ens/tp/init/mfetpd-control.sh start
#			LATER2_HTTPD_STATUS=$(/usr/bin/systemctl status httpd | grep Active | awk '{print $2}')
			LATER2_mfetpd_STATUS=$(/opt/McAfee/ens/tp/init/mfetpd-control.sh status | grep Active | awk '{print $2}')
			if [[ $LATER2_mfetpd_STATUS == "active" ]];
			then
				break
			fi
			NUM_mfetpd=`expr $NUM_mfetpd  + 1`
		done
	fi
fi

if [[ $EARLY_mfeespd_STATUS == "active" ]];
then
        break
else
#        sudo /usr/bin/systemctl start cma
	sudo /opt/McAfee/ens/esp/init/mfeespd-control.sh start
#        LATER_CMA_STATUS=$(/usr/bin/systemctl status cma | grep Active | awk '{print $2}')
	LATER_mfeespd_STATUS=$(/opt/McAfee/ens/esp/init/mfeespd-control.sh status | grep Active | awk '{print $2}')
        if [[ $LATER_mfeespd_STATUS == "inactive" ]];
        then
                while [ $NUM_mfeespd -le 5]
                do
#                        sudo /usr/bin/systemctl start cma
			sudo /opt/McAfee/ens/esp/init/mfeespd-control.sh start
#                        LATER2_CMA_STATUS=$(/usr/bin/systemctl status cma | grep Active | awk '{print $2}')
			LATER2_mfeespd_STATUS=$(/opt/McAfee/ens/esp/init/mfeespd-control.sh status | grep Active | awk '{print $2}')
                        if [[ $LATER2_mfeespd_STATUS == "active" ]];
                        then
                                break
                        fi
                        NUM_mfeespd=`expr $NUM_mfeespd + 1`
                done
        fi
fi


#HTTPD_STATUS=$(hostname ; /usr/bin/systemctl status httpd | head -n 1 | awk '{print $2}' ; /usr/bin/systemctl status httpd | grep Active | awk '{print $2 $3}')
#CMA_STATUS=$(hostname ; /usr/bin/systemctl status cma | head -n 1 | awk '{print $2}' ; /usr/bin/systemctl status cma | grep Active | awk '{print $2 $3}')

mfetpd_STATUS=$(hostname ; /opt/McAfee/ens/tp/init/mfetpd-control.sh status | head -n 1 | awk '{print $2}' ; /opt/McAfee/ens/tp/init/mfetpd-control.sh status | grep Active | awk '{print $2 $3}')
mfeespd_STATUS=$(hostname ; /opt/McAfee/ens/esp/init/mfeespd-control.sh status | head -n 1 | awk '{print $2}' ; /opt/McAfee/ens/esp/init/mfeespd-control.sh status | grep Active | awk '{print $2 $3}')

#echo $HTTPD_STATUS 
#echo $CMA_STATUS

echo $mfetpd_STATUS 
echo $mfeespd_STATUS
