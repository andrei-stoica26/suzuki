from opentrons import robot, containers, instruments
import pandas as pd
all=pd.read_csv('new_protocol_steps.csv')

containers.create(
    'FluidX_24_5ml',
    grid=(4,6),
    spacing=(18,18),
    diameter=13,
    depth=48
    )

robot.head_speed(x=18000, y=18000, z=5000, a=700, b=700)
rack_number=4
rack_stock_reactants=[]
r_positions=['A1','A2','B1','B2']
r_types=['halide','boronic acid','base','catalyst']

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
    tip_racks=tiprack_1000,
    max_volume=1000,
    min_volume=30,
    channels=1,
)

loc_list=[]
vol_list=[]
for num in range (0,rack_number):
    loc_list.append(['A1','A2'])
    vol_list.append(['100','100'])
solvent_location='A2'
    
p1000.pick_up_tip()
for num in range (0,rack_number):
    for i, destination_location in enumerate(loc_list[num]):
        vol_to_dispense = [vol_list[num][i]]
        if vol_to_dispense != 0:
           p1000.transfer(vol_to_dispense, source_trough4row.wells(solvent_location), rack_stock_reactants[num].wells(destination_location).top(-5), new_tip = 'never')
p1000.drop_tip()
robot.home()
#print(robot.commands())
