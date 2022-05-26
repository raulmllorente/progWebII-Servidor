# -*- coding: utf-8 -*-
"""
Created on Thu Mar  16 11:26:05 2020

# Object-relational mapping con SQLALCHEMY - https://www.pythoncentral.io/introductory-tutorial-python-sqlalchemy/

@author: manoel.alonso
"""

# DECLARE THE OBJECT / DECLARANDO EL OBJECTO - Object-relational mapping
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
    


# EXTENDING THE BASE OBJECT INTO AN OBJECT CALLED User 
# / EXTENDENDO EL OBJECTO Base EN UN OBJECTO LLAMADO User
from sqlalchemy import Column, Integer, String
class User(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    username = Column(String(15), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(80))

# CREATING A CONNECTION WITH THE DATABASE ENGINE, IT CAN BE ANY SQL Server, MySql, Posgres, etc...
# / CREANDO UNA CONEXIÓN CON EL MOTOR DE BASE DE DATOS, PUEDE SER CUALQUIERA SQL Server, MySql, Posgres, etc...
from sqlalchemy import create_engine
engine = create_engine('sqlite:///./database.db')


# WE RUN create_all SO THAT IF THE TABLE DOES NOT EXIST IT CREATES IT
# / EJECUTAMOS create_all PARA QUE SI LA TABLA NO EXISTE LA CREE
Base.metadata.create_all(engine)
   
# WE CREATE A SESSION TO BE ABLE TO INSERT, UPDATE AND DELETE DATA.
# / CREAMOS UNA SESIÓN PARA PODER INSERTAR, ACTUALIZAR Y BORRAR DATOS.
from sqlalchemy.orm import sessionmaker
DBSession = sessionmaker(bind=engine)
session = DBSession()

# INSERTING A USER
# / INSERTANDO UN USUARIO. 
user1 = User(username='manoel',
             email='manoelgadi@gmail.com',
             password='12345678') 
print("id={};username={};email={};password={}".format(user1.id,
      user1.username,
      user1.email,
      user1.password))

session.add(user1)

print("id={};username={};email={};password={}".format(user1.id,
      user1.username,
      user1.email,
      user1.password))

session.commit()

print("id={};username={};email={};password={}".format(user1.id,
      user1.username,
      user1.email,
      user1.password))


user1.email = 'manoelalonso@xxx.com'
user1.password = 12
session.commit()


# INSERTING ANOTHER USER
# / INSERTANDO OTRO USUARIO. 
user2 = User(username='manoel2',
             email='manoelgadi2@gmail.com',
             password='12345678')    
session.add(user2)
session.commit()



# DOING A SELECT - EQUIVALENT TO
# / HACIENDO UN SELECT - EQUIVALENTE A
"""
SELECT id, username, email, password FROM usarios WHERE users.id = 1
"""
print(session.query(User).filter(User.id == 1))

a = session.query(User).filter(User.id >= 1)
type(a)
user = a[0]
user.username



user = session.query(User).filter(User.id == 1).first()
print("id = {}, username = {}, email = {} ".format(user.id,user.username,user.email))

# UPDATE
user.username='nombre_usuario_cambiado'
session.commit()

# DELETE
user = session.query(User).filter(User.id == 2).first()
session.delete(user)
session.commit()



# EXERCISE - 10 MINUTES DO IT / EJERCICIO - 10 MINUTOS PARA HACERLO
# INSERT: 2 users. / INSERTAR: 2 usuarios.
# INSERT: SELECT THE USER WITH id 3. / INSERTAR: SELECCIONAR EL USUARIO CON id 3.
# DELETE the user with id equal to 1. / BORRAR el usuario con id igual 1.














# 
# 
# LITTLE BREAK and WE ARE BACK IN 10 MINUTES SO THAT YOU CAN FINISH THE EXERCISE
# / PEQUEÑO DESCANSO y VOLVEMOS EN 10 MINUTOS PARA QUE PUEDES TERMINAR EL EJERCICIO
# 
# 









# SOLUTION TO THE EXERCISE
# / SOLUTION TO THE EXERCISE
session.add(User(username='user1',
                 email='mdasd@gmail.com',
                 password='asdsad'))
session.add(User(username='user2',
                 email='mdasd2@gmail.com',
                 password='asd2sad'))
session.commit()

user=session.query(User).filter(User.id==3).first()
user.username
user = session.query(User).filter(User.id==1).first()
session.delete(user)
session.commit()


#CLOSING SESSION
session.close()