#The bromides come as liquids
from opentrons import robot, containers, instruments
path='C:/Users/opentrons/protocols/Suzuki/'

robot.head_speed(x=18000, y=18000, z=5000, a=700, b=700)
rack_number=3
rack_stock_reactants=[]
r_positions=['A1','A2','B1']
r_types=['halide','boronic acid','base']

tiprack_1000 = containers.load("tiprack-1000ul-H", "D3")
source_trough4row = containers.load("trough-12row", "C2")
for i in range(0,rack_number):
    rack_stock_reactants.append(containers.load("FluidX_24_5ml", r_positions[i], r_types[i]))
trash = containers.load("point", "B3")

    # Pipettes SetUp
p1000 = instruments.Pipette(
    name='eppendorf1000',
    axis='b',
    trash_container=trash,
    tip_racks=[tiprack_1000],
    max_volume=1000,
    min_volume=30,
    channels=1,
)

loc_list=[]
vol_list=[]

locs_as_str=['']*rack_number
vols_as_str=['']*rack_number

copies=6
molarity=0.8
conv_factor=1000

r_scale=[]
with open(path+'reaction_details.csv') as f:
    f.readline()
    for line in f:
        ls=line.split(',')
        r_scale.append(float(ls[1]))

#5 reactions: 2 replicates with the actual reaction, 2 with a negative control (no catalyst), one done manually
#Need 3 times the amount to account for possible errors
#Number of moles used = ls[6]
#Reaction number (1 or 2 here) = ls[3]
with open(path+'solids.csv') as f:
    f.readline()
    for line in f:
        ls = line.split(',')
        if ls[1]=='24_rack4' or ls[1]=='24_rack1' or ls[1]=='24_rack3':
            continue
        locs_as_str[int(ls[1][-1]) - 1] += (ls[0] + ' ')
        vols_as_str[int(ls[1][-1]) - 1] += (str(round(conv_factor*float(ls[12])/molarity,1)) + ' ')

for num in range(0, rack_number):
    loc_list.append(locs_as_str[num].split())
    vol_list.append(vols_as_str[num].split())
solvent_location = 'A1'
#DMA = A1

print(loc_list)
print(vol_list)
    
p1000.pick_up_tip()
for num in range (0,rack_number):
    for i, destination_location in enumerate(loc_list[num]):
        vol_to_dispense = [vol_list[num][i]]
        if vol_to_dispense != 0:
            p1000.transfer(vol_to_dispense, source_trough4row.wells(solvent_location), rack_stock_reactants[num].wells(destination_location).top(-5), new_tip = 'never')
p1000.drop_tip()
robot.home()
#print(robot.command1s())
