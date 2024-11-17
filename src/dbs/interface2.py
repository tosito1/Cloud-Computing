import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Configuración inicial de las bases de datos
DBS = ["Paquito Flores.db", "Test.db"]
CURRENT_DB = DBS[0]


# Funciones de base de datos
def connect_to_db(db_path):
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
        return None


def get_tables():
    conn = connect_to_db(CURRENT_DB)
    if not conn:
        return []
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        return tables
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"No se pudo obtener las tablas: {e}")
        return []
    finally:
        conn.close()


def get_table_data(table_name):
    conn = connect_to_db(CURRENT_DB)
    if not conn:
        return [], []
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return columns, rows
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"No se pudo obtener los datos de la tabla '{table_name}': {e}")
        return [], []
    finally:
        conn.close()


def delete_table(table_name):
    conn = connect_to_db(CURRENT_DB)
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        conn.commit()
        messagebox.showinfo("Éxito", f"Tabla '{table_name}' eliminada correctamente.")
        refresh_tables()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"No se pudo eliminar la tabla '{table_name}': {e}")
    finally:
        conn.close()


def delete_row(table_name, row_id, primary_key):
    conn = connect_to_db(CURRENT_DB)
    if not conn:
        return
    cursor = conn.cursor()
    try:
        query = f"DELETE FROM {table_name} WHERE {primary_key} = ?"
        cursor.execute(query, (row_id,))
        conn.commit()
        messagebox.showinfo("Éxito", "Fila eliminada correctamente.")
        view_table_data()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"No se pudo eliminar la fila: {e}")
    finally:
        conn.close()


def truncate_table(table_name):
    conn = connect_to_db(CURRENT_DB)
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM {table_name}")
        conn.commit()
        messagebox.showinfo("Éxito", f"Tabla '{table_name}' vaciada correctamente.")
        view_table_data()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"No se pudo vaciar la tabla '{table_name}': {e}")
    finally:
        conn.close()


# Interfaz gráfica
def switch_database(selected_db):
    global CURRENT_DB
    CURRENT_DB = selected_db
    messagebox.showinfo("Base de Datos Cambiada", f"Base de datos activa: {CURRENT_DB}")
    refresh_tables()


def refresh_tables():
    tables = get_tables()
    table_listbox.delete(0, tk.END)
    for table in tables:
        table_listbox.insert(tk.END, table)


def view_table_data():
    selected_table = table_listbox.get(tk.ACTIVE)
    if not selected_table:
        messagebox.showwarning("Advertencia", "Seleccione una tabla primero.")
        return
    columns, rows = get_table_data(selected_table)
    if not columns:
        return

    # Limpiar el árbol y añadir nuevas columnas
    table_view.delete(*table_view.get_children())
    table_view["columns"] = columns
    for col in columns:
        table_view.heading(col, text=col)
        table_view.column(col, anchor=tk.W)

    # Añadir filas
    for row in rows:
        table_view.insert("", tk.END, values=row)


def add_record():
    selected_table = table_listbox.get(tk.ACTIVE)
    if not selected_table:
        messagebox.showwarning("Advertencia", "Seleccione una tabla primero.")
        return

    columns, _ = get_table_data(selected_table)
    if not columns:
        return

    def save_record():
        values = [entry.get() for entry in entry_widgets]
        insert_data(selected_table, columns, values)
        add_window.destroy()
        view_table_data()

    add_window = tk.Toplevel()
    add_window.title(f"Añadir Registro a {selected_table}")
    add_window.geometry("400x300")

    entry_widgets = []
    for idx, col in enumerate(columns):
        tk.Label(add_window, text=col).grid(row=idx, column=0, padx=5, pady=5)
        entry = tk.Entry(add_window)
        entry.grid(row=idx, column=1, padx=5, pady=5)
        entry_widgets.append(entry)

    tk.Button(add_window, text="Guardar", command=save_record).grid(row=len(columns), column=0, columnspan=2, pady=10)


def delete_selected_table():
    selected_table = table_listbox.get(tk.ACTIVE)
    if not selected_table:
        messagebox.showwarning("Advertencia", "Seleccione una tabla primero.")
        return
    confirm = messagebox.askyesno("Confirmar", f"¿Está seguro de que desea eliminar la tabla '{selected_table}'?")
    if confirm:
        delete_table(selected_table)


def delete_selected_row():
    selected_table = table_listbox.get(tk.ACTIVE)
    if not selected_table:
        messagebox.showwarning("Advertencia", "Seleccione una tabla primero.")
        return
    selected_item = table_view.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione una fila primero.")
        return
    row_values = table_view.item(selected_item, "values")
    columns, _ = get_table_data(selected_table)
    primary_key = columns[0]
    row_id = row_values[0]

    confirm = messagebox.askyesno("Confirmar", f"¿Está seguro de que desea eliminar la fila con {primary_key} = {row_id}?")
    if confirm:
        delete_row(selected_table, row_id, primary_key)


def truncate_selected_table():
    selected_table = table_listbox.get(tk.ACTIVE)
    if not selected_table:
        messagebox.showwarning("Advertencia", "Seleccione una tabla primero.")
        return
    confirm = messagebox.askyesno("Confirmar", f"¿Está seguro de que desea vaciar la tabla '{selected_table}'?")
    if confirm:
        truncate_table(selected_table)


# Ventana principal
root = tk.Tk()
root.title("Gestor de Base de Datos")
root.geometry("1000x700")

style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="#f5f5f5")
style.configure("TButton", background="#4285f4", foreground="white", font=("Arial", 12), padding=5)
style.configure("TLabel", background="#f5f5f5", foreground="#333", font=("Arial", 11))

# Selector de base de datos
db_frame = ttk.Frame(root)
db_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)

ttk.Label(db_frame, text="Seleccionar Base de Datos:").pack(side=tk.LEFT, padx=5)
db_selector = ttk.Combobox(db_frame, values=DBS, state="readonly", font=("Arial", 11))
db_selector.set(CURRENT_DB)
db_selector.pack(side=tk.LEFT, padx=10)
db_selector.bind("<<ComboboxSelected>>", lambda e: switch_database(db_selector.get()))

# Lista de tablas
left_frame = ttk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=10)

ttk.Label(left_frame, text="Tablas:").pack(anchor=tk.W, pady=5)
table_listbox = tk.Listbox(left_frame, height=15, font=("Arial", 11), selectmode=tk.SINGLE)
table_listbox.pack(fill=tk.BOTH, expand=True, pady=5)

ttk.Button(left_frame, text="Actualizar Tablas", command=refresh_tables).pack(pady=5)
ttk.Button(left_frame, text="Ver Datos de la Tabla", command=view_table_data).pack(pady=5)
ttk.Button(left_frame, text="Eliminar Tabla", command=delete_selected_table).pack(pady=5)
ttk.Button(left_frame, text="Vaciar Tabla", command=truncate_selected_table).pack(pady=5)

# Vista de datos
right_frame = ttk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=10)

table_view = ttk.Treeview(right_frame, show="headings")
table_view.pack(fill=tk.BOTH, expand=True)

# Operaciones CRUD
bottom_frame = ttk.Frame(root)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)

ttk.Button(bottom_frame, text="Añadir Registro", command=add_record).pack(side=tk.LEFT, padx=5)
ttk.Button(bottom_frame, text="Eliminar Fila", command=delete_selected_row).pack(side=tk.LEFT, padx=5)

refresh_tables()
root.mainloop()
