from sqlalchemy import engine, Table, Column, Integer, String, MetaData, update, text

url = 'mysql://root:root@localhost/zoo'
engine = create_engine(url, echo=True)
connection = engine.connect()
meta = MetaData(engine)

#creating the new table 'stato'
newTable = Table('stato', meta,
Column ('idStato', Integer, primary_key=True),
Column ('nome', String),
Column ('popolazione', Integer))

#executing create table
meta.create_all(engine)

#inserting data into 'stato'
stmt1 = newTable.insert().values(nome = 'Francia', popolazione = 20000000)
stmt2 = newTable.insert().values(nome = 'Spagna', popolazione = 140000000)
stmt3 = newTable.insert().values(nome = 'Germania', popolazione = 90000000)
stmt4 = newTable.insert().values(nome = 'Svizzera', popolazione = 130000000)

#executing inserts
connection.execute(stmt1)
connection.execute(stmt2)
connection.execute(stmt3)
connection.execute(stmt4)

#updating stato, it replaces the current name with "Romania" where idStato == 1
updatedTable = update(newTable)
value = updatedTable.values({"Nome":"Romania"})
condition = value.where(newTable.c.idStato == 1)

#executing update
connection.execute(updatedTable)

#deleting from stato where idStato = 1
deletedData = newTable.delete().where(newTable.c.idStato == 1)

#executing delete
engine.execute(deletedData)

#query1: selecting all the empty boxes
sql = text("select * from box where idBox not in (select idBox from box inner join Animali as A on idBox = A.Box) and idBox not in (select idBox from box inner join Piante as P on idBox = P.Box)") 
results = engine.execute(sql)
  
#Display the records
for line in results:
    print(line, "\n")
    
#query2: selecting all the employes who live in "Rome"
sql = text("select nome, cognome from impiegati as I inner join reparto as R on I.Reparto = R.idReparto where R.zoo = (select idZoo from zoo, citta where zoo.Citta = citta.IDCitta and citta.Nome = 'Roma' )") 
results = engine.execute(sql)
  
#Display the records
for line in results:
    print(line, "\n")
    
#query3: selecting all the departments that don't contain plants
sql = text("select idReparto from box inner join reparto on box.Reparto = reparto.idReparto where idBox not in (select idBox from  piante inner join box on piante.box = box.idBox )") 
results = engine.execute(sql)
  
#Display the records
for line in results:
    print(line, "\n")