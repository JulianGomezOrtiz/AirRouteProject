import networkx as nx
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GrafoAereo:
    def __init__(self):
        self.grafo = nx.Graph()
        self.contador_aeropuerto = 1

    def agregar_aeropuerto(self, aeropuerto, ubicacion):
        codigo_aeropuerto = self.contador_aeropuerto
        self.grafo.add_node(codigo_aeropuerto, nombre=aeropuerto, ubicacion=ubicacion)
        self.contador_aeropuerto += 1
        return codigo_aeropuerto

    def obtener_lista_aeropuertos(self):
        lista_aeropuertos = []
        for nodo, datos in self.grafo.nodes(data=True):
            info_aeropuerto = {
                'codigo': nodo,
                'nombre': datos.get('nombre', 'Sin nombre'),
                'ubicacion': datos.get('ubicacion', 'Sin ubicación')
            }
            lista_aeropuertos.append(info_aeropuerto)
        return lista_aeropuertos

    def agregar_ruta(self, origen, destino, distancia, tiempo_vuelo):
        self.grafo.add_edge(origen, destino,
                            distancia=distancia, tiempo_vuelo=tiempo_vuelo)

    def obtener_ruta_mas_corta(self, origen, destino):
        try:
            ruta = nx.dijkstra_path(
                self.grafo, origen, destino, weight='distancia')
            distancia = nx.dijkstra_path_length(
                self.grafo, origen, destino, weight='distancia')
            tiempo_vuelo = nx.dijkstra_path_length(
                self.grafo, origen, destino, weight='tiempo_vuelo')
            return ruta, distancia, tiempo_vuelo
        except nx.NetworkXNoPath:
            return None


class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gestión de Rutas Aéreas")
        self.geometry("1024x490")
        self.configure(bg="#212121")
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - \
            (width // 2)
        y = (self.winfo_screenheight() // 2) - \
            (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.grafo_aereo = GrafoAereo()
        self.crear_widgets()

        self.figura = plt.figure(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.figura, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def crear_widgets(self):
        # Título
        title_label = tk.Label(self, text="AEROPUERTOS Y RUTAS AÉREAS", bg="#212121", fg="#FFFFFF",
                               font=("Helvetica", 20, "bold"))
        title_label.pack(pady=10)

        # Botones en la ventana principal
        button_width = 20

        buttons_frame = tk.Frame(self, bg="#212121")  # Eliminación de marcos
        buttons_frame.pack()

        styles = {'background': '#424242', 'foreground': '#FFFFFF',
                  'highlightbackground': '#212121', 'highlightcolor': '#212121',
                  'borderwidth': 0, 'relief': 'flat', 'font': ('Helvetica', 10)}

        airport_button = tk.Button(buttons_frame, text="Registrar Aeropuerto", command=self.register_airport,
                                   width=button_width, **styles, padx=10, pady=5)  # Se eliminó 'bd=0'
        airport_button.pack(pady=5)

        route_button = tk.Button(buttons_frame, text="Crear Ruta", command=self.create_route,
                                 width=button_width, **styles, bd=0, padx=10, pady=5)
        route_button.pack(pady=5)

        edit_button = tk.Button(buttons_frame, text="Editar Ruta", command=self.edit_route,
                                width=button_width, **styles, bd=0, padx=10, pady=5)
        edit_button.pack(pady=5)

        visualize_button = tk.Button(buttons_frame, text="Visualizar Rutas", command=self.visualize_routes,
                                     width=button_width, **styles, bd=0, padx=10, pady=5)
        visualize_button.pack(pady=5)

        airports_button = tk.Button(buttons_frame, text="Lista de Aeropuertos", command=self.display_airports,
                                    width=button_width, **styles, bd=0, padx=10, pady=5)
        airports_button.pack(pady=5)

        # BÚSQUEDA DE RUTAS
        title_label = tk.Label(self, text="BÚSQUEDA DE RUTAS", bg="#212121", fg="#FFFFFF",
                               font=("Helvetica", 20, "bold"))
        title_label.pack(pady=10)

        search_frame = tk.Frame(self, bg="#212121")
        search_frame.pack()

        label_width = 20

        origin_label = tk.Label(search_frame, text="Aeropuerto de Origen",
                                width=label_width, bg="#212121", fg="#FFFFFF")
        origin_label.pack(pady=5)
        self.origin_entry = tk.Entry(
            search_frame, bg="#424242", fg="#FFFFFF", bd=0)
        self.origin_entry.pack()

        destination_label = tk.Label(
            search_frame, text="Aeropuerto de Destino", width=label_width, bg="#212121", fg="#FFFFFF")
        destination_label.pack(pady=10)
        self.destination_entry = tk.Entry(
            search_frame, bg="#424242", fg="#FFFFFF", bd=0)
        self.destination_entry.pack()

        search_button = tk.Button(search_frame, text="Buscar Ruta", command=self.search_route,
                                  **styles, bd=0, padx=10, pady=5)
        search_button.pack(pady=10)

    def set_window_properties(self, window, title):
        window.title(title)
        window.configure(bg="#212121")
        window.tk_setPalette(background="#212121", foreground="#FFFFFF")
        window.geometry("350x150")  # Tamaño adecuado para la ventana
        # Actualizar para obtener el tamaño correcto después de configurar el contenido
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - \
            (width // 2)  # Centrar horizontalmente
        y = (window.winfo_screenheight() // 2) - \
            (height // 2)  # Centrar verticalmente
        # Establecer la geometría centrada
        window.geometry(f"{width}x{height}+{x}+{y}")

    def register_airport(self):
        # Crear una nueva ventana superior para registrar aeropuertos con el mismo diseño
        register_window = tk.Toplevel(self)
        # Configurar propiedades de la ventana emergente
        self.set_window_properties(register_window, "Registrar Aeropuerto")
        # Modo oscuro para la ventana emergente
        register_window.configure(bg="#212121")

        self.create_input_field(register_window, "Nombre:", "name_entry")
        self.create_input_field(
            register_window, "Ubicación:", "location_entry")

        save_button = tk.Button(
            register_window, text="Guardar", command=self.save_airport)
        save_button.pack()

    def create_input_field(self, window, label_text, entry_name):
        # Crear una etiqueta con el texto proporcionado y agregarla a la ventana
        label = tk.Label(window, text=label_text, bg="#212121", fg="#FFFFFF")
        label.pack()

        # Crear un campo de entrada utilizando ttk.Entry y agregarlo a la ventana
        # Definir el estilo para la entrada
        entry = ttk.Entry(window, style="Dark.TEntry")
        entry.pack()

        # Establecer el atributo de la instancia con el nombre proporcionado para referenciar el campo de entrada
        setattr(self, entry_name, entry)

        # Aplicar el estilo de la entrada
        # Cambiar la paleta de colores
        window.tk_setPalette(background="#212121", foreground="#FFFFFF")
        style = ttk.Style()
        style.theme_use('alt')  # Usar otro tema para Entry
        style.configure("Dark.TEntry", fieldbackground="#424242",
                        foreground="#FFFFFF", bordercolor="#424242")

    def save_airport(self):
        name = self.name_entry.get()
        location = self.location_entry.get()

        if name and location:
            if not any('name' in node_data and node_data['name'] == name for _, node_data in self.graph.graph.nodes(data=True)):
                airport_code = self.graph.add_airport(name, location)
                messagebox.showinfo(
                    "Aeropuerto registrado", f"Aeropuerto '{name}' registrado exitosamente con código {airport_code}.")
                self.update_graph()
                self.name_entry.delete(0, tk.END)
                self.location_entry.delete(0, tk.END)
            else:
                messagebox.showerror(
                    "Error", "Ya existe un aeropuerto con este nombre.")
        else:
            messagebox.showerror("Error", "Todos los campos son requeridos.")

    def create_route(self):
        create_route_window = tk.Toplevel(self)
        self.set_window_properties(create_route_window, "Crear ruta")  # Configurar propiedades de la ventana emergente

        source_label = tk.Label(create_route_window,
                                text="Código de Aeropuerto de Origen:")
        source_entry = tk.Entry(create_route_window)
        source_label.pack()
        source_entry.pack()

        destination_label = tk.Label(
            create_route_window, text="Código de Aeropuerto de Destino:")
        destination_entry = tk.Entry(create_route_window)
        destination_label.pack()
        destination_entry.pack()

        distance_label = tk.Label(create_route_window, text="Distancia:")
        distance_entry = tk.Entry(create_route_window)
        distance_label.pack()
        distance_entry.pack()

        flight_time_label = tk.Label(
            create_route_window, text="Tiempo de vuelo:")
        flight_time_entry = tk.Entry(create_route_window)
        flight_time_label.pack()
        flight_time_entry.pack()

        save_button = tk.Button(create_route_window, text="Guardar",
                                command=lambda: self.save_route(source_entry.get(),
                                                                destination_entry.get(),
                                                                distance_entry.get(),
                                                                flight_time_entry.get(),
                                                                create_route_window))
        save_button.pack()

    def save_route(self, source_code, destination_code, distance, flight_time, window):
        try:
            source_code = int(source_code)
            destination_code = int(destination_code)
            self.graph.add_route(source_code, destination_code, float(
                distance), float(flight_time))
            messagebox.showinfo("Ruta creada", "Ruta creada exitosamente.")
            window.destroy()
        except ValueError:
            messagebox.showerror(
                "Error", "Códigos de aeropuerto, distancia y tiempo de vuelo deben ser números válidos.")
        except nx.NodeNotFound:
            messagebox.showerror(
                "Error", "Aeropuerto no encontrado. Por favor, registra los aeropuertos primero.")

    def edit_route(self):
        edit_route_window = tk.Toplevel(self)
        self.set_window_properties(edit_route_window, "Editar ruta")  # Configurar propiedades de la ventana emergente

        source_label = tk.Label(
            edit_route_window, text="Aeropuerto de Origen:")
        source_entry = tk.Entry(edit_route_window)
        source_label.pack()
        source_entry.pack()

        destination_label = tk.Label(
            edit_route_window, text="Aeropuerto de Destino:")
        destination_entry = tk.Entry(edit_route_window)
        destination_label.pack()
        destination_entry.pack()

        distance_label = tk.Label(edit_route_window, text="Nueva Distancia:")
        distance_entry = tk.Entry(edit_route_window)
        distance_label.pack()
        distance_entry.pack()

        flight_time_label = tk.Label(
            edit_route_window, text="Nuevo Tiempo de Vuelo:")
        flight_time_entry = tk.Entry(edit_route_window)
        flight_time_label.pack()
        flight_time_entry.pack()

        save_button = tk.Button(edit_route_window, text="Guardar",
                                command=lambda: self.update_route(source_entry.get(), destination_entry.get(),
                                                                  distance_entry.get(), flight_time_entry.get(),
                                                                  edit_route_window))
        save_button.pack()

    def visualize_routes(self):
        graph_window = tk.Toplevel(self)
        graph_window.title("Lista de Aeropuertos")

        # Establecer el modo oscuro para la ventana emergente
        graph_window.configure(bg="#212121")

        figure = plt.figure(figsize=(10, 6))
        canvas = FigureCanvasTkAgg(figure, master=graph_window)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        node_labels = {
            node: self.graph.graph.nodes[node]['name'] for node in self.graph.graph.nodes}

        pos = nx.spring_layout(self.graph.graph)
        nx.draw(self.graph.graph, pos, with_labels=True, labels=node_labels,
                node_color='#424242', node_size=800)  # Cambio de color del nodo
        labels = nx.get_edge_attributes(self.graph.graph, 'distance')
        # Cambio de color de las etiquetas de las rutas
        nx.draw_networkx_edge_labels(
            self.graph.graph, pos, edge_labels=labels, font_color='white')

        canvas.draw()

        # Cambiar la paleta de colores
        graph_window.tk_setPalette(background="#212121", foreground="#FFFFFF")

    def update_graph(self):
        self.figure.clear()
        pos = nx.spring_layout(self.graph.graph)
        nx.draw(self.graph.graph, pos, with_labels=True,
                node_color='skyblue', node_size=800)
        labels = nx.get_edge_attributes(self.graph.graph, 'distance')
        nx.draw_networkx_edge_labels(self.graph.graph, pos, edge_labels=labels)
        self.canvas.draw()

    def update_route(self, source, destination, distance, flight_time, window):
        if source and destination and distance and flight_time:
            try:
                source = int(source)
                destination = int(destination)

                if self.graph.graph.has_edge(source, destination):
                    self.graph.graph[source][destination]['distance'] = float(
                        distance)
                    self.graph.graph[source][destination]['flight_time'] = float(
                        flight_time)
                    self.update_graph()  # Asegúrate de llamar correctamente al método update_graph
                    messagebox.showinfo("Ruta actualizada",
                                        "Ruta actualizada exitosamente.")
                    window.destroy()
                else:
                    messagebox.showerror(
                        "Error", "La ruta especificada no existe.")
            except ValueError:
                messagebox.showerror(
                    "Error", "Códigos de aeropuerto deben ser números válidos.")
        else:
            messagebox.showerror("Error", "Todos los campos son requeridos.")

    def search_route(self):
        # Obtener referencias a las entradas de origen y destino
        origin_entry = self.origin_entry
        destination_entry = self.destination_entry

        # Verificar si las entradas están en la ventana principal o en una ventana secundaria
        if not self.origin_entry.winfo_ismapped():
            # Si no están mapeadas, buscar en la ventana secundaria
            origin_entry = self.origin_entry.in_toplevel()
            destination_entry = self.destination_entry.in_toplevel()

        # Verificar si la ventana secundaria aún existe
        if origin_entry.winfo_exists() and destination_entry.winfo_exists():
            origin_code = origin_entry.get()
            destination_code = destination_entry.get()

            if origin_code and destination_code:
                try:
                    origin_code = int(origin_code)
                    destination_code = int(destination_code)
                    result = self.graph.get_shortest_path(
                        origin_code, destination_code)
                    if result:
                        path, distance, flight_time = result
                        airport_names = [
                            self.graph.graph.nodes[node]['name'] for node in path]
                        messagebox.showinfo("Ruta encontrada", f"Ruta encontrada:\n\n"
                                            f"Ruta: {' -> '.join(map(str, airport_names))}\n"
                                            f"Distancia: {distance} km\n"
                                            f"Tiempo de vuelo: {flight_time} horas")
                    else:
                        messagebox.showerror(
                            "Error", "No se encontró una ruta entre los aeropuertos especificados.")
                except ValueError:
                    messagebox.showerror(
                        "Error", "Códigos de aeropuerto deben ser números válidos.")
            else:
                messagebox.showerror(
                    "Error", "Todos los campos son requeridos.")
        else:
            messagebox.showerror(
                "Error", "La ventana de edición de rutas ha sido cerrada.")

    def display_airports(self):
        airports_list = self.graph.get_airports_list()
        airports_window = tk.Toplevel(self)
        self.set_window_properties(airports_list, "Registrar Aeropuerto")  # Configurar propiedades de la ventana emergente
        # Establecer el modo oscuro para la ventana emergente
        airports_window.configure(bg="#212121")

        frame = tk.Frame(airports_window, bg="#212121")
        frame.pack()

        for airport in airports_list:
            airport_info = f"Código: {airport['code']}, Nombre: {airport['name']}, Ubicación: {airport['location']}"
            airport_label = tk.Label(
                frame, text=airport_info, bg="#212121", fg="#FFFFFF")
            airport_label.pack()

        # Cambiar la paleta de colores
        airports_window.tk_setPalette(
            background="#212121", foreground="#FFFFFF")


if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
