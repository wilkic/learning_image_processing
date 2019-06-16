#!/bin/bash

DATETIME=`date +%Y%m%d%H%M%S`

dest='ubuntu@ec2-54-172-171-223.compute-1.amazonaws.com:/mnt/data/catch/images_and_timestamps/.'

# All cam ips start at 101 and go up from there
ip_base='10.10.110.1'
n_cams=15

# New cams have different url for accessing image
new=(1 10 11 12 14 15)


##############

sp="  "
es="';"

ips=()
for (( i=1; i<$n_cams+1; i++ )); do
    ip=$(printf "%s%02d\n" $ip_base $i)
    echo "$ip"
    ips+=($ip)
    

    # Check if new, change url accordingly
    for j in ${new[@]}; do
    
        # Assume it's an old url
        url='http://'$ip'/cgi-bin/getsnapshot.cgi'
        
        if [ $i == $j ]; then
            url='http://admin:admin@'$ip'/tmpfs/auto.jpg'
            break
        fi
    done

    echo "Fetching snap from $ip"
    echo "... $url"
    wget $url -O cam$i.jpg
    
    DATE=`date +%F`
    TIME=`date +%T`
    ss="let text$i = '"
    echo $ss$DATE$sp$TIME$es > ts$i.js
    
    scp -i "ggp1.pem" cam$i.jpg ts$i.js $dest


done


##rtsp_port='554'
##rurl='rtsp://'$ip':'$rtsp_port'/live0.264'
##ffmpeg -r 25 -y -i $rurl -updatefirst 1 -r 2 cam.bmp

