import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import sv_ttk
from rembg import remove
from PIL import Image, ImageTk
import io

def select_input_file():
    input_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")]
    )
    if input_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, input_path)
        show_image(input_path, input_image_label)

def select_output_file():
    output_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")]
    )
    if output_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output_path)

def remove_background():
    input_path = input_entry.get()
    output_path = output_entry.get()

    if not input_path or not output_path:
        messagebox.showerror("Error", "Por favor, selecciona las rutas de entrada y salida.")
        return

    try:
        with open(input_path, 'rb') as input_file:
            input_data = input_file.read()

        output_data = remove(input_data)

        with open(output_path, 'wb') as output_file:
            output_file.write(output_data)

        show_image(output_path, output_image_label)
        messagebox.showinfo("Éxito", "El fondo se eliminó correctamente.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_image(image_path, label):
    image = Image.open(image_path)
    # Ajustar el tamaño manteniendo la proporción original
    width, height = image.size
    if width > 300:
        new_width = 300
        new_height = int(height * (new_width / width))
        image = image.resize((new_width, new_height), Image.LANCZOS)
    elif height > 300:
        new_height = 300
        new_width = int(width * (new_height / height))
        image = image.resize((new_width, new_height), Image.LANCZOS)
    # Crear la imagen PhotoImage
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo

# Crear la ventana principal
root = tk.Tk()
root.title("Eliminador de Fondo de Imágenes")

# Aplicar el tema oscuro
sv_ttk.use_dark_theme()

# Crear los widgets
input_label = ttk.Label(root, text="Imagen de Entrada:")
input_entry = ttk.Entry(root, width=40)
input_button = ttk.Button(root, text="Seleccionar", command=select_input_file)

output_label = ttk.Label(root, text="Imagen de Salida:")
output_entry = ttk.Entry(root, width=40)
output_button = ttk.Button(root, text="Guardar Como", command=select_output_file)

process_button = ttk.Button(root, text="Eliminar Fondo", command=remove_background)

input_image_label = ttk.Label(root)
output_image_label = ttk.Label(root)

# Ubicar los widgets en la ventana
input_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
input_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
input_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

output_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
output_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
output_button.grid(row=1, column=2, padx=10, pady=10, sticky="e")

process_button.grid(row=2, column=0, columnspan=3, pady=10)

# Centrar imágenes
input_image_label.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
output_image_label.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

# Ajustar la columna
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# Ajustar la fila para centrar las imágenes verticalmente
root.grid_rowconfigure(3, weight=1)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
