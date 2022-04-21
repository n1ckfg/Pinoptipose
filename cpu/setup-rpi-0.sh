VERSION="2.4.0"
FILENAME="tensorflow-$VERSION-cp37-none-linux_armv6l.whl"

wget https://github.com/lhelontra/tensorflow-on-arm/releases/download/v$VERSION/$FILENAME
pip3 install $FILENAME
rm $FILENAME
