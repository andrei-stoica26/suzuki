import os
from shutil import copyfile
if not os.path.exists('opentrons'):
    os.mkdir('opentrons')
for file in os.listdir():
    if file.endswith('.py') and 'opentrons' not in file:
        with open(file) as f, open('opentrons/'+file ,'w')as g:
            for line in f:
                if line!="path=''\n":
                    g.write(line)
                else:
                    g.write("path='C:/Users/opentrons/protocols/Suzuki/'\n")
    if file.endswith('.csv'):
        copyfile(file,'opentrons/'+file)
        
