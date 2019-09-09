import sqlite3
import pandas as pd

con = sqlite3.connect('new_rachael_3.db')
cur = con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS compounds ( \
    name TEXT PRIMARY KEY, \
    smiles TEXT, \
    mol_weight FLOAT, \
    type TEXT \
);')

compounds = pd.read_csv('compounds.csv')
for i in range(0, len(compounds)):
    cur.execute("INSERT INTO compounds VALUES(?,?,?,?)", (compounds.iloc[i]['name'],
                                                          compounds.iloc[i]['smiles'],
                                                          compounds.iloc[i]['molecular_weight'],
                                                          compounds.iloc[i]['type']))


cur.execute('CREATE TABLE IF NOT EXISTS reactions ( \
    number INTEGER PRIMARY KEY, \
    rn_scale FLOAT, \
    temperature FLOAT, \
    time FLOAT \
);')


reactions = pd.read_csv('new_reactions.csv')

for i in range(0, len(reactions)):
    cur.execute("INSERT INTO reactions VALUES(?,?,?,?)", (reactions.iloc[i]['Reaction number'],
                                                          reactions.iloc[i]['Reaction scale'],
                                                          reactions.iloc[i]['Temperature'],
                                                          reactions.iloc[i]['Time']))

cur.execute('CREATE TABLE IF NOT EXISTS protocol_steps ( \
    reactant TEXT, \
    operation TEXT, \
    rn_number INTEGER, \
    step_number INTEGER, \
    quantity FLOAT \
);')

protocol_steps = pd.read_csv('protocol_steps.csv')
for i in range(0, len(protocol_steps)):
    cur.execute("SELECT rn_scale FROM reactions where number=?", str(protocol_steps.iloc[i]['reaction']))
    rsc = cur.fetchall()[0][0]
    if protocol_steps.iloc[i]['dilution (if solvent)'] != 0:
        quantity = rsc*protocol_steps.iloc[i]['dilution (if solvent)']
    else:
        cur.execute("SELECT mol_weight FROM compounds where name=(?,)", (protocol_steps.iloc[i]['reactant']))
        mw = cur.fetchall()[0][0]
        quantity = rsc*mw

    cur.execute("INSERT INTO protocol_steps VALUES (?,?,?,?,?)", (protocol_steps.iloc[i]['reactant'],
                                                                  protocol_steps.iloc[i]['operation'],
                                                                  protocol_steps.iloc[i]['reaction'],
                                                                  protocol_steps.iloc[i]['step'],
                                                                  quantity))


cur.close()
con.close()
