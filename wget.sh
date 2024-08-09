mkdir $2
while read line
do
	echo $line
	wget $line -P $2
done < $1
