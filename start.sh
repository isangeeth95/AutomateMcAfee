#! /usr/bin/bash

EARLY_mfetpd_STATUS=$(/opt/McAfee/ens/tp/init/mfetpd-control.sh status | grep Active | awk '{print $2}')
EARLY_mfeespd_STATUS=$(/opt/McAfee/ens/esp/init/mfeespd-control.sh status | grep Active | awk '{print $2}')

NUM_mfetpd=1
NUM_mfeespd=1

if [[ $EARLY_mfetpd_STATUS == "active" ]];
then
	break
else
	sudo /opt/McAfee/ens/tp/init/mfetpd-control.sh start
	LATER_mfetpd_STATUS=$(/opt/McAfee/ens/tp/init/mfetpd-control.sh status | grep Active | awk '{print $2}')
	if [[ $LATER_mfetpd_STATUS == "inactive" ]];
	then
		while [ $NUM_mfetpd -le 5]
		do
			sudo /opt/McAfee/ens/tp/init/mfetpd-control.sh start
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
	sudo /opt/McAfee/ens/esp/init/mfeespd-control.sh start
	LATER_mfeespd_STATUS=$(/opt/McAfee/ens/esp/init/mfeespd-control.sh status | grep Active | awk '{print $2}')
        if [[ $LATER_mfeespd_STATUS == "inactive" ]];
        then
                while [ $NUM_mfeespd -le 5]
                do
			sudo /opt/McAfee/ens/esp/init/mfeespd-control.sh start
			LATER2_mfeespd_STATUS=$(/opt/McAfee/ens/esp/init/mfeespd-control.sh status | grep Active | awk '{print $2}')
                        if [[ $LATER2_mfeespd_STATUS == "active" ]];
                        then
                                break
                        fi
                        NUM_mfeespd=`expr $NUM_mfeespd + 1`
                done
        fi
fi


mfetpd_STATUS=$(hostname ; /opt/McAfee/ens/tp/init/mfetpd-control.sh status | head -n 1 | awk '{print $2}' ; /opt/McAfee/ens/tp/init/mfetpd-control.sh status | grep Active | awk '{print $2 $3}')
mfeespd_STATUS=$(hostname ; /opt/McAfee/ens/esp/init/mfeespd-control.sh status | head -n 1 | awk '{print $2}' ; /opt/McAfee/ens/esp/init/mfeespd-control.sh status | grep Active | awk '{print $2 $3}')

echo $mfetpd_STATUS 
echo $mfeespd_STATUS
