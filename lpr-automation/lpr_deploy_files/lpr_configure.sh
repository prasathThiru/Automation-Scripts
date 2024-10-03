Docker_user="uvcustomer"
Docker_pass="2e430c1b-c2ad-4f22-94c5-56fd96449b4c"
Path="/uncanny"
LPR_DIR="/uncanny/lpr_deploy_files"
sink_bk_config="/uncanny/backup_sink_config/config"
sink_bk_client="/uncanny/backup_sink_config/client"
instance1=/uncanny/anpr/instance1
instance2=/uncanny/anpr/instance2
instance3=/uncanny/anpr/instance3
instance4=/uncanny/anpr/instance4
client_adapter=/uncanny/client_adapter_backup

#mkdir -p LPR_deploy_files/sink_client
#echo "\n****Downloading required files****\n"
#cd $Path
#wget "https://www.dropbox.com/s/mcqxb38it4htmje/lpr_deploy_files.zip?dl=0" -O lpr_deploy_files.zip 
#unzip lpr_deploy_files.zip 
#wget "https://www.dropbox.com/s/s5wwgl79qtnlpc0/reid.zip?dl=0" -O reid.zip
#unzip reid.zip

if [ -d "$LPR_DIR" ]; then
	echo "\n****Download completed. Folder path-> ${LPR_DIR}****\n"

	echo "\n****Logging out from older docker credentials****\n"
	docker logout
	
	echo "\n****Docker login****\n"
	docker login --username=$Docker_user --password=$Docker_pass 
	
	echo "\n****copying the files into appropriate folders****\n"
	cp $LPR_DIR/docker-compose.yml $Path
	

	echo "\n****client format file****"
	mkdir -p $instance1 $instance2 $instance3 $instance4
	mkdir -p /uncanny/client_adapter_backup
	cp $instance1/client_format.py $client_adapter/client_format_1.py
	cp $instance2/client_format.py $client_adapter/client_format_2.py
	cp $instance3/client_format.py $client_adapter/client_format_3.py
	cp $instance4/client_format.py $client_adapter/client_format_4.py
	echo $instance1 $instance2 $instance3 $instance4 | xargs -n 1 cp $LPR_DIR/client_format.py
	
	#sink config file is modified with aws path, token key, and db_sort_order
	echo "\n****Copying portal configuration files...****\n"
	mkdir -p /uncanny/sink/config $sink_bk_config 
	cp $Path/sink/config/config_*.json $sink_bk_config
	cp $LPR_DIR/sink_config/*.json $Path/sink/config/
	cp $LPR_DIR/pm2_app.json $Path/sink
	
	#client integration file is modified
	echo "\n****Copying client integration files...****"
	mkdir -p /uncanny/sink/client $sink_bk_client
	cp $Path/sink/client/*.json $sink_bk_client
	cp $LPR_DIR/sink_client/*.json $Path/sink/client/
	
        echo "\n****Downloading the application****\n"
        cd $Path
        docker-compose pull
	docker-compose down
        echo "\n ****statring the application****\n"
	docker-compose up -d
	sleep 15
	
	sed -i -e 's|"IGFX": false|"IGFX": true|g' /uncanny/anpr/instance*/config/config.json
	sed -i -e 's|"LiveDBDist": 1|"LiveDBDist": 0|g' /uncanny/anpr/instance*/config/config.json
	sed -i -e 's|"LiveDBDist2": 1|"LiveDBDist2": 0|g' /uncanny/anpr/instance*/config/config.json
	sed -i -e 's|"EnableStateCode": false|"EnableStateCode": true|g' /uncanny/anpr/instance*/config/config.json
	sed -i -e 's|"DetectionPath": "V3"|"DetectionPath": "V7"|g' /uncanny/anpr/instance*/config/config.json
	sed -i -e 's|"ReidDBDist": 4|"ReidDBDist": 3|g' /uncanny/anpr/instance*/config/config.json
	sed -i -e 's|"MinimumStateCodeConfidence": 0.7|"MinimumStateCodeConfidence": 0.3|g' /uncanny/anpr/instance*/config/config.json
	sed -i -e 's|"DatabaseMatch": false|"DatabaseMatch": true|g' /uncanny/anpr/instance*/config/config.json
	sed -i -e 's|"Country": "India"|"Country": "US"|g' /uncanny/anpr/instance*/config/config.json
	sed -i -e 's|"OcrVersion": "v10"|"OcrVersion": "v14"|g' /uncanny/anpr/instance*/config/config.json
	sed -i -e 's|"OcrVersion": "v4"|"OcrVersion": "v14"|g' /uncanny/anpr/instance*/config/config.json
	sed -i -e 's|"OcrValidatorVersion": "v7"|"OcrValidatorVersion": "v13"|g' /uncanny/anpr/instance*/config/config.json
	sed -i -e 's|"OcrValidatorVersion": "v5"|"OcrValidatorVersion": "v13"|g' /uncanny/anpr/instance*/config/config.json
	sed -i -e 's|"DirectionFromDevice": true|"DirectionFromDevice": false|g' /uncanny/anpr/instance*/config/config.json
	sed -i -e 's|"NameFlag": 32|"NameFlag": 23|g' /uncanny/anpr/instance*/config/config.json
	sed -i -e 's|"NameFlag": 0|"NameFlag": 23|g' /uncanny/anpr/instance*/config/config.json
	
	echo "\n****Required config parameters are changed****\n"

	echo "\n****Restarting the application****\n"
	docker-compose down
	echo "\n"
	docker-compose up -d
	sleep 10
	curl -sfkL 'https://www.dropbox.com/s/i1rai6gq1lpcold/sink_tcp_configure.sh?dl=0' | sh
	sleep 5
	rm -r $Path/old_lpr_deploy_files
	mv $Path/lpr_deploy_files $Path/old_lpr_deploy_files
	docker ps -a
else
	echo "\nError: ${LPR_DIR} not found. Can not continue...."

  exit 1
fi
