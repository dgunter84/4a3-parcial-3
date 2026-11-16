import mysql.connector
import tkinter as tk
from tkinter import messagebox, simpledialog

from coches import cochesBD


class App:
    CAMPOS_COCHE = ("Marca", "Color", "Modelo", "Velocidad", "Potencia", "Asientos")

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Gestion de coches")
        self.ventana.geometry("760x520")
        self.ventana.resizable(False, False)
        self.main()

    def limpiar(self):
        for widget in self.ventana.winfo_children():
            widget.destroy()

    def crear_titulo(self, texto):
        tk.Label(self.ventana, text=texto).pack(pady=12)

    def main(self):
        self.limpiar()
        self.crear_titulo("MENU PRINCIPAL")
        tk.Button(self.ventana, text="Coches", command=self.menuCoche).pack(pady=5)
        tk.Button(self.ventana, text="Salir", command=self.ventana.destroy).pack(pady=5)

    def menuCoche(self):
        self.limpiar()
        self.crear_titulo("MENU DE COCHES")
        acciones = (
            ("Agregar", self.agregarCoche),
            ("Borrar", self.borrarCoche),
            ("Modificar", self.modificarCoche),
            ("Mostrar", self.mostrarCoches),
            ("Regresar", self.main),
        )
        for texto, accion in acciones:
            tk.Button(self.ventana, text=texto, command=accion).pack(pady=4)

    def agregarCoche(self):
        self.formularioCoche("agregar")

    def modificarCoche(self):
        self.formularioCoche("modificar")

    def formularioCoche(self, modo):
        self.limpiar()
        titulo = "AGREGAR COCHE" if modo == "agregar" else "MODIFICAR COCHE"
        self.crear_titulo(titulo)

        id_coche = tk.StringVar()
        if modo == "modificar":
            tk.Label(self.ventana, text="ID del coche").pack()
            tk.Entry(self.ventana, textvariable=id_coche).pack(pady=3)

        entradas = {}
        for campo in self.CAMPOS_COCHE:
            tk.Label(self.ventana, text=campo).pack()
            entrada = tk.Entry(self.ventana)
            entrada.pack(pady=3)
            entradas[campo] = entrada

        def guardar():
            valores = [entradas[campo].get().strip() for campo in self.CAMPOS_COCHE]
            if not all(valores):
                messagebox.showwarning("Datos incompletos", "Completa todos los campos.", parent=self.ventana)
                return

            coche = cochesBD.CochesBD(*valores)
            if modo == "agregar":
                respuesta = coche.insertar()
            else:
                identificador = id_coche.get().strip()
                if not identificador:
                    messagebox.showwarning("Dato requerido", "Escribe el ID del coche.", parent=self.ventana)
                    return
                respuesta = coche.actualizar(identificador)

            if respuesta:
                messagebox.showinfo("Coches", "Accion realizada con exito.", parent=self.ventana)
                self.menuCoche()
            else:
                messagebox.showerror("Coches", "No se pudo guardar. Revisa la conexion, los datos y el ID.", parent=self.ventana)

        tk.Button(self.ventana, text="Guardar", command=guardar).pack(pady=8)
        tk.Button(self.ventana, text="Regresar", command=self.menuCoche).pack(pady=4)

    def borrarCoche(self):
        identificador = simpledialog.askstring("Borrar coche", "ID del coche a borrar:", parent=self.ventana)
        if identificador is None:
            return
        identificador = identificador.strip()
        if not identificador:
            messagebox.showwarning("Dato requerido", "Escribe el ID del coche.", parent=self.ventana)
            return

        if cochesBD.CochesBD.eliminar(identificador):
            messagebox.showinfo("Coches", "Coche borrado.", parent=self.ventana)
        else:
            messagebox.showerror("Coches", "No se pudo borrar: revisa la conexion y el ID.", parent=self.ventana)

    def mostrarCoches(self):
        self.limpiar()
        self.crear_titulo("COCHES REGISTRADOS")
        lista = tk.Listbox(self.ventana, width=88, height=18)
        lista.pack(padx=8, pady=5)
        registros = cochesBD.CochesBD.consultar()
        if registros:
            for registro in registros:
                lista.insert(tk.END, " | ".join(str(valor) for valor in registro))
        else:
            lista.insert(tk.END, "No hay coches registrados o no hay conexion con la base de datos.")
        tk.Button(self.ventana, text="Regresar", command=self.menuCoche).pack(pady=5)


if __name__ == "__main__":
    ventana = tk.Tk()
    App(ventana)
    ventana.mainloop()
