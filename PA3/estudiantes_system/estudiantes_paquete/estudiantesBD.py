from conexionBD import cursor, conexion


class EstudiantesBD:
    def __init__(self, nombre, nota):
        self._nombre = nombre
        self._nota = nota

    @staticmethod
    def _conexion_disponible():
        return conexion is not None and cursor is not None

    def insertar(self):
        if not self._conexion_disponible():
            return False
        try:
            cursor.execute("insert into estudiante values(NULL, %s, %s)", (self._nombre, self._nota))
            conexion.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def consultar():
        if not EstudiantesBD._conexion_disponible():
            return []
        try:
            cursor.execute("select * from estudiante")
            return cursor.fetchall()
        except Exception as e:
            print(e)
            return []

    @staticmethod
    def eliminar(id):
        if not EstudiantesBD._conexion_disponible():
            return False
        try:
            cursor.execute("delete from estudiante where id= %s", (id,))
            eliminado = cursor.rowcount > 0
            conexion.commit()
            return eliminado
        except Exception as e:
            print(e)
            return False

    def actualizar(self, id):
        if not self._conexion_disponible():
            return False
        try:
            cursor.execute("select id from estudiante where id=%s", (id,))
            if cursor.fetchone() is None:
                return False
            cursor.execute("update estudiante set nombre=%s, nota=%s where id=%s", (self._nombre, self._nota, id))
            conexion.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre

    @property
    def nota(self):
        return self._nota

    @nota.setter
    def nota(self, nota):
        self._nota = nota
