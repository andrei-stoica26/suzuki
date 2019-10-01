from opentrons import robot, containers, instruments

robot.head_speed(x=18000, y=18000, z=5000, a=700, b=700)

containers.create(
    '96_rack_pp',
    grid=(8,12),
    spacing=(18,18),
    diameter=13,
    depth=48
    )

containers.create(
    '96_rack_glass',
    grid=(8,12),
    spacing=(18,18),
    diameter=13,
    depth=48
    )

rack_number=3
rack_stock_reactants=[]
r_positions=['A1','A2','B1']
r_types=['halide','boronic acid','base']
for i in range(0,rack_number):
    rack_stock_reactants.append(containers.load("FluidX_24_5ml", r_positions[i], r_types[i]))
tiprack_1000 = containers.load("tiprack-1000ul-H", "D3")
source_trough4row = containers.load("trough-12row", "C2")
reaction_racks = [containers.load("96_rack_glass", "D1"),containers.load("96_rack_pp", "D2")]

trash = containers.load("point", "B3")

    # Pipettes SetUp
p1000 = instruments.Pipette(
    name='eppendorf1000',
    axis='b',
    trash_container=trash,
    tip_racks=tiprack_1000,
    max_volume=1000,
    min_volume=30,
    channels=1,
)

r_scale=[]
with open('reaction_details.csv') as f:
    f.readline()
    for line in f:
        ls=line.split(',')
        r_scale.append(float(ls[1]))


lines=[]
filelist=['solids.csv','liquids.csv']
for filename in filelist:
    with open(filename) as f:
        f.readline()
        for line in f:
            z=line.replace('\n','')+','+filename.replace('s.csv','')
            lines.append(z.split(','))
            
molarity=0.8
conv_factor=1000
#4 reactions
lines=sorted(lines,key=lambda x: [int(x[3]),int(x[4])])

reaction_wells=['A7','A8']
#A3 and A4 are negative control


#dispense reactants
for well in reaction_wells:
    for line in lines:
        source_location=line[0]
        if line[1]=='24_rack4':
            continue
        if line[1]=='big_trough':
            source_rack=source_trough4row
        else:
            source_location=source_location.replace('A','B')
            source_rack=rack_stock_reactants[int(line[1][-1])-1]
        reaction_number=int(line[3])-1
        if line[-1]=='liquid':
            vol_to_dispense=round(conv_factor*r_scale[reaction_number]*float(line[5]),1)
        else: #if solid
            if len(line[8])<2: #if density not given in the csv file, that is, if the solid used in reaction is NOT a liquid here
                vol_to_dispense=round(conv_factor*r_scale[reaction_number]*float(line[6])/molarity,1)
            else:
                vol_to_dispense=round(conv_factor*r_scale[reaction_number]*float(line[7])/float(line[8].replace('\n','')),1)
        p1000.transfer(vol_to_dispense, source_rack.wells(source_location), reaction_racks[reaction_number].wells(reaction_wells).top(-15), air_gap=10)
            
        

