import sqlite3
import pandas as pd

con = sqlite3.connect('suzuki.db')
cur = con.cursor()
cur.execute('DROP TABLE IF EXISTS compounds')
cur.execute('CREATE TABLE compounds ( \
    name TEXT PRIMARY KEY, \
    smiles TEXT, \
    mol_weight FLOAT, \
    type TEXT \
);')

compounds = pd.read_csv('compounds.csv')
compounds['name']=compounds['name'].str.replace("'","’")
for i in range(0, len(compounds)):
    cur.execute("INSERT INTO compounds VALUES(?,?,?,?)", (compounds.iloc[i]['name'],
                                                          compounds.iloc[i]['smiles'],
                                                          compounds.iloc[i]['molecular_weight'],
                                                          compounds.iloc[i]['type']))

cur.execute('DROP TABLE IF EXISTS reactions')
cur.execute('CREATE TABLE reactions ( \
    number INTEGER PRIMARY KEY, \
    rn_scale FLOAT, \
    temperature FLOAT, \
    time FLOAT \
);')


reactions = pd.read_csv('new_reactions.csv',sep='\s*,\s*',engine='python').replace("'",'’')


for i in range(0, len(reactions)):
    cur.execute("INSERT INTO reactions VALUES(?,?,?,?)", (reactions.iloc[i]['Reaction number'],
                                                          reactions.iloc[i]['Reaction scale'],
                                                          reactions.iloc[i]['Temperature'],
                                                          reactions.iloc[i]['Time']))

cur.execute('DROP TABLE IF EXISTS protocol_steps')
cur.execute('CREATE TABLE protocol_steps ( \
    reactant TEXT, \
    operation TEXT, \
    rn_number INTEGER, \
    step_number INTEGER, \
    quantity FLOAT, \
    is_solvent INTEGER \
);')

protocol_steps = pd.read_csv('protocol_steps.csv')
protocol_steps['reactant']=protocol_steps['reactant'].str.replace("'","’")

for i in range(0, len(protocol_steps)):
    cur.execute("SELECT rn_scale FROM reactions where number=?", str(protocol_steps.iloc[i]['reaction']))
    rsc = cur.fetchall()[0][0]
    if protocol_steps.iloc[i]['dilution (if solvent)'] != 0:
        quantity = rsc*protocol_steps.iloc[i]['dilution (if solvent)']
        is_solvent=1
    else:
        cur.execute("SELECT mol_weight FROM compounds where name='"+protocol_steps.iloc[i]['reactant']+"';")
        mw = cur.fetchall()[0][0]
        quantity = rsc*mw*float(protocol_steps.iloc[i]['moles (if not solvent)'])
        is_solvent=0
    cur.execute("INSERT INTO protocol_steps VALUES (?,?,?,?,?,?)", (protocol_steps.iloc[i]['reactant'],
                                                                  protocol_steps.iloc[i]['operation'],
                                                                  int(protocol_steps.iloc[i]['reaction']),
                                                                  int(protocol_steps.iloc[i]['step']),
                                                                  quantity,is_solvent))

#cur.execute("SELECT * FROM protocol_steps")
#print(cur.fetchall())
cur.close()
con.commit()
con.close()
