# https://github.com/raspberrypi/picamera2/blob/main/README.md

sudo apt-get install -y python3-opencv opencv-data libfmt-dev libdrm-dev python3-pyqt5
sudo pip3 install pyopengl piexif

git clone --branch picamera2 https://github.com/raspberrypi/libcamera.git

cd ..
git clone https://github.com/tomba/kmsxx.git
cd kmsxx
git submodule update --init
meson build
ninja -C build

cd ..
git clone https://github.com/RaspberryPiFoundation/python-v4l2.git

cd ..
git clone https://github.com/raspberrypi/picamera2.git

export PYTHONPATH=/home/pi/picamera2:/home/pi/libcamera/build/src/py:/home/pi/kmsxx/build/py:/home/pi/python-v4l2



