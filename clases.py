from tkinter import *
import tkinter.messagebox
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import datetime
from funciones import calcular_porcentaje, calcular_porcentaje_equipos, calcular_promedio_elementos

from funciones import validarFecha


class Laboratorio:
    __instance = None

    def __init__(self):
        if Laboratorio.__instance is None:
            Laboratorio.__instance = self
            self.labs = {}

    @staticmethod
    def getInstance():
        if not Laboratorio.__instance:
            Laboratorio()
        return Laboratorio.__instance

    def agregarLaboratorio(self, num):
        self.labs[num] = {}
        

    # def obtenerDisponibilidad(self, num, fecha):
    #     with open("registros.txt", "r") as f:
    #         for line in f:
    #             if f"Laboratorio {num}, fecha {fecha}: RESERVADO" in line:
    #                 return False
    #     return True
    def obtenerDisponibilidad(self, num, fecha):
        if num not in self.labs:
            messagebox.showerror("Error", f"El número de laboratorio {num} no existe.")
            return False

        with open("registros.txt", "r") as f:
            for line in f:
                if f"Laboratorio {num}, fecha {fecha}: RESERVADO" in line:
                    return False
        return True


    def reservarLaboratorio(self, num, fecha, nombre, seccion):
        # Verificar si la fecha ya ha sido reservada en cualquier laboratorio
        with open("registros.txt", "r") as f:
            for line in f:
                if f"fecha {fecha}" in line:
                    return False

        # Reservar el laboratorio en la memoria
        if num not in self.labs:
            messagebox.showerror("Error", f"El número de laboratorio {num} no existe.")
            return False
        lab = self.labs[num]
        if fecha in lab and not lab[fecha]:
            return False
        lab[fecha] = False

        # Agregar una nueva entrada en el archivo
        try:
            with open("registros.txt", "a") as f:
                f.write(f"Laboratorio {num}, fecha {fecha}: RESERVADO al docente {nombre} de la seccion: {seccion}\n")
        except IOError:
            print("No se pudo escribir en el archivo 'registros.txt'")

        return True



    
    def cambiarDisponibilidad(self, num, fecha, disponible=True):
            if num not in self.labs:
                return False
            lab = self.labs[num]
            if fecha not in lab:
                return False
            lab[fecha] = disponible
            return True
    

    def generarArchivo(self, archivo):
        if os.path.isfile(archivo):
            tkinter.messagebox.showerror("Error", f"No se puede generar un nuevo archivo porque {archivo} ya existe.")
            return
        
        with open(archivo, "w") as f:
            for num, lab in self.labs.items():
                for fecha, reservado in lab.items():
                    if reservado is False:
                        registro = f"Laboratorio {num}, fecha {fecha}: RESERVADO\n"
                        f.write(registro)
                    else:
                        registro = f"Laboratorio {num}, fecha {fecha}: DISPONIBLE\n"
                        f.write(registro)

    def reemplazarArchivo(self, archivo):
        with open(archivo, "w") as f:
            for num, lab in self.labs.items():
                for fecha, reservado in lab.items():
                    if reservado is False:
                        registro = f"Laboratorio {num}, fecha {fecha}: RESERVADO\n"
                        f.write(registro)
                    else:
                        registro = f"Laboratorio {num}, fecha {fecha}: DISPONIBLE\n"
                        f.write(registro)


                        


class Interfaz:
    def __init__(self, master):
        self.num = None
        self.fecha = None
        self.master = master
        master.title("Reserva de laboratorios")
        # self.master.geometry("500x500")
        master.geometry("800x600+{}+{}".format(int(master.winfo_screenwidth()/2 - 400), int(master.winfo_screenheight()/2 - 300)))
        master.resizable(False, False)
        
        self.lab = Laboratorio.getInstance()

        # Agregar algunos laboratorios al sistema
        self.lab.agregarLaboratorio(1)
        self.lab.agregarLaboratorio(2)
        self.lab.agregarLaboratorio(3)
        

        # Crear el contenedor principal para la imagen de fondo
        self.bg_frame = Frame(master)
        self.bg_frame.pack(fill=BOTH, expand=True)

        # Establecer la imagen de fondo
        self.bg_image = ImageTk.PhotoImage(Image.open("fondo.jpg"))

        self.bg_label = Label(self.bg_frame, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Crear el sub-contenedor para los widgets
        self.frame = Frame(self.bg_frame, bg="#90EE90")
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Crear los widgets de la Interfaz
        self.label_num = Label(self.frame, text="Ingrese el número del laboratorio:", bg="#555555", fg="white")
        self.label_num.pack(pady=3)

        self.num_entry = Entry(self.frame)
        self.num_entry.pack(pady=3)

        self.label_fecha = Label(self.frame, text="Ingrese la fecha (dd/mm/aaaa):", bg="#555555", fg="white")
        self.label_fecha.pack(pady=3)

        self.fecha_entry = Entry(self.frame)
        self.fecha_entry.pack(pady=3)

        self.disp_button = Button(self.frame, text="Consultar disponibilidad", command=self.consultarDisponibilidad, bg="#555555", fg="white")
        self.disp_button.pack(pady=3)

        self.res_button = Button(self.frame, text="Reservar laboratorio", command=self.pedirDatosReserva, bg="#555555", fg="white")
        self.res_button.pack(pady=3)
        self.elim_button = Button(self.frame, text="Eliminar reserva", command=self.pedirDatosEliminacion, bg="#555555", fg="white")

        self.elim_button.pack(pady=3)

        self.status_label = Label(self.frame, text="", bg="#ffffff")
        self.status_label.pack()

        self.status_label_available = Label(self.frame, text="", bg="#ffffff")
        self.status_label_available.pack()



    def consultarDisponibilidad(self):
        num = int(self.num_entry.get())
        fecha = self.fecha_entry.get()

        if not validarFecha(fecha):
            self.status_label_available.config(text="La fecha debe tener el formato dd/mm/aaaa", fg="red")
            return
        disponible = self.lab.obtenerDisponibilidad(num, fecha)
        if disponible is None:
            self.status_label_available.config(text=f"No se encontró el laboratorio {num}", fg="red")
        elif disponible:
            self.status_label_available.config(text=f"El laboratorio {num} está disponible para la fecha {fecha}", fg="green")
        else:
            self.status_label_available.config(text=f"El laboratorio {num} no está disponible para la fecha {fecha}", fg="red")


    def pedirDatosReserva(self):
        # Crear una nueva ventana de diálogo para pedir al usuario el número y fecha de la reserva a eliminar
        dialog = Toplevel(self.master)

        dialog.geometry("300x300")


        # Crear un Frame que cubra toda la ventana emergente y establecer su color de fondo en negro
        bg_frame = Frame(dialog, bg="#0D47A1")
        bg_frame.place(x=0, y=0, relwidth=1, relheight=1)
        

        label_num = Label(dialog, text="Ingrese el número del laboratorio:", bg="#555555", fg="white")
        label_num.pack(pady=3)

        num_entry = Entry(dialog)
        num_entry.pack(pady=3)

        label_fecha = Label(dialog, text="Ingrese la fecha (dd/mm/aaaa):", bg="#555555", fg="white")
        label_fecha.pack(pady=3)

        fecha_entry = Entry(dialog)
        fecha_entry.pack(pady=3)

        label_nombre = Label(dialog, text="Nombre Docente: ", bg="#555555", fg="white")
        label_nombre.pack(pady=3)

        nombre_entry = Entry(dialog)
        nombre_entry.pack(pady=3)

        label_seccion = Label(dialog, text="Seccion: ", bg="#555555", fg="white")
        label_seccion.pack(pady=3)

        seccion_entry = Entry(dialog)
        seccion_entry.pack(pady=3)
        
    # Crear una función para validar los datos ingresados
        def validarDatos():
            # Validar el campo del número de laboratorio
            if not num_entry.get().isdigit():
                messagebox.showerror("Error", "El número de laboratorio debe ser un valor numérico.")
                return False
            
            if not num_entry.get() or not fecha_entry.get() or not nombre_entry.get() or not seccion_entry.get():
                messagebox.showerror("Error", "Debe completar todos los campos.")
                return False
            try:
                datetime.datetime.strptime(fecha_entry.get(), "%d/%m/%Y")
            except ValueError:
                messagebox.showerror("Error", "La fecha debe estar en el formato dd/mm/aaaa.")
                return False
            return True

        # Crear un botón para confirmar los datos ingresados 
        confirm_button = Button(dialog, text="Reservar", command=lambda: 
            validarDatos() and self.reservarLaboratorio(num_entry.get(), fecha_entry.get(), nombre_entry.get(), seccion_entry.get()), 
            bg="#555555", fg="white")
        confirm_button.pack(pady=3)

        self.status_label = Label(dialog, text="", bg="#555555", fg="white")
        self.status_label.pack(pady=3)
        


        # # Crear un botón para confirmar los datos ingresados 
        # confirm_button = Button(dialog, text="Reservar", command=lambda: self.reservarLaboratorio(num_entry.get(), fecha_entry.get(), nombre_entry.get(), seccion_entry.get()), bg="#555555", fg="white")
        # confirm_button.pack(pady=3)

        # # Crear un Label para mostrar el estado de la reserva
        # self.status_label = Label(dialog, text="", bg="#90EE90", fg="white")
        # self.status_label.pack(pady=3)

        # # Guardar los valores ingresados por el usuario en los atributos de la instancia de interfaz
        # self.num = num_entry.get()
        # self.fecha = fecha_entry.get()
        # self.nombre = nombre_entry.get()
        # self.seccion = seccion_entry.get()

    def reservarLaboratorio(self, num, fecha, nombre, seccion):
        num = int(num)
        fecha = fecha
        nombre = nombre
        seccion = seccion
        if self.lab.reservarLaboratorio(num, fecha, nombre, seccion):
            # self.status_label.config(text=f"Se reservó el laboratorio {num} para la fecha {fecha}", fg="green")
            messagebox.showinfo("Se ha registrado su reserva", f"Se a reservado el laboratorio {num}, para el {fecha}")
        else:
            self.status_label.config(text=f"No se pudo reservar el laboratorio {num} para la fecha {fecha}", fg="red")


    def pedirDatosEliminacion(self):
        # Crear una nueva ventana de diálogo para pedir al usuario el número y fecha de la reserva a eliminar
        dialog = Toplevel(self.master)
        dialog.geometry("200x150")

        # Crear un Frame que cubra toda la ventana emergente y establecer su color de fondo en negro
        bg_frame = Frame(dialog, bg="#0D47A1")
        bg_frame.place(x=0, y=0, relwidth=1, relheight=1)

        label_num = Label(dialog, text="Ingrese el número del laboratorio:", bg="#555555", fg="white")
        label_num.pack(pady=3)

        num_entry = Entry(dialog)
        num_entry.pack(pady=3)

        label_fecha = Label(dialog, text="Ingrese la fecha (dd/mm/aaaa):", bg="#555555", fg="white")
        label_fecha.pack(pady=3)

        fecha_entry = Entry(dialog)
        fecha_entry.pack(pady=3)

        # Crear una función para validar los campos
        def validar_campos():
            # Obtener los valores de los campos
            num = num_entry.get()
            fecha = fecha_entry.get()

            # Validar que los campos no estén vacíos
            if num.strip() == "" or fecha.strip() == "":
                messagebox.showerror("Error", "Por favor, complete todos los campos")
                return False

            # Validar que la fecha tenga el formato correcto (dd/mm/aaaa)
            try:
                datetime.datetime.strptime(fecha, '%d/%m/%Y')
            except ValueError:
                messagebox.showerror("Error", "El formato de la fecha es incorrecto. Debe ser dd/mm/aaaa")
                return False

            # Validar que el número del laboratorio sea un entero
            try:
                int(num)
            except ValueError:
                messagebox.showerror("Error", "El número del laboratorio debe ser un número entero")
                return False

            # Si todo está bien, retornar True
            return True

        # Crear un botón para confirmar los datos ingresados y eliminar la reserva correspondiente
        confirm_button = Button(dialog, text="Eliminar", command=lambda: self.eliminarReserva(num_entry.get(), fecha_entry.get()) if validar_campos() else None, bg="#555555", fg="white")
        confirm_button.pack(pady=3)

        # Guardar los valores ingresados por el usuario en los atributos de la instancia de la Interfaz
        self.num = num_entry.get()
        self.fecha = fecha_entry.get()



        # # Crear un botón para confirmar los datos ingresados y eliminar la reserva correspondiente
        # confirm_button = Button(dialog, text="Eliminar", command=lambda: self.eliminarReserva(num_entry.get(), fecha_entry.get()), bg="#555555", fg="white")
        # confirm_button.pack(pady=3)

        # # Guardar los valores ingresados por el usuario en los atributos de la instancia de la Interfaz
        # self.num = num_entry.get()
        # self.fecha = fecha_entry.get()

    
    def eliminarReserva(self, num, fecha):
        archivo = open("registros.txt", "r+")
        contenido = archivo.readlines()
        archivo.seek(0)
        eliminado = False
        for linea in contenido:
            if f"{num}, fecha {fecha}" not in linea:
                archivo.write(linea)
                
            else:
                eliminado = True
        archivo.truncate()
        archivo.close()
        if eliminado:
            messagebox.showinfo("Reserva eliminada", f"Se ha eliminado la reserva del laboratorio {num} para la fecha {fecha} satisfactoriamente.")
        else:
            messagebox.showerror("Error", "No se pudo eliminar la reserva. Por favor, verifique los datos ingresados e intente de nuevo.")

    # def obtenerDisponibilidad(self, num, fecha):
    #     if num not in self.labs:
    #         messagebox.showerror("Error", f"El número de laboratorio {num} no existe.")
    #         return False


class Registros:
    def __init__(self, master):
        self.master = master
        master.title("Registros")

        # Cargar imagen de fondo
        self.bg_image = ImageTk.PhotoImage(Image.open("fondo.jpg"))

        # Establecer tamaño y posición de la ventana
        master.geometry("800x600+{}+{}".format(int(master.winfo_screenwidth()/2 - 400), int(master.winfo_screenheight()/2 - 300)))
        master.resizable(False, False)


        # Crear contenedor principal para la imagen de fondo
        self.bg_frame = Frame(master)
        self.bg_frame.pack(fill=BOTH, expand=True)

        # Establecer la imagen de fondo
        self.bg_label = Label(self.bg_frame, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Crear marco secundario para centrar el contenido
        self.frame = Frame(self.bg_frame, bg="#90EE90")
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Crear un nuevo frame para el encabezado
        self.header_frame = Frame(self.bg_frame, bg="#90EE90")
        self.header_frame.pack(side=TOP, pady=20)

        # Crear el encabezado
        self.welcome_label = Label(self.header_frame, text="Bienvenidos a Informes", font=("Arial", 30, "bold"), fg="white", bg="#0D47A1")
        self.welcome_label.pack()



        self.registros_button = Button(self.frame, text="Generar registros", command=self.generarRegistros, bg="#555555", fg="white")
        self.registros_button.pack(pady=3)

        self.eliminar_button = Button(self.frame, text="Eliminar Registros", command=self.eliminarRegistros, bg="#555555", fg="white")
        self.eliminar_button.pack(pady=3)
        
    def generarRegistros(self):
        lab = Laboratorio.getInstance()
        lab.generarArchivo("registros.txt")
        lab.reemplazarArchivo("registros.txt")

    def eliminarRegistros(self):
        lab = Laboratorio.getInstance()
        lab.reemplazarArchivo("registros.txt")

class Calculos:
    def mostrar_resultado(self):
        resultado = calcular_porcentaje()
        self.resultado_label.config(text=resultado)

    def mostrar_resultado_media(self):
        resultado_media = calcular_promedio_elementos()
        self.resultado_label.config(text=resultado_media)

    def mostrar_resultado_promedio(self):
        resultadosporcentaje = calcular_porcentaje_equipos()
        self.resultado_label.config(text=resultadosporcentaje)

    def __init__(self, master):
        self.master = master
        master.title("Calculos")

        # Cargar imagen de fondo
        self.bg_image = ImageTk.PhotoImage(Image.open("fondo.jpg"))

        # Establecer tamaño y posición de la ventana
        master.geometry("800x600+{}+{}".format(int(master.winfo_screenwidth()/2 - 400), int(master.winfo_screenheight()/2 - 300)))
        master.resizable(False, False)


        # Crear contenedor principal para la imagen de fondo
        self.bg_frame = Frame(master)
        self.bg_frame.pack(fill=BOTH, expand=True)

        # Establecer la imagen de fondo
        self.bg_label = Label(self.bg_frame, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Crear marco secundario para centrar el contenido
        self.frame = Frame(self.bg_frame, bg="#90EE90")
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Crear un nuevo frame para el encabezado
        self.header_frame = Frame(self.bg_frame, bg="#90EE90")
        self.header_frame.pack(side=TOP, pady=20)

        # Crear el encabezado
        self.calculo_label = Label(self.header_frame, text="Bienvenidos a Calculos", font=("Arial", 30, "bold"), fg="white", bg="#0D47A1")
        self.calculo_label.pack()

        # creamos el botón para calcular el porcentaje
        self.calcular_button = Button(self.frame, text="Calcular porcentaje computadoras", command=self.mostrar_resultado, bg="#555555", fg="white")
        self.calcular_button.pack(pady=3)
        # creamos el botón para calcular el porcentaje

        self.calcular_media_button = Button(self.frame, text="Calculo Media Elementos Laboratorio", command=self.mostrar_resultado_media, bg="#555555", fg="white")
        self.calcular_media_button.pack(pady=3)

        # creamos el botón para calcular el porcentaje
        self.calcular_promedio_button = Button(self.frame, text="Calculo porcentaje Elementos Laboratorio", command=self.mostrar_resultado_promedio, bg="#555555", fg="white")
        self.calcular_promedio_button.pack(pady=3)

        # creamos un label para mostrar el resultado del porcentaje
        self.resultado_label = Label(self.frame, text="")
        self.resultado_label.pack(pady=3)

        # self.eliminar_button = Button(self.frame, text="Eliminar Registros", command=self.eliminarRegistros, bg="#555555", fg="white")
        # self.eliminar_button.pack(pady=3)

