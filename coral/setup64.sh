# https://coral.ai/docs/accelerator/get-started/#runtime-on-linux

USER_NAME=$(whoami)

sudo usermod -aG plugdev $USER_NAME

echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update

sudo apt-get install -y libedgetpu1-std python3-pycoral
#sudo pip3 install picamera

echo "Reboot before testing."


