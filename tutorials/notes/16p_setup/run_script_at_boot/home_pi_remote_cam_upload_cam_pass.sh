#!/bin/sh

#ip='192.168.10.11'
ip='192.168.10.13'
#ip='192.168.10.22'


hurl='http://'$ip'/cgi-bin/getsnapshot.cgi'

ss="let text = '"
sp="  "
es="';"

sleep 2

while true; do
    wget $hurl -O /home/pi/remote_cam_upload/snap.jpg

    export DATE=`date +%F`
    export TIME=`date +%T`

    echo $ss$DATE$sp$TIME$es > /home/pi/remote_cam_upload/ts.js

    scp -i "/home/pi/remote_cam_upload/ggp1.pem" /home/pi/remote_cam_upload/snap.jpg /home/pi/remote_cam_upload/ts.js ubuntu@ec2-54-172-171-223.compute-1.amazonaws.com:/mnt/data/catch/camfwd/.

    sleep 5
done

exit 0
