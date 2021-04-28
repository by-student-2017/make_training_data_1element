#!/bin/bash

mkdir all_results

elements="H Li Be B C N O F Na Mg Al Si P S Cl K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te Cs Ba La Sm Yb Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi"

#elements="H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi"

cp element.input element_Xx.input
for elem in ${elements}; do
  rm -f -r work
  cp element_Xx.input element.input
  sed -i "s/Xx/${elem}/g" element.input
  python mkdata.py
  mv results results_${elem}
  cd all_results
  cp -r ../results_${elem} ./
  cd ../
  rm -f -r resutls_${elem}
done
