import os
from shutil import copyfile
if not os.path.exists('opentrons'):
    os.mkdir('opentrons')
for file in os.listdir():
    if file.endswith('.py') and 'opentrons' not in file:
        chd_path=0
        lines_to_kill=0
        with open(file) as f, open('opentrons/'+file ,'w')as g:
            for line in f:
                if lines_to_kill>0:
                    lines_to_kill-=1
                    continue
                if chd_path==0:
                    if line!="path=''\n":
                        g.write(line)
                    else:
                        g.write("path='C:/Users/opentrons/protocols/Suzuki/'\n")
                        chd_path=1
                else:
                    if line!= "containers.create(\n":
                        if '96_rack_glass' in line:
                            line=line.replace('96_rack_glass','Para_dox_96_short')
                        if '96_rack_pp' in line:
                            line=line.replace('96_rack_pp','Starlab_96_Square_2mL')
                        g.write(line)
                    else:
                        lines_to_kill=6
    if file.endswith('.csv'):
        copyfile(file,'opentrons/'+file)
        
