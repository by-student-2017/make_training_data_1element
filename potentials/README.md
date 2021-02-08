PWscf_PBE_PAW_Potentials


# Ubuntu 18.04 LTS
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


## Run
1. cd ~
2. sudo apt update
3. sudo apt install -y git csh
4. git clone https://github.com/by-student-2017/PWscf_PBE_PAW_Potentials.git
5. cd ~/PWscf_PBE_PAW_Potentials
6. chmod +x run_isolated_atom
7. ./run_isolated_atom


# Google Colaboratory
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


## Run
	!apt update
	!apt install -y git csh
	%cd /content
	!git clone https://github.com/by-student-2017/PWscf_PBE_PAW_Potentials.git
	%cd /content/PWscf_PBE_PAW_Potentials
	!chmod +x run_isolated_atom_gc
	!./run_isolated_atom_gc
