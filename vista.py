from modelo import *
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from modelo import Metodos 


class GUI():
    
    def __init__(self,ventana) :
        self.abmc = Metodos()
        self.ventana = ventana
        self.ventana.title('INVENTARIO DE COMPUTADORAS Y SUS PERIFERICOS')
        self.ventana.minsize( height = 600, width = 900 )


        ############################################# LABELS ###########################################################################################
                
        titulo = Label ( self.ventana,text = 'INVENTARIO DE COMPUTADORAS Y SUS PERIFERICOS', background = 'Steel Blue', foreground = 'White',font = ('Arial','16','bold'))
        titulo.place( x = 0 , y = 0 , width = 1400, height = 40)

        fondo = Label (self.ventana, background='snow4', foreground='Black')
        fondo.place( x = 0 , y = 40 , width = 350 , height = 1200 )

        columna  = Label (self.ventana, background = 'Steel Blue', foreground = 'Black')
        columna.place(x = 350 , y = 40 , width = 30 , height = 1200 )

        ############################################ TITULOS ##########################################################################################
                
        titulo_general = Label(self.ventana, text  = 'Ingrese sus datos',width = 20, background = 'snow4', foreground = 'White',font = ('Arial','13','bold'))
        titulo_general.place( x = 70, y = 60 )

        subt_general = Label(self.ventana , text = 'Ingrese los datos que se le piden a continuación', background = 'snow4', foreground = 'White', font = ('Arial','8','bold'))
        subt_general.place( x = 25 , y = 100 )
                
        titulo_componente = Label(self.ventana, text = "Tipo de componente : ", background = 'snow4', foreground = 'White', font = ('Arial','9','bold'))
        titulo_componente.place(x = 5 , y = 160 )
 
        titulo_usuario = Label(self.ventana, text = 'Nombre de Usuario : ', background = 'snow4', foreground = 'White',font = ('Arial','9','bold'))
        titulo_usuario.place(x = 5 , y = 200 )

        titulo_departamento = Label(self.ventana, text = 'Sector de la empresa', width = 20, background = 'snow4', foreground = 'White',font = ('Arial','13','bold'))
        titulo_departamento.place( x = 80 , y = 300 )

        subt_departamento = Label(self.ventana, text = 'Marque el sector de la empresa a la que pertenece', background = 'snow4', foreground = 'White', font = ('Arial','8','bold'))
        subt_departamento.place ( x = 25 , y = 350 )

        ############################################ VARIABLES DE TKINTER ###########################################################################
        var_entero = IntVar()
        var_componente = StringVar()
        var_usuario = StringVar()

        ############################################ CAMPOS DE ENTRADA ##############################################################################

        entry_componente = Entry(self.ventana, textvariable = var_componente) 
        entry_componente.place(x = 130, y = 160, width = 190,height = 20)
        entry_usuario = Entry(self.ventana, textvariable = var_usuario ) 
        entry_usuario.place(x = 125,y = 200, width = 200, height = 20)

        ############################################ GRILLA ###########################################################################        
        tree = ttk.Treeview(ventana)
        tree["columns"]=("col1", "col2",'col3','col4')
        tree.place(x=380,y=40,height=1200,)

        tree.column("#0", width=25, minwidth=80, anchor=CENTER)
        tree.column("col1", width=250, minwidth=80,anchor=CENTER)
        tree.column("col2", width=200, minwidth=80,anchor=CENTER)
        tree.column("col3", width=250, minwidth=80,anchor=CENTER)
        tree.column("col4", width=250, minwidth=80,anchor=CENTER)

        tree.heading("#0", text = "ID")
        tree.heading('col1',text = 'Codigo del producto')
        tree.heading("col2", text = "Tipo de Componente")
        tree.heading("col3", text = "Nombre del usuario")
        tree.heading("col4", text = "Departamento de la empresa")
        ############################################ BOTONES ###########################################################################

        boton_nuevo = Button (self.ventana, text = "Nuevo", command=lambda: self.abmc.nuevo(var_componente.get(),var_usuario.get(),var_entero.get(),tree), bg = 'Steel Blue', fg = 'White')
        boton_nuevo. place (x =  50, y = 250,width = 80,height = 30)

        boton_eliminar = Button (self.ventana,text = 'Eliminar',command = lambda: self.abmc.eliminar(tree), bg = 'Steel Blue', fg = 'White')
        boton_eliminar.place (x = 135, y = 250,width = 80,height = 30)

    
        boton_modificar = Button (self.ventana,text = 'Modificar',command = lambda: self.abmc.modificar(var_componente.get(),var_usuario.get(),var_entero.get(),tree), bg = 'Steel Blue', fg =  'White')
        boton_modificar.place (x = 220, y = 250,width = 80,height = 30)
        
        boton1 = Radiobutton (self.ventana,text = 'Recursos Humanos',variable = var_entero ,value = 1,command = lambda: self.abmc.boton(var_entero.get()),bg = 'Steel Blue', fg='black')
        boton1.place(x = 25,y = 400)

        boton2 = Radiobutton (self.ventana,text = 'Contabilidad',variable = var_entero,value = 2,command = lambda:self.abmc.boton(var_entero.get(),),bg = 'Steel Blue', fg = 'black')
        boton2.place(x = 25,y = 450)

        boton3 = Radiobutton ( self.ventana,text = 'Departamento de informática',variable = var_entero,value = 3,command=lambda: self.abmc.boton(var_entero.get()),bg = 'Steel Blue', fg = 'black')
        boton3.place(x = 25,y = 500)

        boton4 = Radiobutton (self.ventana,text = 'Secretaría' ,variable = var_entero,value = 4,command = lambda: self.abmc.boton(var_entero.get()),bg = 'Steel Blue', fg = 'black')
        boton4.place(x = 25,y = 550)

                        
