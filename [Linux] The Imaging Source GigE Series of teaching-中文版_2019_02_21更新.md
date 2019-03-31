# 1. Dependencies
#Build dependencies

sudo apt-get install git g++ cmake pkg-config libudev-dev libudev1 libtinyxml-dev libgstreamer1.0-dev

sudo apt-get install libgstreamer-plugins-base1.0-dev libglib2.0-dev libgirepository1.0-dev libusb-1.0-0-dev

sudo apt-get install libzip-dev uvcdynctrl python-setuptools libxml2-dev libpcap-dev libaudit-dev libnotify-dev

sudo apt-get install autoconf intltool gtk-doc-tools python3-setuptools

#Runtime dependencies

sudo apt-get install gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-plugins-base gstreamer1.0-plugins-good

sudo apt-get install gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly libxml2 libpcap0.8 libaudit1 libnotify4

sudo apt-get install python3-pyqt5 python3-gi

# 2. install tiscamera
git clone --recursive https://github.com/TheImagingSource/tiscamera.git

cd tiscamera

mkdir build

cd build

#this order is used to set up the diver of linux system to ON

cmake -DBUILD_ARAVIS=ON -DBUILD_GST_1_0=ON -DBUILD_TOOLS=ON -DBUILD_V4L2=ON -DCMAKE_INSTALL_PREFIX=/usr ..

make

sudo make install

If you have completed steps 1 and 2, congratulations on completing the installation of the camera dependency pack
