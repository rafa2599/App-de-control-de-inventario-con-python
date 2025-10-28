from tkinter import *
from tkinter.messagebox import *
import sqlite3
import re

""""
MODELO

"""

"""DECORADOR """
def verficar_duplicados (funcion_parametro):
    def wrapper (self,componente, usuario, entero, tree,*args,**kwargs):
        
       
        # Se conecta con la base de datos
        cursor = self.con.cursor()
        # Consulta SQL para verificar si ya existe un registro con el mismo componente y usuario
        sql='SELECT * FROM Inventario WHERE componente=? AND usuario=? '
        cursor.execute(sql,(componente,usuario))
        # Obtener el primer resultado de la consulta
        resultado=cursor.fetchone()
        # Cerramos el cursor
        cursor.close()

        if resultado: # Si se encuentra un resultado, significa que el ítem ya existe
            showerror('Error', 'El item ya existe en la base de datos. No se puede insertar')
            print('El item ya existe en la base de datos. No se puede insertar')
            
        else :
            return funcion_parametro(self,componente, usuario, entero, tree,*args,**kwargs)
    return wrapper

def registrar_operacion(funcion_parametro): 
    def wrapper (self,componente, usuario, entero, tree,*args,**kwargs):
        operacion = f"Operación: {funcion_parametro.__name__}, Args: {componente, usuario, entero}"
        print(operacion) 
        return funcion_parametro(self,componente, usuario, entero, tree,*args,**kwargs)
    return wrapper


def regristrar_eliminacion(funcion_parametro):
    def wrapper (self,*args,):
        operacion = f"Operación: {funcion_parametro.__name__}"
        print(operacion) 
        return funcion_parametro(self,*args)
    return wrapper


class Metodos():
    def __init__(self,):

        self.con = sqlite3.connect('INVENTARIO Y SUS PERIFERICOS.db')
        cursor = self.con.cursor() 
        sql = "CREATE TABLE IF NOT EXISTS Inventario(id integer PRIMARY KEY AUTOINCREMENT,codigo text, componente text, usuario text, Departamento text)"  
        cursor.execute(sql) 
        self.con.commit()




    def boton(self,entero):
        if entero == 1:
            return 'Recursos Humanos'
        elif entero == 2:
            return 'Contabilidad'
        elif entero == 3:
            return 'Departamento de informática'
        elif entero == 4:
            return 'Secretaría'
        else:
            showerror('Error', 'Por favor seleccione un sector de la empresa')
            return None



    @verficar_duplicados
    @registrar_operacion
    def nuevo(self,componente, usuario, entero, tree):

        departamento = self.boton(entero) 
        if departamento:
            mi_id = self.iden()

            binario = self.binario(mi_id)

            mi_componente = self.validar_componente(componente)

            mi_usuario = self.validar_usuario(usuario)

            if mi_componente is not None and mi_usuario is not None:

                tree.insert('', 'end', text=str(mi_id), values = (binario, mi_componente, mi_usuario, departamento))

                cursor = self.con.cursor()

                datos = (binario, mi_componente, mi_usuario, departamento)

                sql = 'INSERT INTO Inventario (codigo, componente, usuario, departamento) VALUES (?, ?, ?, ?);'

                cursor.execute(sql, datos)
                self.con.commit()
                cursor.close()


    def iden(self,):

        cursor = self.con.cursor() #Me conecto con la base de batos

        sql = 'SELECT MAX(id) FROM Inventario' #Selecionamos el ultimo id registrado

        cursor.execute(sql) #Ejecutamos la acción

        id = cursor.fetchone()[0] #Con el metodo fetchone(), seleccionamos el primer valor de la ultima fila de datos 
        #en este caso el id.
        self.con.commit()

        return int(id) + 1 if id is not None else 1 # si el valor del id no es nulo , lo retornamos en forma de entero


    def binario (self,mi_id):

        if mi_id >= 0:
            mi_id += 1
            binario=' '
            codigo=  mi_id + 0
            if mi_id == 1 :
                binario = '01'
            else:
                while codigo > 0 :
                    residuo = codigo % 2
                    codigo= codigo // 2
                    binario = str(residuo) + binario

        return binario        

    @regristrar_eliminacion
    def eliminar(self,tree):
        cursor = self.con.cursor() #Me conecto con la base de batos
        item = tree.focus()  # Elijo el item a eliminar
        if item:
            # Obtener los valores del item seleccionado
            item_values = tree.item(item, 'values')
            fila = item_values[0]
            
            # Eliminar el item del treeview
            tree.delete(item)
            # Eliminar el registro de la base de datos
            sql = 'DELETE FROM Inventario WHERE codigo = ?'
            cursor.execute(sql, (fila,))
            self.con.commit()
        
        cursor.close() 

    @registrar_operacion
    def modificar(self,componente, usuario, entero, tree):
        cursor = self.con.cursor()  #Me conecto con la base de batos
        item = tree.focus() # Elijo el item a modificar
        
        if item:
            # Obtener los valores actuales del ítem seleccionado
            item_values = tree.item(item, 'values')
            binario = item_values[0]
            
            # Nuevos valores
            new_componente = self.validar_componente (componente)
            new_usuario = self.validar_usuario (usuario)
            new_departamento = self.boton (entero)
            
            # Actualizar el ítem en el treeview
            tree.item(item, values=(binario, new_componente, new_usuario, new_departamento))
            
            # Actualizar el registro en la base de datos
            datos = (new_componente, new_usuario, new_departamento, binario)
            sql = 'UPDATE Inventario SET componente = ?, usuario = ?, departamento = ? WHERE codigo = ?'
            cursor.execute(sql, datos)
            self.con.commit()
        
        cursor.close()




    def validar_componente(self, componente):
        opciones_validas = ['CPU', 'NOTEBOOK', 'MOUSE', 'TECLADO', 'MONITOR', 'IMPRESORA']
        comp = componente.upper()
        if comp in opciones_validas:

            return comp
        else:
            showerror('Error', 'Componente no válido')
            return None

    def validar_usuario(self, usuario):
        patron_usuario = r'^[A-Z][a-z]+ [A-Z][a-z]+$'
        if re.match(patron_usuario, usuario):
            return usuario
        else:
            showerror('Error', 'Usuario no válido,el nombre y apellido debe comenzar con Mayuscula')
            return None
    

