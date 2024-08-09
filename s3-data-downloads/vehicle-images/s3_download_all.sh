data_location="/home/prasath/prasath_hdd/prasath/Flashparking/ocr_data/all"
s3_path="s3://uploads.flashvision.videoanalytics"

echo "enter number of days report"
read no

while read line
	do
		s3=`echo $line | awk -F "," '{print $1}'`
#		site_name=`echo $line | awk -F "/" '{print $2}'`
		place_name=`echo $line | awk -F "," '{print $2}'`
		state=`echo $line | awk -F "," '{print $3}'`
		echo "****$place_name****"
		mkdir -p $data_location/$state/$place_name
		cd $data_location/$state/$place_name

		#echo "enter number of days report"
		#read no
		
		i=1
		while [ $i -le $no ];
		do
			date=`date +%Y-%m-%d --date="$i days ago"`
#			mkdir $data_location/$state/$place_name
#			cd $data_location/$state/$place_name
			aws s3 sync --exclude "*" --include "*.jpg" --exclude "*.json" --exclude "*_fullimage_*.jpg" "$s3_path/$s3/$date" .
			echo $date
			i=$(($i+1))
		done
	done < $1 
