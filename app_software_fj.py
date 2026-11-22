"""
Software FJ - Interfaz gráfica (Tkinter)
Aplicación de escritorio estilo software empresarial.

Requiere:
- software_fj.py (motor de lógica de la Fase 4)
- Python con Tkinter disponible

Ejecutar con el intérprete de VS Code:
    python app_software_fj.py
"""

import tkinter as tk
from tkinter import ttk, messagebox

from software_fj import (
    GestorSoftwareFJ, Cliente, ReservaSala, AlquilerEquipo,
    AsesoriaEspecializada, ErrorSistema
)


class SoftwareFJApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Software FJ | Gestión integral")
        self.geometry("1120x720")
        self.minsize(950, 620)
        self.configure(bg="#F3F6FA")

        self.gestor = GestorSoftwareFJ()
        self._estilo()
        self._crear_layout()
        self._mostrar_dashboard()

    def _estilo(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", rowheight=30, font=("Segoe UI", 10),
                        background="white", fieldbackground="white")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("TCombobox", padding=5)
        style.configure("TEntry", padding=6)
        style.configure("TButton", font=("Segoe UI", 10), padding=7)

    def _crear_layout(self):
        # Barra superior
        header = tk.Frame(self, bg="#FFFFFF", height=66)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="Software FJ", bg="white", fg="#1D3557",
                 font=("Segoe UI", 19, "bold")).pack(side="left", padx=24)
        tk.Label(header, text="Sistema integral de clientes, servicios y reservas",
                 bg="white", fg="#64748B", font=("Segoe UI", 10)).pack(side="left", padx=8)

        # Menú lateral
        body = tk.Frame(self, bg="#F3F6FA")
        body.pack(fill="both", expand=True)
        sidebar = tk.Frame(body, bg="#1D3557", width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        tk.Label(sidebar, text="MENÚ PRINCIPAL", bg="#1D3557", fg="#B7C8DC",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=20, pady=(22, 10))

        for label, callback in [
            ("Dashboard", self._mostrar_dashboard),
            ("Clientes", self._mostrar_clientes),
            ("Servicios", self._mostrar_servicios),
            ("Reservas", self._mostrar_reservas),
            ("Logs", self._mostrar_logs),
        ]:
            tk.Button(sidebar, text=label, command=callback, anchor="w",
                      bg="#1D3557", fg="white", activebackground="#2E527A",
                      activeforeground="white", relief="flat", bd=0,
                      font=("Segoe UI", 11), padx=20, pady=12,
                      cursor="hand2").pack(fill="x", padx=8, pady=2)

        self.content = tk.Frame(body, bg="#F3F6FA")
        self.content.pack(side="left", fill="both", expand=True, padx=24, pady=22)

    def _limpiar(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def _titulo(self, titulo, subtitulo=""):
        tk.Label(self.content, text=titulo, bg="#F3F6FA", fg="#1D3557",
                 font=("Segoe UI", 22, "bold")).pack(anchor="w")
        if subtitulo:
            tk.Label(self.content, text=subtitulo, bg="#F3F6FA", fg="#64748B",
                     font=("Segoe UI", 10)).pack(anchor="w", pady=(3, 16))

    def _tarjeta(self, parent, titulo, valor, color="#1D3557"):
        frame = tk.Frame(parent, bg="white", highlightbackground="#E2E8F0",
                        highlightthickness=1)
        frame.pack(side="left", fill="x", expand=True, padx=6)
        tk.Label(frame, text=titulo, bg="white", fg="#64748B",
                 font=("Segoe UI", 10)).pack(anchor="w", padx=16, pady=(14, 4))
        tk.Label(frame, text=str(valor), bg="white", fg=color,
                 font=("Segoe UI", 22, "bold")).pack(anchor="w", padx=16, pady=(0, 14))
        return frame

    def _mostrar_dashboard(self):
        self._limpiar()
        self._titulo("Dashboard", "Resumen de la operación de Software FJ")
        cards = tk.Frame(self.content, bg="#F3F6FA")
        cards.pack(fill="x", pady=8)
        self._tarjeta(cards, "Clientes registrados", len(self.gestor.clientes))
        self._tarjeta(cards, "Servicios disponibles", sum(1 for s in self.gestor.servicios if s.disponible), "#16804A")
        self._tarjeta(cards, "Reservas registradas", len(self.gestor.reservas), "#2563EB")

        panel = tk.Frame(self.content, bg="white", highlightbackground="#E2E8F0",
                         highlightthickness=1)
        panel.pack(fill="both", expand=True, pady=(18, 0))
        tk.Label(panel, text="Bienvenido al sistema", bg="white", fg="#1D3557",
                 font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=20, pady=(20, 6))
        tk.Label(panel, text=("Utiliza el menú lateral para administrar clientes, crear servicios, "
                              "registrar reservas y consultar los eventos del sistema."),
                 bg="white", fg="#475569", font=("Segoe UI", 11),
                 wraplength=650, justify="left").pack(anchor="w", padx=20)
        tk.Label(panel, text="Flujo recomendado: registrar cliente → registrar servicio → crear reserva → confirmar → procesar.",
                 bg="white", fg="#2563EB", font=("Segoe UI", 10, "bold"),
                 wraplength=700, justify="left").pack(anchor="w", padx=20, pady=18)

    def _mostrar_clientes(self):
        self._limpiar()
        self._titulo("Clientes", "Registrar y consultar clientes")

        form = tk.Frame(self.content, bg="white", highlightbackground="#E2E8F0",
                        highlightthickness=1)
        form.pack(fill="x", pady=(0, 16))
        fields = [("Identificación", "id"), ("Nombre", "nombre"),
                  ("Correo", "correo"), ("Teléfono", "telefono")]
        self.client_vars = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(form, text=label, bg="white", fg="#475569",
                     font=("Segoe UI", 9, "bold")).grid(row=0, column=i, padx=10, pady=(12, 4), sticky="w")
            var = tk.StringVar()
            self.client_vars[key] = var
            ttk.Entry(form, textvariable=var, width=24).grid(row=1, column=i, padx=10, pady=(0, 12), sticky="ew")
            form.grid_columnconfigure(i, weight=1)
        tk.Button(form, text="Registrar cliente", bg="#2563EB", fg="white",
                  activebackground="#1D4ED8", relief="flat", font=("Segoe UI", 10, "bold"),
                  command=self._registrar_cliente).grid(row=2, column=0, columnspan=4, padx=10, pady=(0, 12), sticky="ew")

        table_frame = tk.Frame(self.content, bg="white")
        table_frame.pack(fill="both", expand=True)
        cols = ("id", "nombre", "correo", "telefono")
        self.client_tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for col, text, width in zip(cols, ("Identificación", "Nombre", "Correo", "Teléfono"), (130, 220, 280, 160)):
            self.client_tree.heading(col, text=text)
            self.client_tree.column(col, width=width)
        self.client_tree.pack(fill="both", expand=True)
        self._refrescar_clientes()

    def _registrar_cliente(self):
        try:
            v = self.client_vars
            cliente = Cliente(v["id"].get(), v["nombre"].get(), v["correo"].get(), v["telefono"].get())
            self.gestor.registrar_cliente(cliente)
        except ErrorSistema as e:
            messagebox.showerror("No se pudo registrar", str(e))
            return
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
        for var in self.client_vars.values():
            var.set("")
        self._refrescar_clientes()

    def _refrescar_clientes(self):
        if not hasattr(self, "client_tree"):
            return
        for row in self.client_tree.get_children():
            self.client_tree.delete(row)
        for c in self.gestor.clientes:
            self.client_tree.insert("", "end", values=(c.identificador, c.nombre, c.correo, c.telefono))

    def _mostrar_servicios(self):
        self._limpiar()
        self._titulo("Servicios", "Crear salas, alquileres de equipo y asesorías")
        form = tk.Frame(self.content, bg="white", highlightbackground="#E2E8F0",
                        highlightthickness=1)
        form.pack(fill="x", pady=(0, 14))

        self.sv_type = tk.StringVar(value="Sala")
        self.sv_id = tk.StringVar()
        self.sv_name = tk.StringVar()
        self.sv_price = tk.StringVar()
        self.sv_extra = tk.StringVar()

        labels = ["Tipo", "ID", "Nombre", "Tarifa base", "Capacidad / Tipo equipo / Especialidad"]
        for i, label in enumerate(labels):
            tk.Label(form, text=label, bg="white", fg="#475569",
                     font=("Segoe UI", 9, "bold")).grid(row=0, column=i, padx=8, pady=(12, 4), sticky="w")
        ttk.Combobox(form, textvariable=self.sv_type, values=("Sala", "Equipo", "Asesoría"),
                     state="readonly", width=15).grid(row=1, column=0, padx=8, pady=(0, 12), sticky="ew")
        ttk.Entry(form, textvariable=self.sv_id, width=12).grid(row=1, column=1, padx=8, pady=(0, 12), sticky="ew")
        ttk.Entry(form, textvariable=self.sv_name, width=18).grid(row=1, column=2, padx=8, pady=(0, 12), sticky="ew")
        ttk.Entry(form, textvariable=self.sv_price, width=15).grid(row=1, column=3, padx=8, pady=(0, 12), sticky="ew")
        ttk.Entry(form, textvariable=self.sv_extra, width=28).grid(row=1, column=4, padx=8, pady=(0, 12), sticky="ew")
        for i in range(5):
            form.grid_columnconfigure(i, weight=1)
        tk.Button(form, text="Crear servicio", bg="#2563EB", fg="white", relief="flat",
                  font=("Segoe UI", 10, "bold"), command=self._registrar_servicio).grid(
                  row=2, column=0, columnspan=5, padx=8, pady=(0, 12), sticky="ew")

        self.service_tree = ttk.Treeview(self.content, columns=("id", "name", "type", "price", "available"),
                                         show="headings")
        for col, title, width in zip(("id", "name", "type", "price", "available"),
                                     ("ID", "Nombre", "Tipo", "Tarifa", "Disponible"),
                                     (100, 240, 170, 140, 120)):
            self.service_tree.heading(col, text=title)
            self.service_tree.column(col, width=width)
        self.service_tree.pack(fill="both", expand=True)
        self._refrescar_servicios()

    def _registrar_servicio(self):
        try:
            ident = self.sv_id.get().strip()
            name = self.sv_name.get().strip()
            price = float(self.sv_price.get())
            extra = self.sv_extra.get().strip()
            tipo = self.sv_type.get()
            if tipo == "Sala":
                servicio = ReservaSala(ident, name, price, int(extra))
            elif tipo == "Equipo":
                servicio = AlquilerEquipo(ident, name, price, extra)
            else:
                servicio = AsesoriaEspecializada(ident, name, price, extra)
            self.gestor.registrar_servicio(servicio)
        except (ValueError, ErrorSistema) as e:
            messagebox.showerror("No se pudo crear el servicio", str(e))
            return
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        messagebox.showinfo("Éxito", "Servicio creado correctamente.")
        for var in (self.sv_id, self.sv_name, self.sv_price, self.sv_extra):
            var.set("")
        self._refrescar_servicios()

    def _refrescar_servicios(self):
        if not hasattr(self, "service_tree"):
            return
        for row in self.service_tree.get_children():
            self.service_tree.delete(row)
        for s in self.gestor.servicios:
            tipo = s.__class__.__name__
            self.service_tree.insert("", "end", values=(s.identificador, s.nombre, tipo,
                                                       f"${s.tarifa_base:,.2f}", "Sí" if s.disponible else "No"))

    def _mostrar_reservas(self):
        self._limpiar()
        self._titulo("Reservas", "Crear, confirmar, cancelar y procesar reservas")
        form = tk.Frame(self.content, bg="white", highlightbackground="#E2E8F0",
                        highlightthickness=1)
        form.pack(fill="x", pady=(0, 14))

        self.r_id = tk.StringVar()
        self.r_client = tk.StringVar()
        self.r_service = tk.StringVar()
        self.r_duration = tk.StringVar(value="1")
        self.r_tax = tk.StringVar(value="0.19")
        self.r_discount = tk.StringVar(value="0")

        items = [
            ("ID reserva", self.r_id, 0),
            ("Cliente", self.r_client, 1),
            ("Servicio", self.r_service, 2),
            ("Duración", self.r_duration, 3),
            ("Impuesto (ej. 0.19)", self.r_tax, 4),
            ("Descuento (ej. 0.10)", self.r_discount, 5),
        ]
        for label, var, col in items:
            tk.Label(form, text=label, bg="white", fg="#475569",
                     font=("Segoe UI", 9, "bold")).grid(row=0, column=col, padx=7, pady=(12, 4), sticky="w")
            if col == 1:
                combo = ttk.Combobox(form, textvariable=var, state="readonly", width=20,
                                    values=[f"{c.identificador} - {c.nombre}" for c in self.gestor.clientes])
                combo.grid(row=1, column=col, padx=7, pady=(0, 12), sticky="ew")
            elif col == 2:
                combo = ttk.Combobox(form, textvariable=var, state="readonly", width=20,
                                    values=[f"{s.identificador} - {s.nombre}" for s in self.gestor.servicios])
                combo.grid(row=1, column=col, padx=7, pady=(0, 12), sticky="ew")
            else:
                ttk.Entry(form, textvariable=var, width=18).grid(row=1, column=col, padx=7, pady=(0, 12), sticky="ew")
            form.grid_columnconfigure(col, weight=1)

        tk.Button(form, text="Crear reserva", bg="#2563EB", fg="white", relief="flat",
                  font=("Segoe UI", 10, "bold"), command=self._crear_reserva).grid(
                  row=2, column=0, columnspan=6, padx=7, pady=(0, 12), sticky="ew")

        actions = tk.Frame(self.content, bg="#F3F6FA")
        actions.pack(fill="x", pady=(0, 10))
        tk.Button(actions, text="Confirmar seleccionada", command=lambda: self._accion_reserva("confirmar"),
                  bg="#16804A", fg="white", relief="flat").pack(side="left", padx=(0, 8))
        tk.Button(actions, text="Cancelar seleccionada", command=lambda: self._accion_reserva("cancelar"),
                  bg="#B45309", fg="white", relief="flat").pack(side="left", padx=8)
        tk.Button(actions, text="Procesar seleccionada", command=lambda: self._accion_reserva("procesar"),
                  bg="#2563EB", fg="white", relief="flat").pack(side="left", padx=8)

        self.res_tree = ttk.Treeview(self.content, columns=("id", "client", "service", "duration", "state", "total"),
                                     show="headings")
        for col, title, width in zip(("id", "client", "service", "duration", "state", "total"),
                                     ("ID", "Cliente", "Servicio", "Duración", "Estado", "Total calculado"),
                                     (90, 170, 210, 90, 120, 150)):
            self.res_tree.heading(col, text=title)
            self.res_tree.column(col, width=width)
        self.res_tree.pack(fill="both", expand=True)
        self._refrescar_reservas()

    def _crear_reserva(self):
        try:
            cliente_id = self.r_client.get().split(" - ")[0]
            servicio_id = self.r_service.get().split(" - ")[0]
            reserva = self.gestor.crear_reserva(
                self.r_id.get().strip(), cliente_id, servicio_id,
                float(self.r_duration.get()), float(self.r_tax.get()), float(self.r_discount.get())
            )
        except (ValueError, ErrorSistema) as e:
            messagebox.showerror("No se pudo crear la reserva", str(e))
            return
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        messagebox.showinfo("Éxito", f"Reserva {reserva.identificador} creada. Estado: {reserva.estado}")
        self._refrescar_reservas()

    def _accion_reserva(self, accion):
        selection = self.res_tree.selection()
        if not selection:
            messagebox.showwarning("Selecciona una reserva", "Selecciona una fila de la tabla primero.")
            return
        reserva_id = self.res_tree.item(selection[0], "values")[0]
        reserva = next((r for r in self.gestor.reservas if r.identificador == reserva_id), None)
        if reserva is None:
            return
        try:
            if accion == "confirmar":
                mensaje = reserva.confirmar()
            elif accion == "cancelar":
                mensaje = reserva.cancelar()
            else:
                total = reserva.procesar()
                mensaje = f"Reserva procesada. Total: ${total:,.2f}"
            messagebox.showinfo("Operación completada", mensaje)
        except ErrorSistema as e:
            messagebox.showerror("Operación no permitida", str(e))
        self._refrescar_reservas()

    def _refrescar_reservas(self):
        if not hasattr(self, "res_tree"):
            return
        for row in self.res_tree.get_children():
            self.res_tree.delete(row)
        for r in self.gestor.reservas:
            total = ""
            if r.estado == "Procesada":
                try:
                    total = f"${r.servicio.calcular_costo(r.duracion, r.impuesto, r.descuento):,.2f}"
                except Exception:
                    total = "N/D"
            self.res_tree.insert("", "end", values=(r.identificador, r.cliente.nombre,
                                                   r.servicio.nombre, r.duracion, r.estado, total))

    def _mostrar_logs(self):
        self._limpiar()
        self._titulo("Logs", "Eventos y errores registrados por el sistema")
        log_path = "software_fj.log"
        box = tk.Text(self.content, wrap="word", font=("Consolas", 10), bg="white",
                      fg="#334155", relief="flat")
        box.pack(fill="both", expand=True)
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                box.insert("1.0", f.read())
        except FileNotFoundError:
            box.insert("1.0", "Aún no existe el archivo de log. Realiza operaciones para generarlo.")
        box.configure(state="disabled")


if __name__ == "__main__":
    app = SoftwareFJApp()
    app.mainloop()
