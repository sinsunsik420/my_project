#! /bin/bash

x=/var/lib/mecab/dic/open-jtalk/naist-jdic

dir=/usr/share/hts-voice/mei_happy/ #/usr/share/hts-voice/nitech-jp-atr503-m001/

td=${dir}tree-dur.inf
tm=${dir}tree-mgc.inf
tf=${dir}tree-lf0.inf
tl=${dir}tree-lpf.inf
md=${dir}dur.pdf
mm=${dir}mgc.pdf
mf=${dir}lf0.pdf
ml=${dir}lpf.pdf
dm1=${dir}mgc.win1
dm2=${dir}mgc.win2
dm3=${dir}mgc.win3
df1=${dir}lf0.win1
df2=${dir}lf0.win2
df3=${dir}lf0.win3
dl=${dir}lpf.win1
em=${dir}tree-gv-mgc.inf
ef=${dir}tree-gv-lf0.inf
cm=${dir}gv-mgc.pdf
cf=${dir}gv-lf0.pdf
k=${dir}gv-switch.inf
a=0.075
u=0.0
jf=1.2
jm=0.5
s=18000

echo それは私のおいなりさんだ | open_jtalk -x ${x} -td ${td} -tm ${tm} -tf ${tf} -md ${md} -mm ${mm} -mf ${mf} -dm ${dm1} -dm ${dm2} -dm ${dm3} -df ${df1} -df ${df2} -df ${df3} -em ${em} -ef ${ef} -cm ${cm} -cf ${cf} -k ${k} -a ${a} -jf ${jf} -s ${s} -u ${u} -ow ./test.wav -dl ${dl} -tl ${tl} -ml ${ml}
