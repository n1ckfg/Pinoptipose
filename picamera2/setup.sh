# https://github.com/raspberrypi/picamera2/blob/main/README.md

sudo apt-get install -y python3-pip git meson python3-opencv opencv-data libfmt-dev libdrm-dev python3-pyqt5
sudo apt-get install -y libboost-dev libgnutls28-dev openssl libtiff5-dev libatlas-base-dev libglib2.0-dev libgstreamer-plugins-base1.0-dev
sudo apt-get install -y qtbase5-dev libqt5core5a libqt5gui5 libqt5widgets5 libqt5dbus5 libqt5network5

sudo pip3 install jinja2 pyopengl piexif pyyaml ply tflite-runtime tflite-support
sudo pip3 install --upgrade meson numpy

cd ~/

git clone --branch picamera2 https://github.com/raspberrypi/libcamera
git clone https://github.com/tomba/kmsxx
git clone https://github.com/RaspberryPiFoundation/python-v4l2
git clone https://github.com/raspberrypi/picamera2

cd libcamera
# for RPi OS Lite
#meson build --buildtype=release -Dpipelines=raspberrypi -Dipas=raspberrypi -Dv4l2=true -Dgstreamer=enabled -Dtest=false -Dlc-compliance=disabled -Dcam=disabled -Dqcam=disabled -Ddocumentation=disabled -Dpycamera=enabled
# for RPi OS Desktop
meson build --buildtype=release -Dpipelines=raspberrypi -Dipas=raspberrypi -Dv4l2=true -Dgstreamer=enabled -Dtest=false -Dlc-compliance=disabled -Dcam=disabled -Dqcam=enabled -Ddocumentation=disabled -Dpycamera=enabled
sudo ninja -C build install

cd ../kmsxx
git submodule update --init
meson build
ninja -C build

# python-v4l2 doesn't need to be compiled
# picamera2 doesn't need to be compiled

echo "Put this in .bashrc"
echo "export PYTHONPATH=/home/pi/picamera2:/home/pi/libcamera/build/src/py:/home/pi/kmsxx/build/py:/home/pi/python-v4l2"



