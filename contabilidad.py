from cgitb import text
from contextlib import ContextDecorator
from datetime import datetime
from decimal import Decimal
from email.policy import default
from faulthandler import disable
from multiprocessing import connection
from multiprocessing.sharedctypes import Value
from os import listxattr
from stringprep import c22_specials
from time import strftime
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
import tkinter.font as tkFont
from tkinter.ttk import Combobox, Treeview
from turtle import bgcolor, fillcolor, width
import pymysql
import requests
import json
from urllib.request import urlopen
connection=pymysql.connect(host='localhost',user='****',passwd='******',database='contabilidad')
cursor = connection.cursor()
root=Tk()
root.geometry('1400x700')
root.title('nombre contabilidad hogar')
menubar= Menu(root)
electrodomesticos=['balay encimera induccion','teka fregadero','balay microondas','balay lavavajillas','balay horno','balay frigorifico','balay campana','bosch lavadora','bosch plancha','secador','lg television','caldera gas','robot cocina lidl','cafetera','dyson aspiradora','balay secadora','descalcificador']
electrodomesticos.sort()
categorias=['AHORRO','MTO DESCALCIFICADOR','ALIMENTACION','MTO ELECTRICO','CONTRIBUCION','SEGURO HOGAR','LUZ','AGUA','GAS','INTERNET','OCIO A','OCIO B','HOGAR','SEGURO VEHICULO','LAVADO VEHICULO','ITV','VADO','NEUMATICOS','AMORTIZACION VEHICULO','MTO VEHICULO','SELLO VEHICULO']
categorias.sort()
meses=['AÑO COMPLETO','ENERO','FEBRERO','MARZO','ABRIL','MAYO','JUNIO','JULIO','AGOSTO','SEPTIEMBRE','OCTUBRE','NOMVIEMBRE','DICIEMBRE']
#LA UNICA DIFERENCIA ENTRE CATEGORIAS Y CATEGORIAS INGRESO ES QUE EN CATEGORIAS_INGRESO:APARECE 'VALORES FIJOS'
#VALORES FIJOS DEBE DE APARECER DE ESTE MODO PARA INGRESAR DE 'UNA SOLA VEZ' TODOS LOS VALORES QUE INGRESAMOS MENSUALMENTE
categorias_ingreso=['AHORRO','MTO DESCALCIFICADOR','ALIMENTACION','MTO ELECTRICO','VALORES FIJOS','CONTRIBUCION','SEGURO HOGAR','LUZ','AGUA','GAS','INTERNET','OCIO A','OCIO B','HOGAR','SEGURO VEHICULO','LAVADO VEHICULO','ITV','VADO','NEUMATICOS','AMORTIZACION VEHICULO','MTO VEHICULO','SELLO VEHICULO']
categorias_ingreso.sort()
#ASIGNAMOS VALOR A LOS ELEMENTOS QUE INTRODUCIREMOS AL PULSAR 'VALORES FIJOS'
ocio_a=1
ocio_b=1
hogar=1
seguro_vehiculo=1
lavado_vehiculo=1
neumaticos=1
amortizacion_vehiculo=1
mto_vehiculo=1
suma_valores_fijos=[ocio_a,ocio_b,hogar,seguro_vehiculo,lavado_vehiculo,neumaticos,amortizacion_vehiculo,mto_vehiculo]
suma_valores_fijos=sum(suma_valores_fijos)
global suma_acumulado
suma_acumulado=0
def coste_mto_electrico():
    #Creo esta funcion con la misma consulta que "conocer_mto_electrico" porque necesito el dato al inicio y si se lo pido a la funcion
    #'conocer_mto_electrico' se me abre la ventana de esa función
    consulta=("select cod_cacharro,fecha_compra,precio,vida_util,fecha_inicio_amortizacion from info_cacharros order by fecha_compra asc;")
    cursor.execute(consulta)
    respuesta = cursor.fetchall()
    global acumular_precio
    acumular_precio=0
    #Insertamos valores de la consulta
    contador=0
    global suma_acumulado
    suma_acumulado=0
    for n in range (len(respuesta)):
        electrodomestico=respuesta[n][0]
        electrodomestico=str(electrodomestico)
        fecha_compra=respuesta[n][1]
        fecha_compra=str(fecha_compra)
        fecha_compra=fecha_compra[8::]+'/'+fecha_compra[5:-3]+'/'+fecha_compra[0:-6]
        precio=respuesta[n][2]
        precio=str(precio)
        precio=precio+'€'
        vida_util=respuesta[n][3]
        strvida_util=vida_util
        strvida_util=str(vida_util)
        strvida_util=strvida_util+' años'
        coste_mensual=respuesta[n][2]
        coste_mensual=coste_mensual/vida_util
        coste_mensual=coste_mensual/12
        coste_mensual=round(coste_mensual,2)
        acumular_precio+=coste_mensual
        coste_mensual=str(coste_mensual)
        strcoste_mensual=coste_mensual+'€'
        coste_mensual=float(coste_mensual)
        fecha_inicio_amortizacion=respuesta[n][4]
        fecha_original=fecha_inicio_amortizacion
        fecha_inicio_amortizacion=str(fecha_inicio_amortizacion)
        fecha_inicio_amortizacion=fecha_inicio_amortizacion[8::]+'/'+fecha_inicio_amortizacion[5:-3]+'/'+fecha_inicio_amortizacion[0:-6]
        consulta=("select importe from inminente where categoria=%s;")
        datos=(electrodomestico)
        cursor.execute(consulta,datos)
        cantidades_ingresadas_gastadas_electrodomestico = cursor.fetchall()
        suma=0
        #Conocer el número de veces que se ha insertado MTO ELECTRICO
        consulta=("select count(categoria) from inminente where categoria='MTO ELECTRICO' and fecha>=%s")
        datos=(fecha_original)
        cursor.execute(consulta,datos)
        numero_veces_mto_electrico = cursor.fetchone()
        numero_veces_mto_electrico=str(numero_veces_mto_electrico)
        numero_veces_mto_electrico=numero_veces_mto_electrico[1:-2]
        numero_veces_mto_electrico=int(numero_veces_mto_electrico)
        
        for n in range(len(cantidades_ingresadas_gastadas_electrodomestico)):
            numero=cantidades_ingresadas_gastadas_electrodomestico[n]
            numero=str(numero)
            numero=numero[1:-2]
            numero=float(numero)
            suma+=numero
        acumulado=(coste_mensual*numero_veces_mto_electrico)+suma
        acumulado=round(acumulado,2)
        stracumulado=str(acumulado)
        stracumulado=stracumulado+'€'
        suma_acumulado+=acumulado
        contador+=1
    suma_acumulado=round(suma_acumulado,2)
    return suma_acumulado

def conocer_mto_electrico():
    ventana_conocer_mto_electrico = Toplevel()
    ventana_conocer_mto_electrico.geometry('1400x700')
    ventana_conocer_mto_electrico.title('CONOCER MANTENIMIENTO ELÉCTRICO ESPINOSA 25')
    def cerrar_ventana_conocer_mto():
        if messagebox.askokcancel("SALIR", "¿Desea salir de CONOCER MANTENIMIENTO ELÉCTRICO ESPINOSA 25?",parent = ventana_conocer_mto_electrico):
            ventana_conocer_mto_electrico.destroy()

    consulta=("select cod_cacharro,fecha_compra,precio,vida_util,fecha_inicio_amortizacion from info_cacharros order by fecha_compra asc;")
    cursor.execute(consulta)
    respuesta = cursor.fetchall()
    my_tree=Treeview(ventana_conocer_mto_electrico)
    #definimos columnas
    my_tree['columns']=('ELECTRODOMESTICO','FECHA COMPRA','PRECIO','VIDA UTIL ESPERADA','COSTE MENSUAL','FECHA INICIO AMORTIZACION','CANTIDAD ACUMULADA')
    #Formateamos columnas
    my_tree.column('#0',width=0,minwidth=0,stretch=NO)#Según codemy es una columna fantasma y tiene que estar...
    my_tree.column('ELECTRODOMESTICO',anchor=W,width=180)
    my_tree.column('FECHA COMPRA',anchor=W,width=150)
    my_tree.column('PRECIO',anchor=W,width=80)
    my_tree.column('VIDA UTIL ESPERADA',anchor=W,width=180)
    my_tree.column('COSTE MENSUAL',anchor=W,width=150)
    my_tree.column('FECHA INICIO AMORTIZACION',anchor=W,width=240)
    my_tree.column('CANTIDAD ACUMULADA',anchor=W,width=240)
    #Crear encabezado
    my_tree.heading('#0',text='Label1',anchor=W)
    my_tree.heading('ELECTRODOMESTICO',text='ELECTRODOMÉSTICO',anchor=W)
    my_tree.heading('FECHA COMPRA',text='FECHA COMPRA',anchor=CENTER)
    my_tree.heading('PRECIO',text='PRECIO',anchor=W)
    my_tree.heading('VIDA UTIL ESPERADA',text='VIDA ÚTIL ESPERADA',anchor=W)
    my_tree.heading('COSTE MENSUAL',text='COSTE MENSUAL',anchor=W)
    my_tree.heading('FECHA INICIO AMORTIZACION',text='FECHA INICIO AMORTIZACIÓN',anchor=W)
    my_tree.heading('CANTIDAD ACUMULADA',text='CANTIDAD ACUMULADA',anchor=W)
    my_tree.grid(row=1,column=0,padx=30)
    global acumular_precio
    acumular_precio=0
    #Insertamos valores de la consulta
    contador=0
    global suma_acumulado
    suma_acumulado=0
    for n in range (len(respuesta)):
        electrodomestico=respuesta[n][0]
        electrodomestico=str(electrodomestico)
        fecha_compra=respuesta[n][1]
        fecha_compra=str(fecha_compra)
        fecha_compra=fecha_compra[8::]+'/'+fecha_compra[5:-3]+'/'+fecha_compra[0:-6]
        precio=respuesta[n][2]
        precio=str(precio)
        precio=precio+'€'
        vida_util=respuesta[n][3]
        strvida_util=vida_util
        strvida_util=str(vida_util)
        strvida_util=strvida_util+' años'
        coste_mensual=respuesta[n][2]
        coste_mensual=coste_mensual/vida_util
        coste_mensual=coste_mensual/12
        coste_mensual=round(coste_mensual,2)
        acumular_precio+=coste_mensual
        coste_mensual=str(coste_mensual)
        strcoste_mensual=coste_mensual+'€'
        coste_mensual=float(coste_mensual)
        fecha_inicio_amortizacion=respuesta[n][4]
        fecha_original=fecha_inicio_amortizacion
        fecha_inicio_amortizacion=str(fecha_inicio_amortizacion)
        fecha_inicio_amortizacion=fecha_inicio_amortizacion[8::]+'/'+fecha_inicio_amortizacion[5:-3]+'/'+fecha_inicio_amortizacion[0:-6]
        consulta=("select importe from inminente where categoria=%s;")
        datos=(electrodomestico)
        cursor.execute(consulta,datos)
        cantidades_ingresadas_gastadas_electrodomestico = cursor.fetchall()
        suma=0
        #Conocer el número de veces que se ha insertado MTO ELECTRICO
        consulta=("select count(categoria) from inminente where categoria='MTO ELECTRICO' and fecha>=%s")
        datos=(fecha_original)
        cursor.execute(consulta,datos)
        numero_veces_mto_electrico = cursor.fetchone()
        numero_veces_mto_electrico=str(numero_veces_mto_electrico)
        numero_veces_mto_electrico=numero_veces_mto_electrico[1:-2]
        numero_veces_mto_electrico=int(numero_veces_mto_electrico)
        
        for n in range(len(cantidades_ingresadas_gastadas_electrodomestico)):
            numero=cantidades_ingresadas_gastadas_electrodomestico[n]
            numero=str(numero)
            numero=numero[1:-2]
            numero=float(numero)
            suma+=numero
        acumulado=(coste_mensual*numero_veces_mto_electrico)+suma
        acumulado=round(acumulado,2)
        stracumulado=str(acumulado)
        stracumulado=stracumulado+'€'
        suma_acumulado+=acumulado
        contador+=1
        my_tree.insert(parent='',index='end',iid=contador,text='Parent',values=(electrodomestico,fecha_compra,precio,strvida_util,strcoste_mensual,fecha_inicio_amortizacion,stracumulado))
    suma_acumulado=round(suma_acumulado,2)
   
    acumular_precio=round(acumular_precio,2)
    stracumular_precio=acumular_precio
    stracumular_precio=str(acumular_precio)
    stracumular_precio='CUOTA MENSUAL:'+stracumular_precio+'€'

    strsuma_acumulado=str(suma_acumulado)
    stracumular_total='TOTAL ACUMULADO:'+strsuma_acumulado+'€'
   
    cuota=Label(ventana_conocer_mto_electrico,text=stracumular_precio+'        '+stracumular_total)
    cuota.grid(row=2,column=0)
    
    ventana_conocer_mto_electrico.protocol("WM_DELETE_WINDOW", cerrar_ventana_conocer_mto)
    ventana_conocer_mto_electrico.mainloop()
    
def registrar_ingresos():
    ventana_registrar_ingresos = Toplevel()
    ventana_registrar_ingresos.geometry('1400x700')
    ventana_registrar_ingresos.title('REGISTRO INGRESOS')
    ventana_registrar_ingresos.configure(bg='#CEF6E3')

    #CABECERA: CATEGORIA-IMPORTE-FECHA-COMENTARIOS DE LA VENTANA "REGISTRAR INGRESOS"
    categoria=Label(ventana_registrar_ingresos,text='CATEGORIA')
    categoria.configure(font=('Ubuntu Light',25),bg='#CEF6E3')
    categoria.grid(row=0,column=0,padx=5,pady=5)
    importe=Label(ventana_registrar_ingresos,text='IMPORTE')
    importe.configure(font=('Ubuntu Light',25),bg='#CEF6E3')
    importe.grid(row=0,column=1,padx=5,pady=5)
    fecha=Label(ventana_registrar_ingresos,text='FECHA')
    fecha.configure(font=('Ubuntu Light',25),bg='#CEF6E3')
    fecha.grid(row=0,column=2,padx=5,pady=5)
    comentarios=Label(ventana_registrar_ingresos,text='COMENTARIOS')
    comentarios.configure(font=('Ubuntu Light',25),bg='#CEF6E3')
    comentarios.grid(row=0,column=3,padx=5,pady=5)
    #VALIDAR IMPORTE Y FECHA
    def comprobar_datos_ingresos():
        #IMPORTE
        correcto=False
        usa_comas=False
        fecha_correcta=True
        try:
            try:
                datetime.strptime(fecha_categoria.get(),'%d-%m-%Y')
                fecha_categoria.config(highlightbackground = "grey", highlightcolor= "white")
            except:
                fecha_categoria.config(highlightbackground = "red", highlightcolor= "red")
                fecha_correcta=False
        except:
            pass    
        if fecha_correcta==False:
            messagebox.showwarning(message="FECHA NO VÁLIDA", title="ERROR",parent=ventana_registrar_ingresos)
        if entrada_importe_categoria.get().isdigit() or entrada_importe_categoria.get().replace('.','').isdigit() and entrada_importe_categoria.get().count(".")==1:
            correcto=True
            entrada_importe_categoria.config(highlightbackground='grey',highlightcolor='white')
        elif entrada_importe_categoria.get().replace(',','').isdigit():
            usa_comas=True
            entrada_importe_categoria.config(highlightbackground='red',highlightcolor='red')

        else:
            entrada_importe_categoria.delete(0,END)
            entrada_importe_categoria.insert(0,0)
            correcto=True

        if usa_comas==True:
            messagebox.showwarning(message="PARA LOS DECIMALES UTILIZA ','", title="ERROR",parent=ventana_registrar_ingresos)
        if entrada_importe_categoria.get()=='0': 
            messagebox.showwarning(message="HAS DEJADO CAMPOS SIN VALOR O CON VALORES NO RECONOCIDOS", title="AVISO",parent=ventana_registrar_ingresos)

        if correcto==True and float(entrada_importe_categoria.get())>0 and fecha_correcta==True:
            if len(comentarios_categoria.get())<450:
                comentarios_categoria.config(highlightbackground='grey',highlightcolor='white')   
                aplicar_registrar_ingresos()
            else:
                if len(comentarios_categoria.get())>450:
                    comentarios_categoria.config(highlightbackground='red',highlightcolor='red') 
                else:
                    comentarios_categoria.config(highlightbackground='grey',highlightcolor='white')
                messagebox.showwarning(message="COMENTARIO DEMASIADO EXTENSO", title="ERROR",parent=ventana_registrar_ingresos)     
        
    def aplicar_registrar_ingresos():
        global acumular_precio
        try:
            if messagebox.askokcancel("APLICAR Y SALIR", "¿Desea aplicar los cambios y salir del registro de ingresos?",parent = ventana_registrar_ingresos):
                categoria=desplegable_categoria.get()
                comentarios=comentarios_categoria.get()
                comentarios=str(comentarios)
                fecha=fecha_categoria.get()#Aquí a la fecha hay que darle la vuelta, porque ahora mismo está en formato dia/mes/año
                dia=fecha[0:-8]
                mes=fecha[3:-5]
                aNo=fecha[6:]
                fecha=aNo+'-'+mes+'-'+dia
                importe=entrada_importe_categoria.get()
                importe=float(importe)
                
                
                if categoria=='VALORES FIJOS':
                    consulta = "insert into inminente (categoria,fecha,importe) values (%s,%s,%s);"
                    datos = [('MTO ELECTRICO',fecha,acumular_precio),('OCIO A',fecha,ocio_a),('OCIO B',fecha,ocio_b),('HOGAR',fecha,hogar),('SEGURO VEHICULO',fecha,seguro_vehiculo),('LAVADO VEHICULO',fecha,lavado_vehiculo),('NEUMATICOS',fecha,neumaticos),('AMORTIZACION VEHICULO',fecha,amortizacion_vehiculo),('MTO VEHICULO',fecha,mto_vehiculo)]
                    cursor.executemany(consulta,datos)
                    connection.commit()
                else:
                    if importe > 0:
                        if categoria=='MTO ELECTRICO':
                            categoria=desplegable.get()
                        consulta = "insert into inminente (categoria,fecha,importe) values (%s,%s,%s);"
                        datos = (categoria,fecha,importe)
                        cursor.execute(consulta,datos)
                        connection.commit()
                        consulta_clave="select max(cod_inminente)from inminente"
                        cursor.execute(consulta_clave)
                        codigo=cursor.fetchone()
                        codigo=str(codigo)
                        codigo=codigo[1:-2]
                        codigo=int(codigo)
                        connection.commit()
                        if len(comentarios)<450 and len(comentarios)>1:
                            
                            consulta = "insert into informacion (categoria,codigo,fecha,comentarios) values(%s,%s,%s,%s);"
                            datos = (categoria,codigo,fecha,comentarios)
                            cursor.execute(consulta,datos)
                            connection.commit()

                
               
                
        except:
            pass
        

   

                
    #CUERPO: CATEGORIA-IMPORTE-FECHA-COMENTARIOS DE LA VENTANA "REGISTRAR INGRESOS"
    def llamar(event):
        
        
        if desplegable_categoria.get()=='VALORES FIJOS':
            entrada_importe_categoria.delete(0,END)
            entrada_importe_categoria.insert(0,acumular_precio+suma_valores_fijos)
            comentarios_categoria.delete(0,END)
            comentarios_categoria.config(state=DISABLED)
        else:
            entrada_importe_categoria.delete(0,END)
            comentarios_categoria.delete(0,END)
            comentarios_categoria.config(state=NORMAL)
        if desplegable_categoria.get()=='MTO ELECTRICO':
            
            desplegable.grid(row=2,column=0,padx=60)
        if desplegable_categoria.get()!='MTO ELECTRICO':
           desplegable.grid_remove()
              
            
   
    desplegable=Combobox(ventana_registrar_ingresos,values=electrodomesticos,state='readonly')
    desplegable.current(0)
    desplegable_categoria=Combobox(ventana_registrar_ingresos,values=categorias_ingreso,state='readonly')
    desplegable_categoria.grid(row=1,column=0,padx=60)
    desplegable_categoria.current(0)
    desplegable_categoria.bind("<<ComboboxSelected>>", llamar)
    entrada_importe_categoria= Entry(ventana_registrar_ingresos,width=15)
    entrada_importe_categoria.grid(row=1,column=1)
    fecha_actual = datetime.now()
    dia_mes_año = fecha_actual.strftime('%d-%m-%G')
    fecha_categoria= Entry(ventana_registrar_ingresos,width=15)
    fecha_categoria.insert(0,dia_mes_año)
    fecha_categoria.grid(row=1,column=2)
    comentarios_categoria= Entry(ventana_registrar_ingresos,width=65)
    comentarios_categoria.grid(row=1,column=3,padx=5)
  

   
    

    boton_aplicar=Button(ventana_registrar_ingresos,text='APLICAR',command=comprobar_datos_ingresos)
    boton_aplicar.grid(row=3,column=2)

    ventana_registrar_ingresos.mainloop()

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def registrar_gastos():
    ventana_registrar_gastos = Toplevel()
    ventana_registrar_gastos.geometry('1400x700')
    ventana_registrar_gastos.title('REGISTRO GASTOS')
    ventana_registrar_gastos.configure(bg='#FFE4E1')

    #CABECERA: CATEGORIA-IMPORTE-FECHA-COMENTARIOS DE LA VENTANA "REGISTRAR GASTOS"
    categoria=Label(ventana_registrar_gastos,text='CATEGORIA')
    categoria.configure(font=('Ubuntu Light',25),bg='#FFE4E1')
    categoria.grid(row=0,column=0,padx=5,pady=5)
    importe=Label(ventana_registrar_gastos,text='IMPORTE')
    importe.configure(font=('Ubuntu Light',25),bg='#FFE4E1')
    importe.grid(row=0,column=1,padx=5,pady=5)
    fecha=Label(ventana_registrar_gastos,text='FECHA')
    fecha.configure(font=('Ubuntu Light',25),bg='#FFE4E1')
    fecha.grid(row=0,column=2,padx=5,pady=5)
    comentarios=Label(ventana_registrar_gastos,text='COMENTARIOS')
    comentarios.configure(font=('Ubuntu Light',25),bg='#FFE4E1')
    comentarios.grid(row=0,column=3,padx=5,pady=5)
    #VALIDAR IMPORTE Y FECHA
    def comprobar_datos_gastos():
        #IMPORTE
        correcto=False
        usa_comas=False
        fecha_correcta=True
        try:
            try:
                datetime.strptime(fecha_categoria.get(),'%d-%m-%Y')
                fecha_categoria.config(highlightbackground = "grey", highlightcolor= "white")
            except:
                fecha_categoria.config(highlightbackground = "red", highlightcolor= "red")
                fecha_correcta=False
        except:
            pass    
        if fecha_correcta==False:
            messagebox.showwarning(message="FECHA NO VÁLIDA", title="ERROR",parent=ventana_registrar_gastos)
            
        if entrada_importe_categoria.get().isdigit() or entrada_importe_categoria.get().replace('.','').isdigit() and entrada_importe_categoria.get().count(".")==1:
            correcto=True
            entrada_importe_categoria.config(highlightbackground='grey',highlightcolor='white')
        elif entrada_importe_categoria.get().replace(',','').isdigit():
            usa_comas=True
            entrada_importe_categoria.config(highlightbackground='red',highlightcolor='red')

        else:
            entrada_importe_categoria.delete(0,END)
            entrada_importe_categoria.insert(0,0)
            correcto=True

        if usa_comas==True:
            messagebox.showwarning(message="PARA LOS DECIMALES UTILIZA ','", title="ERROR",parent=ventana_registrar_gastos)
        if entrada_importe_categoria.get()=='0': 
            messagebox.showwarning(message="HAS DEJADO CAMPOS SIN VALOR O CON VALORES NO RECONOCIDOS", title="AVISO",parent=ventana_registrar_gastos)

        if correcto==True and float(entrada_importe_categoria.get())>0 and fecha_correcta==True:
            if len(comentarios_categoria.get())<450:
                comentarios_categoria.config(highlightbackground='grey',highlightcolor='white')   
                aplicar_registrar_gastos()
            else:
                if len(comentarios_categoria.get())>450:
                    comentarios_categoria.config(highlightbackground='red',highlightcolor='red') 
                else:
                    comentarios_categoria.config(highlightbackground='grey',highlightcolor='white')
                messagebox.showwarning(message="COMENTARIO DEMASIADO EXTENSO", title="ERROR",parent=ventana_registrar_gastos)     
        
    def aplicar_registrar_gastos():
        try:
            if messagebox.askokcancel("APLICAR Y SALIR", "¿Desea aplicar los cambios y salir del registro de ingresos?",parent = ventana_registrar_gastos):
                categoria=desplegable_categoria.get()
                comentarios=comentarios_categoria.get()
                comentarios=str(comentarios)
                fecha=fecha_categoria.get()#Aquí a la fecha hay que darle la vuelta, porque ahora mismo está en formato dia/mes/año
                dia=fecha[0:-8]
                mes=fecha[3:-5]
                aNo=fecha[6:]
                fecha=aNo+'-'+mes+'-'+dia
                importe=entrada_importe_categoria.get()
                importe=float(importe)
                
                
               
                if importe > 0:
                    if categoria=='MTO ELECTRICO':
                        categoria=desplegable.get()
                    importe=importe*-1
                    consulta = "insert into inminente (categoria,fecha,importe) values (%s,%s,%s);"
                    datos = (categoria,fecha,importe)
                    cursor.execute(consulta,datos)
                    connection.commit()
                    consulta_clave="select max(cod_inminente)from inminente"
                    cursor.execute(consulta_clave)
                    codigo=cursor.fetchone()
                    connection.commit()
                    codigo=str(codigo)
                    codigo=codigo[1:-2]
                    codigo=int(codigo)
                    if len(comentarios)<450 and len(comentarios)>1:
                        consulta = "insert into informacion (codigo,categoria,fecha,comentarios) values(%s,%s,%s,%s);"
                        datos = (codigo,categoria,fecha,comentarios)
                        cursor.execute(consulta,datos)
                        connection.commit()

            
               
                
        except:
            pass
        
        #connection.close()
   

                
    #CUERPO: CATEGORIA-IMPORTE-FECHA-COMENTARIOS DE LA VENTANA "REGISTRAR GASTOS"

    def llamar(event):
        if desplegable_categoria.get()=='MTO ELECTRICO':
            
            desplegable.grid(row=2,column=0,padx=60)
        if desplegable_categoria.get()!='MTO ELECTRICO':
           desplegable.grid_remove()

    desplegable=Combobox(ventana_registrar_gastos,values=electrodomesticos,state='readonly')
    desplegable.current(0)
    desplegable_categoria=Combobox(ventana_registrar_gastos,values=categorias,state='readonly')
    desplegable_categoria.grid(row=1,column=0,padx=60)
    desplegable_categoria.current(0)
    desplegable_categoria.bind("<<ComboboxSelected>>", llamar)
    entrada_importe_categoria= Entry(ventana_registrar_gastos,width=15)
    entrada_importe_categoria.grid(row=1,column=1)
    fecha_actual = datetime.now()
    dia_mes_año = fecha_actual.strftime('%d-%m-%G')
    fecha_categoria= Entry(ventana_registrar_gastos,width=15)
    fecha_categoria.insert(0,dia_mes_año)
    fecha_categoria.grid(row=1,column=2)
    comentarios_categoria= Entry(ventana_registrar_gastos,width=65)
    comentarios_categoria.grid(row=1,column=3,padx=5)

   
    

    boton_aplicar=Button(ventana_registrar_gastos,text='APLICAR',command=comprobar_datos_gastos)
    boton_aplicar.grid(row=3,column=2)

    ventana_registrar_gastos.mainloop()    

def reparto():
    ventana_reparto= Toplevel()
    ventana_reparto.geometry('1400x700')
    ventana_reparto.title('REPARTO GASTOS ESPINOSA 25')
    meses=('ENERO','FEBRERO','MARZO','ABRIL','MAYO','JUNIO','JULIO','AGOSTO','SEPTIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE')
    aNos=[]
    now=datetime.now()
    aNo_actual=now.year
    aNo_actual=aNo_actual+1
    for n in range(2020,aNo_actual):
        aNos.append(n)
    def reparto_gastos():
        mes=desplegable_meses.get()
        aNo=desplegable_aNos.get()
        posicion_mes=meses.index(mes)+1
    #CONSULTAS BASE DE DATOS:
        importe_consulta=("select (select COALESCE(sum(importe),0) from inminente where categoria in ('OCIO A','OCIO B','HOGAR','SEGURO VEHICULO','LAVADO VEHICULO','NEUMATICOS','AMORTIZACION VEHICULO','MTO VEHICULO','MTO ELECTRICO')and importe>0 and month(fecha)=%s and year(fecha)=%s);")
        datos_importe=(posicion_mes,aNo)
        cursor.execute(importe_consulta,datos_importe)
        respuesta = cursor.fetchone()
        coste_total=str(respuesta)
        coste_total=coste_total[1:-2]
        coste_total=float(coste_total)
        coste_total=round(coste_total,2)
        
     

        importe_nacho_consulta=("select COALESCE(sum(importe),0)*-1 from inminente where categoria in('CONTRIBUCION','SEGURO HOGAR','LUZ','AGUA','GAS','INTERNET','SELLO VEHICULO','VADO')and importe<0 and month(fecha)=%s and year(fecha)=%s;")
        datos_importe_nacho=(posicion_mes,aNo,)
        cursor.execute(importe_nacho_consulta,datos_importe_nacho)
        respuesta_nacho = cursor.fetchone()
        coste_total_nacho=str(respuesta_nacho)
        coste_total_nacho=coste_total_nacho[1:-2]
        coste_total_nacho=float(coste_total_nacho)
        coste_total_nacho=round(coste_total_nacho,2)

        consulta_ahorro=("select COALESCE(sum(importe),0) from inminente where categoria='AHORRO'and importe>0 and year(fecha)=%s and month(fecha)=%s;")
        ahorro_datos=(aNo,posicion_mes)
        cursor.execute(consulta_ahorro,ahorro_datos)
        respuesta_ahorro = cursor.fetchone()
        ahorro=str(respuesta_ahorro)
        ahorro=ahorro[1:-2]
        ahorro=float(ahorro)
        ahorro=round(ahorro,2)
        ahorro_dividido=ahorro/2 

        comida=500
        comida_dividida=comida/2
        ocio_introducido=cantidad_ocio.get()
        try:
            ocio_introducido=float(ocio_introducido)
            ocio_dividido=ocio_introducido/2
        except:
            cantidad_ocio.delete('0',END)
            cantidad_ocio.insert('0',0)
            ocio_dividido=0
      
        print("*****NACHO Y LAURA*****")
        print("VALORES FIJOS = ",coste_total)
        print("GASTOS CARGADOS EN CUENTA NACHO = ",coste_total_nacho)
        print("AHORRO = ",ahorro)
        print("OCIO A INGRESAR DIVIDIDO = ",ocio_dividido)
        totalAdividir = coste_total+coste_total_nacho+ahorro
        totalAdividir = round(totalAdividir,2) 
        totalAdividirDividido =totalAdividir/2
        totalAdividirDividido = round(totalAdividirDividido,2)
        print("VALORES FIJOS + GASTOS CARGADOS EN CUENTA NACHO + AHORRO = ",totalAdividir)
        print("TOTAL GASTOS DIVIDIDO = ",totalAdividirDividido)
        nacho_banco=totalAdividirDividido-coste_total_nacho-ocio_dividido
        nacho_banco = round(nacho_banco,2)
        print("NACHO INGRESA EN BANCO = ",nacho_banco)
        laura_banco=totalAdividirDividido-ocio_dividido
        laura_banco = round(laura_banco,2)
        print("LAURA INGRESA A BANCO = ",laura_banco)
        

        nacho_casa=comida_dividida-ahorro_dividido+ocio_dividido
        nacho_casa=round(nacho_casa,2)
        laura_casa=comida_dividida-ahorro_dividido+ocio_dividido
        laura_casa=round(laura_casa,2)
        
    
        strnacho_banco=str(nacho_banco)
        strnacho_banco='NACHO A BANCO: '+strnacho_banco + '€'
        strnacho_casa=str(nacho_casa)
        strnacho_casa='NACHO A CASA: '+strnacho_casa + '€'

        strlaura_banco=str(laura_banco)
        strlaura_banco='LAURA A BANCO: '+strlaura_banco + '€'
        strlaura_casa=str(laura_casa)
        strlaura_casa='LAURA A CASA: '+strlaura_casa + '€'

        cantidad_reparto.delete('1.0',END)
        cantidad_reparto.insert('1.0',strnacho_banco +'\n'+strnacho_casa+'\n'+strlaura_banco +'\n'+strlaura_casa)
        cantidad_reparto.config(font=('italic',10),foreground='black')
        def telegram():
            recibo=''
            consulta_recibos=("select categoria,COALESCE(importe,0) from inminente where categoria in('CONTRIBUCION','SEGURO HOGAR','LUZ','AGUA','GAS','INTERNET','VADO','SELLO VEHICULO')and importe<0 and month(fecha)=%s and year(fecha)=%s;")
            recibos_datos=(posicion_mes,aNo)
            cursor.execute(consulta_recibos,recibos_datos)
            respuesta_recibos = cursor.fetchall()
            for n in respuesta_recibos:
                categoria=n[0]
                strcategoria=str(categoria)
                importe=n[1]
                importe=float(importe)
                importe=importe*-1
                strimporte=str(importe)
                recibo+=strcategoria+'='+strimporte+'€'+'\n'
                
            
            def mensaje(texto):
                try:
                    r=requests.post('https://*****',
                    data={'chat_id':'-*****','text':texto})
                    data=json.loads(r.text)
                except:
                    cantidad_reparto.delete('1.0',END)
                    cantidad_reparto.insert('1.0','NO SE HA ENVIADO EL MENSAJE')
                    cantidad_reparto.config(font=('italic',10),foreground='black')
            mes=meses[posicion_mes-1]
            texto='HOLA CHIC@S, AQUI TENÉIS LOS COSTES CON FECHA: '+mes+' '+aNo+'\n'+recibo+strnacho_banco+'\n'+strnacho_casa+'\n'+strlaura_banco+'\n'+strlaura_casa
            mensaje(texto)

        envio_telegram=Button(ventana_reparto,text='ENVIAR POR TELEGRAM',command=telegram)
        envio_telegram.grid(row=8,column=0,pady=10,padx=60)
    
    etiqueta_mes=Label(ventana_reparto,text='ELIGE UN MES')
    etiqueta_mes.grid(row=0,column=0)
    desplegable_meses=Combobox(ventana_reparto,values=meses,width=15,state='readonly')
    desplegable_meses.grid(row=1,column=0,pady=10,padx=60)   
    desplegable_meses.current(0)

    etiqueta_aNo=Label(ventana_reparto,text='ELIGE UN AÑO')
    etiqueta_aNo.grid(row=2,column=0)
    desplegable_aNos=Combobox(ventana_reparto,values=aNos,width=10,state='readonly')
    desplegable_aNos.grid(row=3,column=0,pady=10,padx=60)   
    desplegable_aNos.current(0)

    etiqueta_ocio=Label(ventana_reparto,text='OCIO PARA CASA')
    etiqueta_ocio.grid(row=4,column=0)
    cantidad_ocio= Entry(ventana_reparto,width=15)
    cantidad_ocio.grid(row=5,column=0)


    boton_aplicar=Button(ventana_reparto,text='REPARTIR',command=reparto_gastos)
    boton_aplicar.grid(row=6,column=0,pady=10,padx=60)

    cantidad_reparto= Text(ventana_reparto,width=35,height=4)
    cantidad_reparto.grid(row=7,column=0,padx=10)

    





    ventana_reparto.mainloop()




#PAGINA INICIO
coste=coste_mto_electrico()
global total
#coste=coste_mto_electrico() es para conocer el total acumulado el electrodomésticos.
#'acumular_precio' contiene el coste mensual del mto electrico, en linea 821 sumamos 'suma_valores_fijos'+acumular_precio
try:
    total=0
    #En la consulta no metemos mto electrico porque lo vamos a sumar después (coste) ya que así tenemos restados los posibles gastos por mto en los electrodomesticos    
    listado_importes=[]
    suma=0
    negativo=0
    consulta=("select sum(importe) from inminente where categoria in ('OCIO A','OCIO B','AHORRO','HOGAR','SEGURO VEHICULO','LAVADO VEHICULO','NEUMATICOS','AMORTIZACION VEHICULO','MTO VEHICULO')")
    cursor.execute(consulta)
    total=cursor.fetchone()
    total=str(total)
    total=total[1:-2]
    total=float(total)
    total=total+coste
    total=round(total,2)
    total=str(total)
    total='SALDO ACTUAL: '+total+'€'
    print (total)
    acumulado=Label(root,text=total)
    acumulado.grid(row=0,column=0,pady=10)

except:
    strcoste=str(coste)
    strcoste=strcoste+'€'
    acumulado=Label(root,text=strcoste)
    acumulado.grid(row=0,column=0,pady=10)
my_tree=Treeview(root)
#definimos columnas
my_tree['columns']=('FECHA','CATEGORIA','IMPORTE','COMENTARIOS')
#Formateamos columnas
my_tree.column('#0',width=0,minwidth=0,stretch=NO)#Según codemy es una columna fantasma y tiene que estar...
my_tree.column('FECHA',anchor=W,width=80)
my_tree.column('CATEGORIA',anchor=W,width=200)
my_tree.column('IMPORTE',anchor=W,width=80)
my_tree.column('COMENTARIOS',anchor=W,width=600)
#Crear encabezado
my_tree.heading('#0',text='Label1',anchor=W)
my_tree.heading('FECHA',text='FECHA',anchor=W)
my_tree.heading('CATEGORIA',text='CATEGORIA',anchor=CENTER)
my_tree.heading('IMPORTE',text='IMPORTE',anchor=W)
my_tree.heading('COMENTARIOS',text='COMENTARIOS',anchor=W)
my_tree.grid(row=1,column=0,padx=30)
contador=0
def mov_todos():
    sumatoria.delete('1.0',END) 
    global contador
    if contador>0:
        for n in range(contador):
            my_tree.delete(n+1)
    contador=0


    #anadir datos

    consulta=("select fecha,categoria,importe,cod_inminente from inminente order by fecha desc")
    cursor.execute(consulta)
    respuesta=cursor.fetchall()

    consulta_codigo_comentarios=('select codigo from informacion')
    cursor.execute(consulta_codigo_comentarios)
    respuesta_codigo_comentarios=cursor.fetchall()
    lista=[]
    for n in range (len(respuesta_codigo_comentarios)):
        codigo=respuesta_codigo_comentarios[n]
        codigo=str(codigo)
        codigo=codigo[1:-2]
        codigo=int(codigo)
        lista.append(codigo)
        
    for n in range(len(respuesta)):
        fecha=respuesta[n][0]
        fecha=str(fecha)
        fecha=fecha[8::]+'/'+fecha[5:-3]+'/'+fecha[0:-6]
        categoria=respuesta[n][1]
        importe=respuesta[n][2]
        importe=str(importe)
        importe=' '+importe+'€'
        codigo=respuesta[n][3]
        contador+=1
        if codigo in lista:
            consulta_comentarios=('select comentarios from informacion where codigo=%s')
            valores=codigo
            cursor.execute(consulta_comentarios,valores)
            respuesta_comentarios=cursor.fetchone()
            texto=respuesta_comentarios
            texto=str(texto)
            texto=texto[2:-3]
            my_tree.insert(parent='',index='end',iid=contador,text='Parent',values=(fecha,categoria,importe,texto))
        else:
            my_tree.insert(parent='',index='end',iid=contador,text='Parent',values=(fecha,categoria,importe))
        
def mov_ingresos():
    sumatoria.delete('1.0',END) 
    global contador
    for n in range(contador):
        my_tree.delete(n+1)

    consulta=("select fecha,categoria,importe,cod_inminente from inminente where importe >0 order by fecha desc;")
    cursor.execute(consulta)
    respuesta = cursor.fetchall()
    contador=0

    consulta_codigo_comentarios=('select codigo from informacion')
    cursor.execute(consulta_codigo_comentarios)
    respuesta_codigo_comentarios=cursor.fetchall()
    lista=[]
    for n in range (len(respuesta_codigo_comentarios)):
        codigo=respuesta_codigo_comentarios[n]
        codigo=str(codigo)
        codigo=codigo[1:-2]
        codigo=int(codigo)
        lista.append(codigo)
        
    for n in range(len(respuesta)):
        fecha=respuesta[n][0]
        fecha=str(fecha)
        fecha=fecha[8::]+'/'+fecha[5:-3]+'/'+fecha[0:-6]
        categoria=respuesta[n][1]
        importe=respuesta[n][2]
        importe=str(importe)
        importe=' '+importe+'€'
        codigo=respuesta[n][3]
        contador+=1
        if codigo in lista:
            consulta_comentarios=('select comentarios from informacion where codigo=%s')
            valores=codigo
            cursor.execute(consulta_comentarios,valores)
            respuesta_comentarios=cursor.fetchone()
            texto=respuesta_comentarios
            texto=str(texto)
            texto=texto[2:-3]
            my_tree.insert(parent='',index='end',iid=contador,text='Parent',values=(fecha,categoria,importe,texto))
        else:
            my_tree.insert(parent='',index='end',iid=contador,text='Parent',values=(fecha,categoria,importe))

def mov_gastos():
    sumatoria.delete('1.0',END) 
    global contador
    for n in range(contador):
        my_tree.delete(n+1)

    consulta=("select fecha,categoria,importe,cod_inminente from inminente where importe <0 order by fecha desc;")
    cursor.execute(consulta)
    respuesta = cursor.fetchall() 

    contador=0

    consulta_codigo_comentarios=('select codigo from informacion')
    cursor.execute(consulta_codigo_comentarios)
    respuesta_codigo_comentarios=cursor.fetchall()
    lista=[]
    for n in range (len(respuesta_codigo_comentarios)):
        codigo=respuesta_codigo_comentarios[n]
        codigo=str(codigo)
        codigo=codigo[1:-2]
        codigo=int(codigo)
        lista.append(codigo)
        
    for n in range(len(respuesta)):
        fecha=respuesta[n][0]
        fecha=str(fecha)
        fecha=fecha[8::]+'/'+fecha[5:-3]+'/'+fecha[0:-6]
        categoria=respuesta[n][1]
        importe=respuesta[n][2]
        importe=str(importe)
        importe=' '+importe+'€'
        codigo=respuesta[n][3]
        contador+=1
        if codigo in lista:
            consulta_comentarios=('select comentarios from informacion where codigo=%s')
            valores=codigo
            cursor.execute(consulta_comentarios,valores)
            respuesta_comentarios=cursor.fetchone()
            texto=respuesta_comentarios
            texto=str(texto)
            texto=texto[2:-3]
            my_tree.insert(parent='',index='end',iid=contador,text='Parent',values=(fecha,categoria,importe,texto))
        else:
            my_tree.insert(parent='',index='end',iid=contador,text='Parent',values=(fecha,categoria,importe))
def buscar_mov():
    categoria=cuadro_busqueda.get()
    mes=desplegable_meses.get()
    posicion_mes=meses.index(mes)
    aNo=desplegable_aNos.get()
    #CONSTRUIMOS LA CONSULTA FILTRANDO LOS RESULTADOS DE LOS COMBOBOX:
    if desplegable_buscar.get()=='BUSCAR TODOS LOS RESULTADOS':
        listado_importe=[]
        suma=0
        if posicion_mes==0:#año completo
            if desplegable_aNos.get()=='TODOS LOS AÑOS REGISTRADOS':
                texto_consulta=("select fecha,categoria,importe,cod_inminente from inminente where categoria=%s order by fecha desc;")
                datos_recop=(categoria)

                importe_consulta=("select sum(importe) from inminente where categoria=%s;")
                datos_importe=(categoria)

                if categoria=='TODAS':
                    texto_consulta=("select fecha,categoria,importe,cod_inminente from inminente order by fecha desc;")
                    importe_consulta=("select (select COALESCE(sum(importe),0) from inminente where categoria in ('OCIO A','OCIO B','HOGAR','SEGURO VEHICULO','LAVADO VEHICULO','NEUMATICOS','AMORTIZACION VEHICULO','MTO VEHICULO','MTO ELECTRICO')and importe>0)+(select COALESCE(sum(importe),0)*-1 from inminente where categoria!='OCIO A'and categoria!='OCIO B'and categoria!='AHORRO'and categoria!='HOGAR'and categoria!='SEGURO VEHICULO'and categoria!='LAVADO VEHICULO'and categoria!='NEUMATICOS'and categoria!='AMORTIZACION VEHICULO'and categoria!='MTO VEHICULO'and categoria!='MTO ELECTRICO'and importe<0);")
                    consulta=texto_consulta
                    cursor.execute(consulta)
                    respuesta = cursor.fetchall() 
                    consulta_importe=importe_consulta
                    cursor.execute(consulta_importe)
                    respuesta_importe = cursor.fetchone()
            else:
                aNo=int(aNo)
                texto_consulta=("select fecha,categoria,importe,cod_inminente from inminente where categoria=%s and year(fecha)=%s order by fecha desc;")
                datos_recop=(categoria,aNo)

                importe_consulta=("select sum(importe) from inminente where categoria=%s and year(fecha)=%s;")
                datos_importe=(categoria,aNo)

                if categoria=='TODAS':
                    texto_consulta=("select fecha,categoria,importe,cod_inminente from inminente where year(fecha)=%s order by fecha desc;")
                    datos_recop=(aNo)
                    importe_consulta=("select (select COALESCE(sum(importe),0) from inminente where categoria in ('OCIO A','OCIO B','HOGAR','SEGURO VEHICULO','LAVADO VEHICULO','NEUMATICOS','AMORTIZACION VEHICULO','MTO VEHICULO','MTO ELECTRICO')and importe>0 and year(fecha)=%s)+(select COALESCE(sum(importe),0)*-1 from inminente where categoria!='OCIO A'and categoria!='OCIO B'and categoria!='AHORRO'and categoria!='HOGAR'and categoria!='SEGURO VEHICULO'and categoria!='LAVADO VEHICULO'and categoria!='NEUMATICOS'and categoria!='AMORTIZACION VEHICULO'and categoria!='MTO VEHICULO'and categoria!='MTO ELECTRICO'and importe<0 and year(fecha)=%s);")
                    datos_importe=(aNo,aNo)
                    consulta=texto_consulta
                    datos=(datos_recop)
                    cursor.execute(consulta,datos)
                    respuesta = cursor.fetchall() 
                    consulta_importe=importe_consulta
                    datos_consulta=(datos_importe)
                    cursor.execute(consulta_importe,datos_consulta)
                    respuesta_importe = cursor.fetchone()
                
        else:#mes en concreto
            posicion_mes=meses.index(mes)
            mes=posicion_mes
            if desplegable_aNos.get()=='TODOS LOS AÑOS REGISTRADOS':
                texto_consulta=("select fecha,categoria,importe,cod_inminente from inminente where categoria=%s and month(fecha)=%s order by fecha desc;")
                datos_recop=(categoria,mes)

                importe_consulta=("select sum(importe) from inminente where categoria=%s and month(fecha)=%s;")
                datos_importe=(categoria,mes)

                if categoria=='TODAS':
                    texto_consulta=("select fecha,categoria,importe,cod_inminente from inminente where month(fecha)=%s order by fecha desc;")
                    datos_recop=(mes)
                    importe_consulta=("select (select COALESCE(sum(importe),0) from inminente where categoria in ('OCIO A','OCIO B','HOGAR','SEGURO VEHICULO','LAVADO VEHICULO','NEUMATICOS','AMORTIZACION VEHICULO','MTO VEHICULO','MTO ELECTRICO')and importe>0 and month(fecha)=%s)+(select COALESCE(sum(importe),0)*-1 from inminente where categoria!='OCIO A'and categoria!='OCIO B'and categoria!='AHORRO'and categoria!='HOGAR'and categoria!='SEGURO VEHICULO'and categoria!='LAVADO VEHICULO'and categoria!='NEUMATICOS'and categoria!='AMORTIZACION VEHICULO'and categoria!='MTO VEHICULO'and categoria!='MTO ELECTRICO'and importe<0 and month(fecha)=%s);")
                    datos_importe=(mes,mes)

                    consulta=texto_consulta
                    datos=(datos_recop)
                    cursor.execute(consulta,datos)
                    respuesta = cursor.fetchall() 
                    consulta_importe=importe_consulta
                    datos_consulta=(datos_importe)
                    cursor.execute(consulta_importe,datos_consulta)
                    respuesta_importe = cursor.fetchone() 

            else:
                aNo=int(aNo)
                texto_consulta=("select fecha,categoria,importe,cod_inminente from inminente where categoria=%s and month(fecha)=%s and year(fecha)=%s order by fecha desc;")
                datos_recop=(categoria,mes,aNo)

                importe_consulta=("select sum(importe) from inminente where categoria=%s and month(fecha)=%s and year(fecha)=%s;")
                datos_importe=(categoria,mes,aNo)

                if categoria=='TODAS':
                    texto_consulta=("select fecha,categoria,importe,cod_inminente from inminente where month(fecha)=%s and year(fecha)=%s order by fecha desc;")
                    datos_recop=(mes,aNo)
                    importe_consulta=("select (select COALESCE(sum(importe),0) from inminente where categoria in ('OCIO A','OCIO B','HOGAR','SEGURO VEHICULO','LAVADO VEHICULO','NEUMATICOS','AMORTIZACION VEHICULO','MTO VEHICULO','MTO ELECTRICO')and importe>0 and month(fecha)=%s and year(fecha)=%s)+(select COALESCE(sum(importe),0)*-1 from inminente where categoria!='OCIO A'and categoria!='OCIO B'and categoria!='AHORRO'and categoria!='HOGAR'and categoria!='SEGURO VEHICULO'and categoria!='LAVADO VEHICULO'and categoria!='NEUMATICOS'and categoria!='AMORTIZACION VEHICULO'and categoria!='MTO VEHICULO'and categoria!='MTO ELECTRICO'and importe<0 and month(fecha)=%s and year(fecha)=%s);")
                    datos_importe=(mes,aNo,mes,aNo)

                    consulta=texto_consulta
                    datos=(datos_recop)
                    cursor.execute(consulta,datos)
                    respuesta = cursor.fetchall() 
                    consulta_importe=importe_consulta
                    datos_consulta=(datos_importe)
                    cursor.execute(consulta_importe,datos_consulta)
                    respuesta_importe = cursor.fetchone()
                

    if desplegable_buscar.get()=='BUSCAR TODOS LOS GASTOS':
        if posicion_mes==0:#año completo
            if desplegable_aNos.get()=='TODOS LOS AÑOS REGISTRADOS':
                texto_consulta=("select fecha,categoria,importe,cod_inminente from inminente where categoria=%s and importe<0 order by fecha desc;")
                datos_recop=(categoria)
              
                importe_consulta=("select sum(importe) from inminente where categoria=%s and importe<0;")
                datos_importe=(categoria)

                if categoria=='TODAS':
                    texto_consulta=("select fecha,categoria,importe,cod_inminente from inminente where importe<0 order by fecha desc;")
                    importe_consulta=("select sum(importe) from inminente where importe<0;")
                    consulta=texto_consulta
                    cursor.execute(consulta)
                    respuesta = cursor.fetchall() 
                    consulta_importe=importe_consulta
                    cursor.execute(consulta_importe)
                    respuesta_importe = cursor.fetchone() 
    
            else:
                aNo=int(aNo)
                texto_consulta=("select fecha,categoria,importe,cod_inminente from inminente where categoria=%s and year(fecha)=%s and importe<0 order by fecha desc;")
                datos_recop=(categoria,aNo)

                importe_consulta=("select sum(importe) from inminente where categoria=%s and year(fecha)=%s and importe<0;")
                datos_importe=(categoria,aNo)

                if categoria=='TODAS':
                    texto_consulta=("select fecha,categoria,importe,cod_inminente from inminente where year(fecha)=%s and importe<0 order by fecha desc;")
                    datos_recop=(aNo)
                    importe_consulta=("select sum(importe) from inminente where year(fecha)=%s and importe<0;")
                    datos_importe=(aNo)

                    consulta=texto_consulta
                    datos=(datos_recop)
                    cursor.execute(consulta,datos)
                    respuesta = cursor.fetchall() 
                    consulta_importe=importe_consulta
                    datos_consulta=(datos_importe)
                    cursor.execute(consulta_importe,datos_consulta)
                    respuesta_importe = cursor.fetchone() 

        else:#mes en concreto
            posicion_mes=meses.index(mes)
            mes=posicion_mes
            if desplegable_aNos.get()=='TODOS LOS AÑOS REGISTRADOS':
                texto_consulta=("select fecha,categoria,importe,cod_inminente from inminente where categoria=%s and month(fecha)=%s and importe<0 order by fecha desc;")
                datos_recop=(categoria,mes)

                importe_consulta=("select sum(importe) from inminente where categoria=%s and month(fecha)=%s and importe<0;")
                datos_importe=(categoria,mes)

                if categoria=='TODAS':
                    texto_consulta=("select fecha,categoria,importe,cod_inminente from inminente where month(fecha)=%s and importe<0 order by fecha desc;")
                    datos_recop=(mes)
                    importe_consulta=("select sum(importe) from inminente where month(fecha)=%s and importe<0;")
                    datos_importe=(mes)
                    consulta=texto_consulta
                    datos=(datos_recop)
                    cursor.execute(consulta,datos)
                    respuesta = cursor.fetchall() 
                    consulta_importe=importe_consulta
                    datos_consulta=(datos_importe)
                    cursor.execute(consulta_importe,datos_consulta)
                    respuesta_importe = cursor.fetchone() 

            else:
                aNo=int(aNo)
                texto_consulta=("select fecha,categoria,importe,cod_inminente from inminente where categoria=%s and month(fecha)=%s and year(fecha)=%s and importe<0 order by fecha desc;")
                datos_recop=(categoria,mes,aNo)
                importe_consulta=("select sum(importe) from inminente where categoria=%s and month(fecha)=%s and year(fecha)=%s and importe<0;")
                datos_importe=(categoria,mes,aNo)

                if categoria=='TODAS':
                    texto_consulta=("select fecha,categoria,importe,cod_inminente from inminente where month(fecha)=%s and year(fecha)=%s and importe<0 order by fecha desc;")
                    datos_recop=(mes,aNo)
                    importe_consulta=("select sum(importe) from inminente where month(fecha)=%s and year(fecha)=%s and importe<0;")
                    datos_importe=(mes,aNo)
                    consulta=texto_consulta
                    datos=(datos_recop)
                    cursor.execute(consulta,datos)
                    respuesta = cursor.fetchall() 
                    consulta_importe=importe_consulta
                    datos_consulta=(datos_importe)
                    cursor.execute(consulta_importe,datos_consulta)
                    respuesta_importe = cursor.fetchone() 

    if desplegable_buscar.get()=='BUSCAR TODOS LOS INGRESOS':
        if posicion_mes==0:#año completo
            if desplegable_aNos.get()=='TODOS LOS AÑOS REGISTRADOS':
                texto_consulta=("select fecha,categoria,importe,cod_inminente from inminente where categoria=%s and importe>0 order by fecha desc;")
                datos_recop=(categoria)
                importe_consulta=("select sum(importe) from inminente where categoria=%s and importe>0;")
                datos_importe=(categoria)

                if categoria=='TODAS':
                    texto_consulta=("select fecha,categoria,importe,cod_inminente from inminente where importe>0 order by fecha desc;")
                    importe_consulta=("select sum(importe) from inminente where importe>0;")
                    consulta=texto_consulta
                    cursor.execute(consulta)
                    respuesta = cursor.fetchall() 
                    consulta_importe=importe_consulta
                    cursor.execute(consulta_importe)
                    respuesta_importe = cursor.fetchone() 
                    
            else:
                aNo=int(aNo)
                texto_consulta=("select fecha,categoria,importe,cod_inminente from inminente where categoria=%s and year(fecha)=%s and importe>0 order by fecha desc;")
                datos_recop=(categoria,aNo)
                importe_consulta=("select sum(importe) from inminente where categoria=%s and year(fecha)=%s and importe>0;")
                datos_importe=(categoria,aNo)

                if categoria=='TODAS':
                    texto_consulta=("select fecha,categoria,importe,cod_inminente from inminente where year(fecha)=%s and importe>0 order by fecha desc;")
                    datos_recop=(aNo)
                    importe_consulta=("select sum(importe) from inminente where year(fecha)=%s and importe>0;")
                    datos_importe=(aNo)
                    consulta=texto_consulta
                    datos=(datos_recop)
                    cursor.execute(consulta,datos)
                    respuesta = cursor.fetchall() 
                    consulta_importe=importe_consulta
                    datos_consulta=(datos_importe)
                    cursor.execute(consulta_importe,datos_consulta)
                    respuesta_importe = cursor.fetchone() 


        else:#mes en concreto
            posicion_mes=meses.index(mes)
            mes=posicion_mes
            if desplegable_aNos.get()=='TODOS LOS AÑOS REGISTRADOS':
                texto_consulta=("select fecha,categoria,importe,cod_inminente from inminente where categoria=%s and month(fecha)=%s and importe>0 order by fecha desc;")
                datos_recop=(categoria,mes)
                importe_consulta=("select sum(importe) from inminente where categoria=%s and month(fecha)=%s and importe>0;")
                datos_importe=(categoria,mes)

                if categoria=='TODAS':
                    texto_consulta=("select fecha,categoria,importe,cod_inminente from inminente where month(fecha)=%s and importe>0 order by fecha desc;")
                    datos_recop=(mes)
                    importe_consulta=("select sum(importe) from inminente where month(fecha)=%s and importe>0;")
                    datos_importe=(mes)
                    consulta=texto_consulta
                    datos=(datos_recop)
                    cursor.execute(consulta,datos)
                    respuesta = cursor.fetchall() 
                    consulta_importe=importe_consulta
                    datos_consulta=(datos_importe)
                    cursor.execute(consulta_importe,datos_consulta)
                    respuesta_importe = cursor.fetchone() 


            else:
                aNo=int(aNo)
                texto_consulta=("select fecha,categoria,importe,cod_inminente from inminente where categoria=%s and month(fecha)=%s and year(fecha)=%s and importe>0 order by fecha desc;")
                datos_recop=(categoria,mes,aNo)

                importe_consulta=("select sum(importe) from inminente where categoria=%s and month(fecha)=%s and year(fecha)=%s and importe>0;")
                datos_importe=(categoria,mes,aNo)

                if categoria=='TODAS':
                    texto_consulta=("select fecha,categoria,importe,cod_inminente from inminente where month(fecha)=%s and year(fecha)=%s and importe>0 order by fecha desc;")
                    datos_recop=(mes,aNo)
                    importe_consulta=("select sum(importe) from inminente where month(fecha)=%s and year(fecha)=%s and importe>0;")
                    
                    datos_importe=(mes,aNo)
                    consulta=texto_consulta
                    datos=(datos_recop)
                    cursor.execute(consulta,datos)
                    respuesta = cursor.fetchall() 
                    consulta_importe=importe_consulta
                    datos_consulta=(datos_importe)
                    cursor.execute(consulta_importe,datos_consulta)
                    respuesta_importe = cursor.fetchone() 

     
    global contador
    for n in range(contador):
        my_tree.delete(n+1)
    sumatoria.delete('1.0',END) 
    if categoria!='TODAS':
        consulta=texto_consulta
        datos=(datos_recop)
        cursor.execute(consulta,datos)
        respuesta = cursor.fetchall() 
        consulta_importe=importe_consulta
        datos_consulta=(datos_importe)
        cursor.execute(consulta_importe,datos_consulta)
        respuesta_importe = cursor.fetchone() 


    if respuesta==():
        cuadro_busqueda.delete(0,END)
        cuadro_busqueda.insert(0,'NO HAY RESULTADOS')
    contador=0

    consulta_codigo_comentarios=('select codigo from informacion')
    cursor.execute(consulta_codigo_comentarios)
    respuesta_codigo_comentarios=cursor.fetchall()
    lista=[]
    for n in range (len(respuesta_codigo_comentarios)):
        codigo=respuesta_codigo_comentarios[n]
        codigo=str(codigo)
        codigo=codigo[1:-2]
        codigo=int(codigo)
        lista.append(codigo)
        
    for n in range(len(respuesta)):
        fecha=respuesta[n][0]
        fecha=str(fecha)
        fecha=fecha[8::]+'/'+fecha[5:-3]+'/'+fecha[0:-6]
        categoria=respuesta[n][1]
        importe=respuesta[n][2]
        importe=str(importe)
        importe=' '+importe+'€'
        codigo=respuesta[n][3]
        contador+=1
        if codigo in lista:
            consulta_comentarios=('select comentarios from informacion where codigo=%s')
            valores=codigo
            cursor.execute(consulta_comentarios,valores)
            respuesta_comentarios=cursor.fetchone()
            texto=respuesta_comentarios
            texto=str(texto)
            texto=texto[2:-3]
            my_tree.insert(parent='',index='end',iid=contador,text='Parent',values=(fecha,categoria,importe,texto))
        else:
            my_tree.insert(parent='',index='end',iid=contador,text='Parent',values=(fecha,categoria,importe))
    
    try:
        respuesta_importe=str(respuesta_importe)
        respuesta_importe=respuesta_importe[1:-2]
        respuesta_importe=float(respuesta_importe)
        respuesta_importe=round(respuesta_importe,2)
        respuesta_importe=str(respuesta_importe)
        respuesta_importe=respuesta_importe+'€' 
        sumatoria.delete('1.0',END)  
        sumatoria.insert(END,respuesta_importe)
        sumatoria.config(font=('italic',10),foreground='black')
    except:
        pass
    
  
sumatoria=Text(root,height=1,width=15)
sumatoria.grid(row=8,column=0)    
    
mov_todos()
def actualizar():
    #En la consulta no metemos mto electrico porque lo vamos a sumar después (coste) ya que así tenemos restados los posibles gastos por mto en los electrodomesticos    
    consulta=("select sum(importe) from inminente where categoria in ('OCIO A','OCIO B','AHORRO','HOGAR','SEGURO VEHICULO','LAVADO VEHICULO','NEUMATICOS','AMORTIZACION VEHICULO','MTO VEHICULO')")
    cursor.execute(consulta)
    total=cursor.fetchone()
    total=str(total)
    total=total[1:-2]
    total=float(total)
    total=total+coste
    total=round(total,2)
    total=str(total)
    total='SALDO ACTUAL: '+total+'€'
    acumulado.config(text=total)

   
boton_ingresos=Button(root,text='INGRESOS',command=mov_ingresos)
boton_ingresos.grid(row=0,column=3)

boton_gastos=Button(root,text='GASTOS',command=mov_gastos)
boton_gastos.grid(row=0,column=2)

boton_todo=Button(root,text='TODOS',command=mov_todos)
boton_todo.grid(row=0,column=1)

boton_todo=Button(root,text='ACTUALIZAR',command=actualizar)
boton_todo.grid(row=0,column=4)

desplegable_buscar=Combobox(root,values=['BUSCAR TODOS LOS RESULTADOS','BUSCAR TODOS LOS GASTOS','BUSCAR TODOS LOS INGRESOS'],width=30,state='readonly')
desplegable_buscar.grid(row=4,column=0,padx=60)   
desplegable_buscar.current(0)

desplegable_meses=Combobox(root,values=meses,width=30,state='readonly')
desplegable_meses.grid(row=5,column=0,padx=60)   
desplegable_meses.current(0)

#Generamos la lista de años automáticamente a partir de 2020
lista_aNos=['TODOS LOS AÑOS REGISTRADOS']
now=datetime.now()
aNo_actual=now.year
aNo_actual=aNo_actual+1
for n in range(2020,aNo_actual):
    lista_aNos.append(n)
desplegable_aNos=Combobox(root,values=lista_aNos,width=30,state='readonly')
desplegable_aNos.grid(row=6,column=0,padx=60)   
desplegable_aNos.current(0)
boton_sumatoria=Button(root,text='OBTENER',command=buscar_mov)
boton_sumatoria.grid(row=7,column=0)

indicaciones=Label(root,text='*Introduce "TODAS" junto con "BUSCAR TODOS LOS RESULTADOS" para sumar todos los costes de las categorias de una fecha elegida')
indicaciones.grid(row=2,column=0)
cuadro_busqueda=Entry(0,width=30,borderwidth=1)
cuadro_busqueda.grid(row=3,column=0)   



menu_reparto=Menu(menubar,tearoff=0)
menu_reparto.add_command(label='REPARTO GASTOS',command=reparto)

menu_registrar=Menu(menubar,tearoff=0)
menu_registrar.add_command(label='REGISTRAR INGRESOS',command=registrar_ingresos)
menu_registrar.add_command(label='REGISTRAR GASTOS',command=registrar_gastos)


menu_conocer=Menu(menubar,tearoff=0)
menu_conocer.add_command(label='CONOCER MTO ELÉCTRICO',command=conocer_mto_electrico)


contabilidad=Menu(menubar,tearoff=0)
contabilidad.add_cascade(label='CONOCER',menu = menu_conocer)
contabilidad.add_cascade(label='REGISTRAR',menu=menu_registrar)

menubar.add_cascade(label='CONTABILIDAD',menu=contabilidad)
menubar.add_cascade(label='REPARTO GASTOS',menu=menu_reparto)




root.config(menu=menubar)
root.mainloop()
