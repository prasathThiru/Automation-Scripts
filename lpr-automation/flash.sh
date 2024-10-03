path="/uncanny"
lpr_dir="/uncanny/lpr_deploy_files/"

mkdir -p /uncanny
cd $path
echo "\n****Downloading required files****\n"
wget "https://www.dropbox.com/s/93icw9j38swehhw/lpr_deploy_files.zip?dl=0" -O lpr_deploy_files.zip 
unzip lpr_deploy_files.zip
wget "https://www.dropbox.com/s/ent0hihvvz0cuy1/reid.zip?dl=0" -O reid.zip 
unzip reid.zip

echo "\n****Starting the LPR application****\n"
cd $lpr_dir
sh lpr_configure.sh

