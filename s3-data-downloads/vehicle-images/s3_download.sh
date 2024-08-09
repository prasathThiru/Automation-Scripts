#!/bin/bash

# Variables
data_location="/home/prasath/prasath_hdd/prasath/Flashparking/ocr_data/all_2"
s3_path="s3://uploads.flashvision.videoanalytics"

echo "Enter the number of days report"
read no

while read line; do
    s3=`echo $line | awk -F "," '{print $1}'`
    place_name=`echo $line | awk -F "," '{print $2}'`
    state=`echo $line | awk -F "," '{print $3}'`
    echo "****$place_name****"
    mkdir -p $data_location/$state/$place_name
    cd $data_location/$state/$place_name

    i=1
    while [ $i -le $no ]; do
        date=`date +%Y-%m-%d --date="$i days ago"`
        
        # List the last 20 images
        images=$(aws s3 ls "$s3_path/$s3/$date" --recursive | grep ".jpg" | sort | tail -n 100 | awk '{print $4}')
        
        # Download each image
        for image in $images; do
            aws s3 cp "$s3_path/$image" .
        done
        
        echo $date
        i=$(($i+1))
    done
done < $1

