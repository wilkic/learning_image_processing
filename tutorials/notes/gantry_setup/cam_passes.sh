#!/bin/bash

DATETIME=`date +%Y%m%d%H%M%S`

dest='ubuntu@18.214.141.78:/mnt/data/catch/images_and_timestamps/.'

# All cam ips start at 101 and go up from there
ip_base='10.10.110.1'
n_cams=14

Nsecs2wait=5
Ntries=2

pdir='/home/pi/gsp'
kdir=$pdir'/aws'
cdir=$pdir'/cams'

##############

sp="  "
es="';"

ips=()
for (( i=86; i<86+$n_cams; i++ )); do
    ip=$(printf "%s%02d\n" $ip_base $i)
    echo "$ip"
    ips+=($ip)
    
    # old url
    #url='http://'$ip'/cgi-bin/getsnapshot.cgi'
    #new url
    url='http://admin:admin@'$ip'/tmpfs/auto.jpg'

    echo "Fetching snap from $ip"
    echo "... $url"
    wget -T $Nsecs2wait -t $Ntries $url -O $cdir/cam$i.jpg
    
    DATE=`date +%F`
    TIME=`date +%T`
    ss="let text$i = '"
    echo $ss$DATE$sp$TIME$es > $cdir/ts$i.js
    
    scp -i "$kdir/ggp1.pem" $cdir/cam$i.jpg $cdir/ts$i.js $dest

done


##rtsp_port='554'
##rurl='rtsp://'$ip':'$rtsp_port'/live0.264'
##ffmpeg -r 25 -y -i $rurl -updatefirst 1 -r 2 cam.bmp

