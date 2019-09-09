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
    halide TEXT, \
    halide_qty FLOAT, \
    borac TEXT, \
    borac_qty FLOAT, \
    base1 TEXT, \
    base1_qty FLOAT, \
    base2 TEXT, \
    base2_qty FLOAT, \
    ligand TEXT, \
    ligand_qty FLOAT, \
    catalyst TEXT, \
    catalyst_qty FLOAT, \
    solvent1 TEXT, \
    solvent1_qty FLOAT, \
    solvent2 TEXT, \
    solvent2_qty FLOAT, \
    solvent3 TEXT, \
    solvent3_qty FLOAT, \
    temperature FLOAT, \
    time FLOAT, \
    rn_order \
);')


with open('reactions.csv') as f:
    for line in f:
        to_insert="INSERT INTO reactions VALUES('"
        line=line.replace("'",'’')
        ls=line.split('^')
        if ls[0]=='Reaction scale':
            continue
        ls[-1]=ls[-1].replace('\n','')
        for i in range(1,13,2):
            if ls[i]=='':
                to_insert+="none', '0', '"
            else:
                rows=cur.execute("SELECT mol_weight FROM compounds where name='"+ls[i]+"';")
                for row in rows:
                    to_insert+=ls[i]+"', '"+str(float(ls[0])*float(ls[i+1])*float(row[0]))+"', '"
        for i in range(13,19,2):
            if ls[i+1]=='':
                ls[i]="none"
                ls[i+1]=0
            to_insert+=ls[i]+"', '"+str(float(ls[0])*float(ls[i+1]))+"', '"
        for i in range(19,22):
            to_insert+=(ls[i]+(i<21)*"', '"+(i==21)*"');")
        cur.execute(to_insert)
        #cur.execute("SELECT * FROM reactions")
        #print(cur.fetchall())
cur.close()
con.close()
