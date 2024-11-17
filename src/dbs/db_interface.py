import sqlite3
import tkinter as tk
from tkinter import Listbox, messagebox
from tkinter import simpledialog
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

db_path = 'Paquito Flores.db'

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)

    # Relación con las notificaciones
    notifications = relationship("Notification", back_populates="president")

class Notification(Base):
    __tablename__ = 'notificationes'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    text = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    # Columna para almacenar el ID del presidente (usuario)
    president_id = Column(Integer, ForeignKey('users.id'), nullable=False)  
    
    # Relación con la clase User
    president = relationship("users", back_populates="notificationes")

class Voting(Base):
    __tablename__ = 'votaciones'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # Relación con las tablas User y Option
    option = relationship("opciones", back_populates="votaciones")
    
class Option(Base):
    __tablename__ = 'opciones'
    
    id = Column(Integer, primary_key=True)
    voting_id = Column(Integer, ForeignKey('votaciones.id'), nullable=False)
    option_text = Column(String, nullable=False)

    # Relación con la clase Voting
    voting = relationship("votaciones", back_populates="opciones")

# Tabla de votos
class Vote(Base):
    __tablename__ = 'votes'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    option_id = Column(Integer, ForeignKey('opciones.id'), nullable=False)

    # Relaciones
    user = relationship("users", back_populates="votes")
    option = relationship("opciones", backref="votes")

class Quota(Base):
    __tablename__ = 'cuotas'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String, nullable=False)  # Nueva columna para el nombre de la cuota
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, nullable=False)
    
    fine_id = Column(Integer, ForeignKey('multas.id'))


class Fine(Base):
    __tablename__ = 'multas'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    quota_id = Column(Integer, ForeignKey('cuotas.id'))  # Nueva relación con la cuota
    date = Column(DateTime, default=datetime.datetime.utcnow)

def create_database(db_name):
    engine = create_engine(f'sqlite:///{db_name}.db')  # Cambia la ruta según tu preferencia
    Base.metadata.create_all(engine)  # Crea todas las tablas definidas en Base
    return engine

def on_create_database():
    db_name = entry_db_name.get()
    if db_name.strip() == "":
        messagebox.showwarning("Advertencia", "Por favor, ingrese un nombre para la base de datos.")
        return

    try:
        global db_path
        db_path = f"{db_name}.db"
        engine = create_database(db_name)
        messagebox.showinfo("Éxito", f"Base de datos '{db_name}.db' y tablas creadas.")
        entry_db_name.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al crear la base de datos: {e}")


def conectar(db_path):
    """Función para conectar a la base de datos."""
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

def cerrar(conn):
    """Función para cerrar la conexión a la base de datos."""
    if conn:
        conn.close()

def crear_tabla():
    nombre_tabla = simpledialog.askstring("Crear Tabla", "Ingrese el nombre de la tabla:")
    columnas = simpledialog.askstring("Crear Tabla", "Ingrese las columnas (ejemplo: 'id INTEGER PRIMARY KEY, nombre TEXT'):")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {nombre_tabla} ({columnas})')
        conn.commit()
        messagebox.showinfo("Éxito", f"Tabla '{nombre_tabla}' creada correctamente.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Ocurrió un error al crear la tabla: {e}")
    finally:
        cursor.close()
        conn.close()

def mostrar_tablas():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = cursor.fetchall()
        return [tabla[0] for tabla in tablas]
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Ocurrió un error al obtener las tablas: {e}")
    finally:
        cursor.close()
        conn.close()

def borrar_tabla():
    tablas = mostrar_tablas()
    if not tablas:
        messagebox.showinfo("Tablas en la base de datos", "No hay tablas en la base de datos.")
        return

    ventana_borrar = tk.Toplevel()
    ventana_borrar.title("Borrar Tabla")
    ventana_borrar.geometry("400x400")  # Ventana más grande

    label = tk.Label(ventana_borrar, text="Seleccione una tabla para borrar:", font=("Helvetica", 14))
    label.pack(pady=10)

    listbox = Listbox(ventana_borrar, height=15, width=40)
    listbox.pack(pady=10)

    for tabla in tablas:
        listbox.insert(tk.END, tabla)

    def confirmar_borrado():
        nombre_tabla = listbox.get(tk.ACTIVE)
        if not nombre_tabla:
            messagebox.showwarning("Advertencia", "Seleccione una tabla para borrar.")
            return

        respuesta = messagebox.askyesno("Confirmar Borrado", f"¿Está seguro de que desea borrar la tabla '{nombre_tabla}'?")
        if respuesta:
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute(f'DROP TABLE IF EXISTS {nombre_tabla}')
                conn.commit()
                messagebox.showinfo("Éxito", f"Tabla '{nombre_tabla}' borrada correctamente.")
                ventana_borrar.destroy()  # Cierra la ventana después de borrar
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Ocurrió un error al borrar la tabla: {e}")
            finally:
                cursor.close()
                conn.close()

    # Agregar botón para confirmar el borrado
    btn_borrar = tk.Button(ventana_borrar, text="Borrar Tabla", command=confirmar_borrado)
    btn_borrar.pack(pady=10)

    btn_cerrar = tk.Button(ventana_borrar, text="Cerrar", command=ventana_borrar.destroy)
    btn_cerrar.pack(pady=10)

def mostrar_contenido_tabla(nombre_tabla):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {nombre_tabla}')
        registros = cursor.fetchall()

        if registros:
            # Obtener nombres de columnas
            column_names = [description[0] for description in cursor.description]
            # Formatear la salida
            contenido_str = f"{', '.join(column_names)}\n" + "\n".join([str(registro) for registro in registros])
            messagebox.showinfo(f"Contenido de la tabla '{nombre_tabla}'", contenido_str)
        else:
            messagebox.showinfo(f"Contenido de la tabla '{nombre_tabla}'", "La tabla está vacía.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Ocurrió un error al acceder a la tabla: {e}")
    finally:
        cursor.close()
        conn.close()

def mostrar_contenido_todas_las_tablas():
    tablas = mostrar_tablas()
    if not tablas:
        messagebox.showinfo("Tablas en la base de datos", "No hay tablas en la base de datos.")
        return

    contenido_total = ""
    for tabla in tablas:
        cursor = sqlite3.connect(db_path).cursor()
        cursor.execute(f'SELECT * FROM {tabla}')
        registros = cursor.fetchall()

        if registros:
            # Obtener nombres de columnas
            column_names = [description[0] for description in cursor.description]
            contenido_total += f"\nContenido de la tabla '{tabla}':\n"
            contenido_total += f"{', '.join(column_names)}\n" + "\n".join([str(registro) for registro in registros]) + "\n\n"
        else:
            contenido_total += f"\nContenido de la tabla '{tabla}':\nLa tabla está vacía.\n\n"
        cursor.close()

    messagebox.showinfo("Contenido de Todas las Tablas", contenido_total)

def mostrar_contenido_tabla_seleccionada():
    tablas = mostrar_tablas()
    if not tablas:
        messagebox.showinfo("Tablas en la base de datos", "No hay tablas en la base de datos.")
        return

    ventana_tablas = tk.Toplevel()
    ventana_tablas.title("Seleccionar Tabla")
    ventana_tablas.geometry("400x400")  # Ventana más grande
    
    label = tk.Label(ventana_tablas, text="Seleccione una tabla:", font=("Helvetica", 14))
    label.pack(pady=10)

    listbox = Listbox(ventana_tablas, height=15, width=40)
    listbox.pack(pady=10)

    for tabla in tablas:
        listbox.insert(tk.END, tabla)

    btn_mostrar_contenido = tk.Button(ventana_tablas, text="Mostrar Contenido", command=lambda: mostrar_contenido_tabla(listbox.get(tk.ACTIVE)))
    btn_mostrar_contenido.pack(pady=10)

    btn_cerrar = tk.Button(ventana_tablas, text="Cerrar", command=ventana_tablas.destroy)
    btn_cerrar.pack(pady=10)

# Crear la ventana principal
# Crear la ventana principal
def crear_ventana():
    ventana = tk.Tk()
    ventana.title("Gestor de Base de Datos")
    ventana.geometry("400x500")
    ventana.configure(bg="#f0f0f0")  # Color de fondo

    # Estilo
    label = tk.Label(ventana, text="Menú de Base de Datos", font=("Helvetica", 18), bg="#f0f0f0", fg="#333")
    label.pack(pady=20)

    # Campo de entrada para el nombre de la base de datos
    global entry_db_name
    entry_db_name = tk.Entry(ventana, width=30, font=("Helvetica", 12))
    entry_db_name.pack(pady=10)
    entry_db_name.insert(0, "Nombre de la base de datos")

    # Botones personalizados
    style = {
        "bg": "#007BFF",  # Color de fondo de los botones
        "fg": "white",    # Color de texto
        "font": ("Helvetica", 12),
        "activebackground": "#0056b3",  # Color al hacer clic
        "width": 30,
        "borderwidth": 2,
        "relief": "flat"
    }

    btn_crear_db = tk.Button(ventana, text="Crear Base de Datos", command=on_create_database, **style)
    btn_crear_db.pack(pady=10)

    btn_crear_tabla = tk.Button(ventana, text="Crear Tabla", command=crear_tabla, **style)
    btn_crear_tabla.pack(pady=10)

    btn_mostrar_tablas = tk.Button(ventana, text="Ver Tablas", command=mostrar_contenido_tabla_seleccionada, **style)
    btn_mostrar_tablas.pack(pady=10)

    btn_mostrar_contenido_todas = tk.Button(ventana, text="Ver Contenido de Todas las Tablas", command=mostrar_contenido_todas_las_tablas, **style)
    btn_mostrar_contenido_todas.pack(pady=10)

    btn_borrar_tabla = tk.Button(ventana, text="Borrar Tabla", command=borrar_tabla, **style)
    btn_borrar_tabla.pack(pady=10)

    btn_salir = tk.Button(ventana, text="Salir", command=ventana.quit, **style)
    btn_salir.pack(pady=20)

    ventana.mainloop()

if __name__ == '__main__':
    # Aquí se puede abrir la ventana de gestión de la base de datos
    crear_ventana()
    print("Gestión de la base de datos abierta.")
