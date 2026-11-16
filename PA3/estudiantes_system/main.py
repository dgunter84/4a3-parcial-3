import tkinter as tk
from tkinter import messagebox, simpledialog

from estudiantes_paquete import estudiantesBD


class App:
    CAMPOS_ESTUDIANTE = ("Nombre", "Nota")

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Gestion de estudiantes")
        self.ventana.geometry("560x420")
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
        tk.Button(self.ventana, text="Estudiantes", command=self.menuEstudiante).pack(pady=5)
        tk.Button(self.ventana, text="Salir", command=self.ventana.destroy).pack(pady=5)

    def menuEstudiante(self):
        self.limpiar()
        self.crear_titulo("MENU DE ESTUDIANTES")
        acciones = (
            ("Agregar", self.agregarEstudiante),
            ("Borrar", self.borrarEstudiante),
            ("Modificar", self.modificarEstudiante),
            ("Mostrar", self.mostrarEstudiantes),
            ("Regresar", self.main),
        )
        for texto, accion in acciones:
            tk.Button(self.ventana, text=texto, command=accion).pack(pady=4)

    def agregarEstudiante(self):
        self.formularioEstudiante("agregar")

    def modificarEstudiante(self):
        self.formularioEstudiante("modificar")

    def formularioEstudiante(self, modo):
        self.limpiar()
        titulo = "AGREGAR ESTUDIANTE" if modo == "agregar" else "MODIFICAR ESTUDIANTE"
        self.crear_titulo(titulo)

        id_estudiante = tk.StringVar()
        if modo == "modificar":
            tk.Label(self.ventana, text="ID del estudiante").pack()
            tk.Entry(self.ventana, textvariable=id_estudiante).pack(pady=3)

        entradas = {}
        for campo in self.CAMPOS_ESTUDIANTE:
            tk.Label(self.ventana, text=campo).pack()
            entrada = tk.Entry(self.ventana)
            entrada.pack(pady=3)
            entradas[campo] = entrada

        def guardar():
            valores = [entradas[campo].get().strip() for campo in self.CAMPOS_ESTUDIANTE]
            if not all(valores):
                messagebox.showwarning("Datos incompletos", "Completa todos los campos.", parent=self.ventana)
                return

            estudiante = estudiantesBD.EstudiantesBD(*valores)
            if modo == "agregar":
                respuesta = estudiante.insertar()
            else:
                identificador = id_estudiante.get().strip()
                if not identificador:
                    messagebox.showwarning("Dato requerido", "Escribe el ID del estudiante.", parent=self.ventana)
                    return
                respuesta = estudiante.actualizar(identificador)

            if respuesta:
                messagebox.showinfo("Estudiantes", "Accion realizada con exito.", parent=self.ventana)
                self.menuEstudiante()
            else:
                messagebox.showerror(
                    "Estudiantes",
                    "No se pudo guardar. Revisa la conexion, los datos y el ID.",
                    parent=self.ventana,
                )

        tk.Button(self.ventana, text="Guardar", command=guardar).pack(pady=8)
        tk.Button(self.ventana, text="Regresar", command=self.menuEstudiante).pack(pady=4)

    def borrarEstudiante(self):
        identificador = simpledialog.askstring(
            "Borrar estudiante", "ID del estudiante a borrar:", parent=self.ventana
        )
        if identificador is None:
            return
        identificador = identificador.strip()
        if not identificador:
            messagebox.showwarning("Dato requerido", "Escribe el ID del estudiante.", parent=self.ventana)
            return

        if estudiantesBD.EstudiantesBD.eliminar(identificador):
            messagebox.showinfo("Estudiantes", "Estudiante borrado.", parent=self.ventana)
        else:
            messagebox.showerror("Estudiantes", "No se pudo borrar: revisa la conexion y el ID.", parent=self.ventana)

    def mostrarEstudiantes(self):
        self.limpiar()
        self.crear_titulo("ESTUDIANTES REGISTRADOS")
        lista = tk.Listbox(self.ventana, width=64, height=14)
        lista.pack(padx=8, pady=5)
        registros = estudiantesBD.EstudiantesBD.consultar()
        if registros:
            for registro in registros:
                lista.insert(tk.END, " | ".join(str(valor) for valor in registro))
        else:
            lista.insert(tk.END, "No hay estudiantes registrados o no hay conexion con la base de datos.")
        tk.Button(self.ventana, text="Regresar", command=self.menuEstudiante).pack(pady=5)


if __name__ == "__main__":
    ventana = tk.Tk()
    App(ventana)
    ventana.mainloop()