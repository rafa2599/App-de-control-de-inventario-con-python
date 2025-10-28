from tkinter import *
from tkinter.messagebox import *
import sqlite3
import re
import logging  # Agregado para logging

# Configura logging básico: escribe en 'inventario.log' con nivel INFO
logging.basicConfig(filename='inventario.log', level=logging.INFO, format='%(asctime)s - %(message)s')

""""
MODELO
"""

"""DECORADOR """
def verificar_duplicados(funcion_parametro):
    def wrapper(self, componente, usuario, entero, tree, *args, **kwargs):
        # Se conecta con la base de datos
        cursor = self.con.cursor()
        try:
            # Consulta SQL para verificar si ya existe un registro con el mismo componente y usuario
            sql = 'SELECT * FROM Inventario WHERE componente=? AND usuario=? '
            cursor.execute(sql, (componente, usuario))
            # Obtener el primer resultado de la consulta
            resultado = cursor.fetchone()
        finally:
            cursor.close()

        if resultado:  # Si se encuentra un resultado, significa que el ítem ya existe
            showerror('Error', 'El item ya existe en la base de datos. No se puede insertar')
            logging.warning('Intento de insertar ítem duplicado')  # Logging en lugar de print
        else:
            return funcion_parametro(self, componente, usuario, entero, tree, *args, **kwargs)
    return wrapper

def registrar_operacion(funcion_parametro): 
    def wrapper(self, componente, usuario, entero, tree, *args, **kwargs):
        operacion = f"Operación: {funcion_parametro.__name__}, Args: {componente, usuario, entero}"
        logging.info(operacion)  # Logging en lugar de print
        return funcion_parametro(self, componente, usuario, entero, tree, *args, **kwargs)
    return wrapper

def registrar_eliminacion(funcion_parametro):
    def wrapper(self, *args):
        operacion = f"Operación: {funcion_parametro.__name__}"
        logging.info(operacion)  # Logging en lugar de print
        return funcion_parametro(self, *args)
    return wrapper

class Metodos():
    def __init__(self):
        self.con = sqlite3.connect('INVENTARIO Y SUS PERIFERICOS.db')
        cursor = self.con.cursor()
        try:
            sql = "CREATE TABLE IF NOT EXISTS Inventario(id integer PRIMARY KEY AUTOINCREMENT, codigo text, componente text, usuario text, Departamento text)"  
            cursor.execute(sql) 
            self.con.commit()
        finally:
            cursor.close()

    def validar_datos(self, componente, usuario, entero):
        """Método único para validar componente, usuario y departamento. Devuelve (comp, usr, dept) si todo es válido, o (None, None, None) si falla."""
        comp = self.validar_componente(componente)
        usr = self.validar_usuario(usuario)
        dept = self.boton(entero)
        if comp and usr and dept:
            return comp, usr, dept
        return None, None, None  # Si alguna validación falla, detiene la operación

    def boton(self, entero):
        if entero == 1:
            return 'Recursos Humanos'
        elif entero == 2:
            return 'Contabilidad'
        elif entero == 3:
            return 'Informatica'
        elif entero == 4:
            return 'Secretaria'
        else:
            showerror('Error', 'Por favor seleccione un sector de la empresa')
            return None

    @verificar_duplicados
    @registrar_operacion
    def nuevo(self, componente, usuario, entero, tree):
        mi_componente, mi_usuario, departamento = self.validar_datos(componente, usuario, entero)
        if mi_componente and mi_usuario and departamento:
            mi_id = self.iden()
            binario = self.binario(mi_id)
            cursor = self.con.cursor()
            try:
                datos = (binario, mi_componente, mi_usuario, departamento)
                sql = 'INSERT INTO Inventario (codigo, componente, usuario, departamento) VALUES (?, ?, ?, ?);'
                cursor.execute(sql, datos)
                self.con.commit()
                tree.insert('', 'end', text=str(mi_id), values=(binario, mi_componente, mi_usuario, departamento))
                showinfo('Éxito', 'Ítem agregado correctamente')
            except sqlite3.Error as e:
                showerror('Error', f'Error al insertar en DB: {e}')
                logging.error(f"Error en nuevo(): {e}")
            finally:
                cursor.close()

    def iden(self):
        cursor = self.con.cursor()
        try:
            sql = 'SELECT MAX(id) FROM Inventario'
            cursor.execute(sql)
            id_result = cursor.fetchone()[0]
            self.con.commit()
            return int(id_result) + 1 if id_result is not None else 1
        finally:
            cursor.close()

    def binario(self, mi_id):
        # Simplificado: usa bin() built-in para binario estándar, sin prefijo '0b'
        if mi_id > 0:
            return bin(mi_id)[2:]  # e.g., bin(1)[2:] = '1', bin(2)[2:] = '10'
        return '0'  # Para ID=0 o negativo, aunque no debería ocurrir      

    @registrar_eliminacion
    def eliminar(self, tree):
        item = tree.focus()  # Elijo el item a eliminar
        if item:
            # Obtener los valores del item seleccionado
            item_values = tree.item(item, 'values')
            fila = item_values[0]
            cursor = self.con.cursor()
            try:
                # Eliminar el registro de la base de datos
                sql = 'DELETE FROM Inventario WHERE codigo = ?'
                cursor.execute(sql, (fila,))
                self.con.commit()
                tree.delete(item)  # Eliminar del treeview solo si DB fue exitosa
                showinfo('Éxito', 'Ítem eliminado correctamente')
            except sqlite3.Error as e:
                showerror('Error', f'Error al eliminar de DB: {e}')
                logging.error(f"Error en eliminar(): {e}")
            finally:
                cursor.close()

    @registrar_operacion
    def modificar(self, componente, usuario, entero, tree):
        mi_componente, mi_usuario, departamento = self.validar_datos(componente, usuario, entero)
        if mi_componente and mi_usuario and departamento:
            item = tree.focus()  # Elijo el item a modificar
            if item:
                # Obtener los valores actuales del ítem seleccionado
                item_values = tree.item(item, 'values')
                binario = item_values[0]
                cursor = self.con.cursor()
                try:
                    # Actualizar el registro en la base de datos
                    datos = (mi_componente, mi_usuario, departamento, binario)
                    sql = 'UPDATE Inventario SET componente = ?, usuario = ?, departamento = ? WHERE codigo = ?'
                    cursor.execute(sql, datos)
                    self.con.commit()
                    tree.item(item, values=(binario, mi_componente, mi_usuario, departamento))  # Actualizar treeview solo si DB fue exitosa
                    showinfo('Éxito', 'Ítem modificado correctamente')
                except sqlite3.Error as e:
                    showerror('Error', f'Error al modificar en DB: {e}')
                    logging.error(f"Error en modificar(): {e}")
                finally:
                    cursor.close()
    def buscar(self, tree, filtro, campo):
        """Busca en la DB por filtro en el campo especificado y actualiza el Treeview."""
        # Limpiar el Treeview
        for item in tree.get_children():
            tree.delete(item)
        
        cursor = self.con.cursor()
        try:
            # Consulta SQL con LIKE para búsqueda parcial (case-insensitive)
            sql = f"SELECT id, codigo, componente, usuario, departamento FROM Inventario WHERE {campo} LIKE ?"
            cursor.execute(sql, (f'%{filtro}%',))
            resultados = cursor.fetchall()
            
            # Repoblar el Treeview con resultados
            for row in resultados:
                tree.insert('', 'end', text=str(row[0]), values=(row[1], row[2], row[3], row[4]))
            
            if not resultados:

                showinfo('Búsqueda', 'No se encontraron resultados.')

            else:

                showinfo('Búsqueda', f'Encontrados {len(resultados)} resultados.')
        except sqlite3.Error as e:

            showerror('Error', f'Error en búsqueda: {e}')
            logging.error(f"Error en buscar(): {e}")

        finally:
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
            showerror('Error', 'Usuario no válido, el nombre y apellido debe comenzar con Mayúscula')
            return None