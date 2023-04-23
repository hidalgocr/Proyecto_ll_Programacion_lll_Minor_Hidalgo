import clases
from tkinter import *
from PIL import Image, ImageTk

class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("Bienvenidos a Laboratorios")

        # Cargar imagen de fondo
        self.bg_image = ImageTk.PhotoImage(Image.open("fondo.jpg"))

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
        self.welcome_label = Label(self.header_frame, text="Bienvenidos a Registros de Laboratorios", font=("Arial", 30, "bold"), fg="white", bg="#0D47A1")
        self.welcome_label.pack()

        # Crear botón para abrir la ventana de consulta
        self.consultar_button = Button(self.frame, text="Consultar Laboratorios", command=self.open_clases, bg="#555555", fg="white")
        self.consultar_button.pack()

        # Crear botón para abrir la ventana Registros
        self.nueva_ventana_button = Button(self.frame, text="Registros", command=self.open_nueva_registros, bg="#555555", fg="white")
        self.nueva_ventana_button.pack(pady=5)
        self.nueva_ventana_button = Button(self.frame, text="Calculos", command=self.open_nueva_calculos, bg="#555555", fg="white")
        self.nueva_ventana_button.pack(pady=5)
        self.salir_button = Button(self.frame, text="Salir", command=self.master.destroy, bg="#555555", fg="white")
        self.salir_button.pack(pady=5)

    def open_clases(self):
        root = Toplevel()
        interfaz = clases.Interfaz(root)

    def open_nueva_registros(self):
        root = Toplevel()
        registros_lab = clases.Registros(root)

    def open_nueva_calculos(self):
        root = Toplevel()
        calculos_lab = clases.Calculos(root)


root = Tk()
# root.geometry("500x500")
root.geometry("800x600+{}+{}".format(int(root.winfo_screenwidth()/2 - 400), int(root.winfo_screenheight()/2 - 300)))
root.resizable(False, False)
main_window = MainWindow(root)
root.mainloop()
