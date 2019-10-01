from opentrons import robot, containers, instruments

robot.head_speed(x=18000, y=18000, z=5000, a=700, b=700)
path='C:/Users/opentrons/protocols/Suzuki/'



rack_number=3
rack_stock_reactants=[]
r_positions=['A1','A2','B1']
r_types=['halide','boronic acid','base']
for i in range(0,rack_number):
    rack_stock_reactants.append(containers.load("FluidX_24_5ml", r_positions[i], r_types[i]))
tiprack_1000 = containers.load("tiprack-1000ul-H", "D3")
source_trough4row = containers.load("trough-12row", "C2")
reaction_racks = [containers.load("Para_dox_96_short", "D1"),containers.load("Starlab_96_Square_2mL", "D2")]

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
with open(path+'reaction_details.csv') as f:
    f.readline()
    for line in f:
        ls=line.split(',')
        r_scale.append(float(ls[1]))


lines=[]
filelist=['solids.csv','liquids.csv']
for filename in filelist:
    with open(path+filename) as f:
        f.readline()
        for line in f:
            z=line.replace('\n','')+','+filename.replace('s.csv','')
            lines.append(z.split(','))

number_rows=4
molarity=0.8
conv_factor=1000
#4 reactions
lines=sorted(lines,key=lambda x: [int(x[3]),int(x[4])])

reaction_wells=['A5','A6']
#A3 and A4 are negative control


#dispense reactants
p1000.pick_up_tip()
for well in reaction_wells:
    sum_liquids=[0]*2
    sum_solids=[0]*2
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
            #print(vol_to_dispense)
            if line[1]!='big_trough':
                p1000.transfer(vol_to_dispense, source_rack.wells(source_location), reaction_racks[reaction_number].wells(reaction_wells).top(-15), air_gap=10)
                sum_solids[reaction_number]+=vol_to_dispense
            sum_liquids[reaction_number]+=vol_to_dispense
        else: #if solid
            if line[1]=='24_rack3':
                vol_to_dispense=conv_factor*r_scale[reaction_number]
                print(vol_to_dispense)
            else:
                if len(line[8])<2: #if density not given in the csv file, that is, if the solid used in reaction is NOT a liquid here
                    vol_to_dispense=round(conv_factor*r_scale[reaction_number]*float(line[6])/molarity,1)
                else:
                    vol_to_dispense=conv_factor*r_scale[reaction_number]*float(line[7])/float(line[8].replace('\n',''))
            p1000.transfer(vol_to_dispense, source_rack.wells(source_location), reaction_racks[reaction_number].wells(reaction_wells).top(-15), air_gap=10)
            sum_solids[reaction_number]+=vol_to_dispense
        print(line[2],vol_to_dispense)
    print(sum_liquids)
    print(sum_solids)
    for line in lines:
        source_location=line[0]
        reaction_number=int(line[3])-1
        if line[1]=='big_trough':
            source_rack=source_trough4row
            vol_to_dispense=max(sum_liquids[reaction_number]-sum_solids[reaction_number],0)
            if vol_to_dispense!=0:
                p1000.transfer(vol_to_dispense, source_rack.wells(source_location), reaction_racks[reaction_number].wells(reaction_wells).top(-15), air_gap=10)
p1000.drop_tip()
robot.home()           
        

