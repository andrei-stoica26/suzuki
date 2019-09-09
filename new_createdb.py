import sqlite3
con=sqlite3.connect('new.db')
cur=con.cursor()
cur.execute('DROP TABLE IF EXISTS compounds')
cur.execute('CREATE TABLE compounds ( \
    name TEXT PRIMARY KEY, \
    smiles TEXT, \
    mol_weight FLOAT, \
    type TEXT \
);')


with open('compounds.csv') as f:
    for line in f:
        line=line.replace("'",'’')
        ls=line.split('^')
        if ls[0]=='name':
            continue
        ls[-1]=ls[-1].replace('\n','')
        cur.execute("INSERT INTO compounds VALUES('"+"', '".join(ls)+"');")

cur.execute('DROP TABLE IF EXISTS reactions')
cur.execute('CREATE TABLE reactions ( \
    number INTEGER PRIMARY KEY, \
    rn_scale FLOAT, \
    temperature FLOAT, \
    time FLOAT \
);')


with open('new_reactions.csv') as f:
    for line in f:
        ls=line.split(',')
        if ls[0]=='Reaction number':
            continue
        ls[-1]=ls[-1].replace('\n','')
        cur.execute("INSERT INTO reactions VALUES('"+"', '".join(ls)+"');")

cur.execute('DROP TABLE IF EXISTS protocol_steps')
cur.execute('CREATE TABLE protocol_steps ( \
    reactant TEXT, \
    operation TEXT, \
    rn_number INTEGER, \
    step_number INTEGER, \
    quantity FLOAT \
);')

with open('protocol_steps.csv') as f:
    for line in f:
        line=line.replace("'",'’')
        ls=line.split('^')
        if ls[0]=='reactant':
            continue
        ls[-1]=ls[-1].replace('\n','')
        cur.execute("SELECT rn_scale FROM reactions where number='"+ls[2]+"';")
        rsc=cur.fetchall()[0][0]
        #if solvent
        if ls[4]!='0':
            ls[4]=str(rsc*float(ls[4]))
        else:
            cur.execute("SELECT mol_weight FROM compounds where name='"+ls[0]+"';")
            mw=cur.fetchall()[0][0]
            ls[4]=str(rsc*mw)
        cur.execute("INSERT INTO protocol_steps VALUES('"+"', '".join(ls)+"');")
    #cur.execute("SELECT * FROM protocol_steps")
    #print(cur.fetchall())
cur.close()
con.close()
