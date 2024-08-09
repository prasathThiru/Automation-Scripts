data_location="/home/prasath/prasath_hdd/prasath/Flashparking/ocr_data"
s3_path="s3://uploads.flashvision.videoanalytics"

echo "enter number of days report"
read no

while read line
	do
		s3=`echo $line | awk -F "," '{print $1}'`
#		site_name=`echo $line | awk -F "/" '{print $2}'`
		place_name=`echo $line | awk -F "," '{print $2}'`
		echo "****$place_name****"
		mkdir -p $data_location/$place_name
		cd $data_location/$place_name

		#echo "enter number of days report"
		#read no
		
		i=1
		while [ $i -le $no ];
		do
			date=`date +%Y-%m-%d --date="$i days ago"`
			mkdir $data_location/$place_name/$date
			cd $data_location/$place_name/$date
			aws s3 cp --recursive --exclude "*" --include "*.json" $s3_path/$s3/$date .
			echo $date
			i=$(($i+1))
		done
	done < $1 
