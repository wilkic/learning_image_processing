#!/bin/bash

ips=(
    '10.10.110.101'
    '10.10.110.102'
    '10.10.110.103'
    '10.10.110.104'
    '10.10.110.105'
    '10.10.110.106'
    '10.10.110.107'
    '10.10.110.108'
    '10.10.110.109'
    '10.10.110.110'
    '10.10.110.111'
    '10.10.110.112'
    '10.10.110.113'
    '10.10.110.114'
    '10.10.110.115'
    )



ss="let text = '"
sp="  "
es="';"

sleep 30

while true; do
    
    i=0
    
    for ip in ${ips[@]}; do
        ((i++))
        hurl='http://admin:admin@'$ip'/tmpfs/auto.jpg'
        wget $hurl -O /home/pi/remote_cam_upload/snap$i.jpg

        export DATE=`date +%F`
        export TIME=`date +%T`

        echo $ss$DATE$sp$TIME$es > /home/pi/remote_cam_upload/ts$i.js

        scp -i "/home/pi/remote_cam_upload/ggp1.pem" /home/pi/remote_cam_upload/snap$i.jpg /home/pi/remote_cam_upload/ts$i.js ubuntu@ec2-54-172-171-223.compute-1.amazonaws.com:/mnt/data/ava/images_and_timestamps/.
    
    done
    
    sleep 30
    
done

exit 0
