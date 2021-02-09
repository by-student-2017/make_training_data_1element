# make_training_data_1element


# Ubuntu 18.04 LTS
## Install (cif2cell-informal)
1. sudo apt install -y git python python-setuptools python-dev gcc
2. git clone https://github.com/by-student-2017/cif2cell-informal.git
3. cd cif2cell-informal
4. tar zxvf PyCifRW-3.3.tar.gz
5. cd PyCifRW-3.3
6. sudo python setup.py install
7. cd ..
8. sudo python setup.py install


## Install (PWscf)
1. cd ~
2. sudo apt update
3. sudo apt install -y gcc g++ build-essential gfortran libopenblas-dev libfftw3-dev libopenmpi-dev wget
4. wget https://github.com/QEF/q-e/archive/qe-6.4.1.tar.gz
5. tar zxvf qe-6.4.1.tar.gz
6. cd q-e-qe-6.4.1
7. wget https://github.com/QEF/q-e/releases/download/qe-6.4.1/backports-6.4.1.diff
8. patch -p1 --merge < backports-6.4.1.diff
9. ./configure
10. make pw
11. sudo make install


## Setup mkdata and run
1. cd ~
2. sudo apt update
3. sudo apt install -y git python-pip python-scipy csh gfortran gnuplot
4. git clone https://github.com/by-student-2017/make_training_data_1element.git
5. cd ~/make_training_data_1element
6. sed -i 's/Xx/Si/g' element.input
7. python mkdata.py


# Google Colaboratory
## Install (cif2cell-informal)
	!apt update
	!apt install -y git python python-setuptools python-dev gcc
	%cd /content
	!git clone https://github.com/by-student-2017/cif2cell-informal.git
	%cd cif2cell-informal
	!tar zxvf PyCifRW-3.3.tar.gz
	%cd PyCifRW-3.3
	!python2 setup.py install
	%cd /content/cif2cell-informal
	!python2 setup.py install


## Install (PWscf)
	!apt update
	!apt install -y gcc g++ build-essential gfortran libopenblas-dev libfftw3-dev libopenmpi-dev wget
	%cd /content
	!wget https://github.com/QEF/q-e/archive/qe-6.4.1.tar.gz
	!tar zxvf qe-6.4.1.tar.gz
	%cd q-e-qe-6.4.1
	!wget https://github.com/QEF/q-e/releases/download/qe-6.4.1/backports-6.4.1.diff
	!patch -p1 --merge < backports-6.4.1.diff
	!./configure
	!make pw
	import os
	os.environ['PATH'] = "/content/q-e-qe-6.4.1/bin:"+os.environ['PATH']


## Setup mkdata
	!apt update
	!apt install -y git python-pip python-scipy csh gfortran gnuplot
	%cd /content
	!git clone https://github.com/by-student-2017/make_training_data_1element.git
	%cd /content/make_training_data_1element


## Run
	import os
	os.environ["OMP_NUM_THREADS"] = "1,1"
	os.environ["MKL_NUM_THREADS"] = "1"
	!cp element.input_tmp element.input
	!sed -i 's/Xx/Si/g' element.input
	!python2 mkdata_gc.py
	!zip -r results.zip results
	from google.colab import files
	files.download("results.zip")


# Google Colaboratory
## all settings
	!apt update
	!apt install -y git python python-setuptools python-dev gcc
	%cd /content
	!git clone https://github.com/by-student-2017/cif2cell-informal.git
	%cd cif2cell-informal
	!tar zxvf PyCifRW-3.3.tar.gz
	%cd PyCifRW-3.3
	!python2 setup.py install
	%cd /content/cif2cell-informal
	!python2 setup.py install
	
	!apt update
	!apt install -y gcc g++ build-essential gfortran libopenblas-dev libfftw3-dev libopenmpi-dev wget
	%cd /content
	!wget https://github.com/QEF/q-e/archive/qe-6.4.1.tar.gz
	!tar zxvf qe-6.4.1.tar.gz
	%cd q-e-qe-6.4.1
	!wget https://github.com/QEF/q-e/releases/download/qe-6.4.1/backports-6.4.1.diff
	!patch -p1 --merge < backports-6.4.1.diff
	!./configure
	!make pw
	import os
	os.environ['PATH'] = "/content/q-e-qe-6.4.1/bin:"+os.environ['PATH']
	
	!apt update
	!apt install -y git python-pip python-scipy csh gfortran gnuplot
	%cd /content
	!git clone https://github.com/by-student-2017/make_training_data_1element.git
	%cd /content/make_training_data_1element
	
	import os
	os.environ["OMP_NUM_THREADS"] = "1,1"
	os.environ["MKL_NUM_THREADS"] = "1"
	!cp element.input_tmp element.input
	!sed -i 's/Xx/Si/g' element.input
	!python2 mkdata_gc.py
	
	!zip -r results.zip results
	from google.colab import files
	files.download("results.zip")