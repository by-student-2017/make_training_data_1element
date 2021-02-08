import numpy as np
import commands
import sys
#----------------------------------------------------------------------
satom = "Si"

cif2cell_adress = "cif2cell"

commands.getoutput("setenv OMP_NUM_THREADS 1")
num_core = commands.getoutput("grep 'core id' /proc/cpuinfo | sort -u | wc -l")

#pwscf_adress = "mpirun -np "+str(num_core)+" --allow-run-as-root pw.x"
#pwscf_adress = "mpirun -np "+str(num_core)+" pw.x"
pwscf_adress = "mpirun -np 1 pw.x"

commands.getoutput("chmod +x pwscf2force")
commands.getoutput("mkdir work")
commands.getoutput("mkdir dftb")
commands.getoutput("mkdir poscar")
commands.getoutput("mkdir cif")
#
# skpar
commands.getoutput("mkdir skpar")
commands.getoutput("mkdir refdata")
commands.getoutput("mv refdata ./skpar/refdata")
commands.getoutput("mkdir template")
commands.getoutput("mv template ./skpar/template")
commands.getoutput("mkdir "+str(satom)+".mol-evol")
commands.getoutput("echo \"# Energy [eV], Volume tag\" > toten-"+str(satom)+".ml.dat")

print "use struct.dat"
struct = commands.getoutput("awk '{if($1==\""+str(satom)+"\"){print $0}}' struct.dat")
struct_list = struct.split()
ntemp = int((len(struct_list)-1)/3 - 1)
temp = []
stru = []
weig = []
#if float(struct_list[3*ntemp+1]) <= 1073.0 :
#  ntemp = ntemp + 1
#  struct_list.append(1273.0)
#  struct_list.append("L")
#  struct_list.append(1.0)
for i in range(ntemp+1):
  temp.append(float(struct_list[3*i+1]))
  stru.append(struct_list[3*i+2])
  weig.append(float(struct_list[3*i+3]))
  t = temp[i]
  s = stru[i]
  commands.getoutput("cp ./material_project_cif/"+str(s)+".cif "+str(s)+"_"+str(t)+"K.cif")
print "temperature: ",temp
print "structure  : ",stru
print "weight     : ",weig
dim = len(temp)
#----------------------------------------------------------------------
for t in temp:
  print "---------------"
  print "Temperature: "+str(t)+" [K]"
  # Different fractions we will multiply the 'a0' lattice constant with:
  r1 = np.arange(0.09, 0.18, 0.09) # very short distance
  r2 = np.arange(0.27, 0.93, 0.03) # short distance
  r3 = np.arange(0.94, 1.08, 0.01) # middle distance
  r4 = np.arange(1.09, 1.75, 0.03) # long distance
  r5 = np.arange(1.78, 2.68, 0.09) # very long distance
  r6 = np.arange(2.95, 5.65, 0.27) # ultra long distance
  fractions = np.hstack((r1, r2, r3, r4, r5, r6))
  for vp in fractions:
    print "          Volume, vp: "+str(vp)
    a0 = float(vp)**(1.0/3.0)
    print "Lattice constant, a0: "+str(a0)
    #
    new_name = str(s)+"_"+str(a0)+"_"+str(t)+"K"
    commands.getoutput("cp "+str(s)+"_"+str(t)+"K.cif"+" "+str(new_name)+".cif")
    #
    commands.getoutput("awk '{if($1==\"_cell_length_a\"){printf \"%s  %10.8f \\n\",$1,$2*"+str(a0)+"}else{print $0}}' "+str(new_name)+".cif > tmp1")
    commands.getoutput("awk '{if($1==\"_cell_length_b\"){printf \"%s  %10.8f \\n\",$1,$2*"+str(a0)+"}else{print $0}}' tmp1 > tmp2")
    commands.getoutput("awk '{if($1==\"_cell_length_c\"){printf \"%s  %10.8f \\n\",$1,$2*"+str(a0)+"}else{print $0}}' tmp2 > tmp3")
    commands.getoutput("cp tmp3 "+str(new_name)+".cif")
    commands.getoutput("rm -f -r tmp1 tmp2 tmp3")
    #
    commands.getoutput(cif2cell_adress+" "+str(new_name)+".cif --no-reduce -p pwscf --pwscf-pseudo-PSLibrary-libdr=\"./potentials\" --setup-all --k-resolution=0.48 --pwscf-force=yes --pwscf-stress=yes --pwscf-run-type=scf -o pw.in") 
    commands.getoutput("sed -i 's/\'pw\'/\'pw_"+str(t)+"K\'/g' pw.scf.in")
    commands.getoutput(pwscf_adress+" < pw.scf.in > pw.out")
    #
    commands.getoutput(cif2cell_adress+" "+str(new_name)+".cif  --no-reduce -p pwscf --pwscf-pseudo-PSLibrary-libdr=\"./potentials\" --setup-all --k-resolution=0.20 --pwscf-force=yes --pwscf-stress=yes --pwscf-run-type=scf -o pw.in") 
    commands.getoutput("sed -i 's/\'pw\'/\'pw_"+str(t)+"K\'/g' pw.scf.in")
    commands.getoutput(pwscf_adress+" < pw.scf.in > pw.out")
    #
    commands.getoutput(cif2cell_adress+" "+str(new_name)+"  --no-reduce -p dftb -o "+str(new_name)+".gen")
    commands.getoutput("mv "+str(new_name)+".gen  ./dftb/")
    commands.getoutput(cif2cell_adress+" "+str(new_name)+"  --no-reduce -p vasp -o "+str(new_name)+".vasp")
    commands.getoutput("mv "+str(new_name)+".vasp ./poscar/")
    commands.getoutput("mv "+str(new_name)+".cif  ./cif/")
    #
    commands.getoutput("./pwscf2force > tmp_config_potfit")
    for itw in range(ntemp+1):
      if t == temp[itw]:
        wt = weig[itw]
    print "          weight, wt: "+str(wt)
    commands.getoutput("awk '{if($1==\"#W\"){print $1 $2*"+str(wt)+"}else{print $0}}' tmp_config_potfit > config_potfit")
    commands.getoutput("cat config_potfit >> config_potfit_"+str(satom)+"_"+str(t)+"K")
    #
    toten_per_atom = commands.getoutput("awk '{if($1==\"#E\"){print $2}}' config_potfit")
    natom = commands.getoutput("awk '{if($1==\"#N\"){print $2+$3+$4+$5+$6+$7+$8+$9}}' config_potfit")
    commands.getoutput("rm -f -r tmp_config_potfit config_potfit")
    toten = float(toten_per_atom) * float(natom)
    print "    Total energy, TE: "+str(toten)+" [eV]"
    commands.getoutput("echo "+str(toten)+"  "+str(vp)+" >> toten-"+str(satom)+".ml.dat")
    vp = float(vp)*100.0
    if (vp < 10.0):
      commands.getoutput("mkdir "+str(vp)[0:1].zfill(3))
      commands.getoutput("cp "+str(new_name)+".gen  ./"+str(vp)[0:1].zfill(3)+"/POS.gen")
      commands.getoutput("cp "+str(new_name)+".vasp  ./"+str(vp)[0:1].zfill(3)+"/POSCAR")
      commands.getoutput("cp "+str(new_name)+".cif  ./"+str(vp)[0:1].zfill(3)+"/"+str(new_name)+".cif")
      commands.getoutput("mv "+str(vp)[0:1].zfill(3)+" ./"+str(satom)+".mol-evol/"+str(vp)[0:1].zfill(3))
    elif (vp < 100.0):
      commands.getoutput("mkdir "+str(vp)[0:2].zfill(3))
      commands.getoutput("cp "+str(new_name)+".gen  ./"+str(vp)[0:2].zfill(3)+"/POS.gen")
      commands.getoutput("cp "+str(new_name)+".vasp  ./"+str(vp)[0:2].zfill(3)+"/POSCAR")
      commands.getoutput("cp "+str(new_name)+".cif  ./"+str(vp)[0:2].zfill(3)+"/"+str(new_name)+".cif")
      commands.getoutput("mv "+str(vp)[0:2].zfill(3)+" ./"+str(satom)+".mol-evol/"+str(vp)[0:2].zfill(3))
    else:
      commands.getoutput("mkdir "+str(vp)[0:3])
      commands.getoutput("cp "+str(new_name)+".gen  ./"+str(vp)[0:3]+"/POS.gen")
      commands.getoutput("cp "+str(new_name)+".vasp  ./"+str(vp)[0:3]+"/POSCAR")
      commands.getoutput("cp "+str(new_name)+".cif  ./"+str(vp)[0:3]+"/"+str(new_name)+".cif")
      commands.getoutput("mv "+str(vp)[0:3]+" ./"+str(satom)+".mol-evol/"+str(vp)[0:3])
    #
  commands.getoutput("mv "+str(satom)+".ml-evol ./skpar/template/")
  commands.getoutput("mv toten-"+str(satom)+".ml.dat ./skpar/refdata/")
  commands.getoutput("mv skpar skpar_"+str(t)+"K")
  commands.getoutput("mkdir skpar")
  commands.getoutput("mkdir refdata")
  commands.getoutput("mv refdata ./skpar/refdata")
  commands.getoutput("mkdir template")
  commands.getoutput("mv template ./skpar/template")
  commands.getoutput("mv toten-"+str(satom)+".ml.dat ./dftb/")
  commands.getoutput("mv dftb dftb_"+str(t)+"K")
  commands.getoutput("mkdir dftb")