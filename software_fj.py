"""
Software FJ - Sistema Integral de Gestión de Clientes, Servicios y Reservas
Fase 4 - Programación (UNAD)

Requisitos: Python 3.10+ (no requiere librerías externas).
Ejecución: python software_fj.py

No utiliza bases de datos. Mantiene información en listas en memoria y registra
eventos/errores en software_fj.log.
"""

from abc import ABC, abstractmethod
from datetime import datetime
import logging
import re
from typing import List, Optional


# ============================= LOGGING =========================================
logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)
logger = logging.getLogger("SoftwareFJ")


# ======================== EXCEPCIONES PERSONALIZADAS ===========================
class ErrorSistema(Exception):
    """Excepción base para errores controlados del sistema."""


class ValidacionError(ErrorSistema):
    """Datos que no cumplen las validaciones."""


class ServicioNoDisponibleError(ErrorSistema):
    """Servicio no disponible para ser reservado."""


class ReservaError(ErrorSistema):
    """Operación de reserva inválida."""


class ClienteNoEncontradoError(ErrorSistema):
    """Cliente no encontrado en la lista interna."""


# ============================= ENTIDAD ========================================
class Entidad(ABC):
    """Clase abstracta general para entidades del sistema."""

    def __init__(self, identificador: str):
        if not identificador or not str(identificador).strip():
            raise ValidacionError("El identificador no puede estar vacío.")
        self._identificador = str(identificador).strip()

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def mostrar_informacion(self) -> str:
        """Cada entidad concreta debe definir cómo mostrar sus datos."""


# ============================== CLIENTE =======================================
class Cliente(Entidad):
    def __init__(self, identificador: str, nombre: str, correo: str, telefono: str):
        super().__init__(identificador)
        self.__nombre = self._validar_nombre(nombre)
        self.__correo = self._validar_correo(correo)
        self.__telefono = self._validar_telefono(telefono)

    @staticmethod
    def _validar_nombre(nombre: str) -> str:
        if not isinstance(nombre, str) or len(nombre.strip()) < 2:
            raise ValidacionError("El nombre debe tener mínimo 2 caracteres.")
        return nombre.strip()

    @staticmethod
    def _validar_correo(correo: str) -> str:
        if not isinstance(correo, str) or not re.match(
            r"^[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}$", correo.strip()
        ):
            raise ValidacionError("El correo electrónico no tiene un formato válido.")
        return correo.strip().lower()

    @staticmethod
    def _validar_telefono(telefono: str) -> str:
        limpio = re.sub(r"\D", "", str(telefono))
        if len(limpio) < 7 or len(limpio) > 15:
            raise ValidacionError("El teléfono debe contener entre 7 y 15 dígitos.")
        return limpio

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, nuevo_telefono):
        self.__telefono = self._validar_telefono(nuevo_telefono)

    def mostrar_informacion(self) -> str:
        return (
            f"Cliente ID: {self.identificador} | Nombre: {self.nombre} | "
            f"Correo: {self.correo} | Teléfono: {self.telefono}"
        )


# =============================== SERVICIO =====================================
class Servicio(Entidad, ABC):
    def __init__(self, identificador: str, nombre: str, tarifa_base: float):
        super().__init__(identificador)
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValidacionError("El nombre del servicio es obligatorio.")
        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise ValidacionError("La tarifa base debe ser un valor positivo.")
        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = True

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, disponible: bool):
        if not isinstance(disponible, bool):
            raise ValidacionError("La disponibilidad debe ser True o False.")
        self._disponible = disponible

    # Sobrecarga simulada: distintos cálculos con parámetros opcionales.
    # calcular_costo(duracion)
    # calcular_costo(duracion, impuesto=0.19)
    # calcular_costo(duracion, impuesto=0.19, descuento=0.10)
    def calcular_costo(self, duracion: float = 1, impuesto: float = 0.0,
                       descuento: float = 0.0) -> float:
        self.validar_parametros(duracion)
        if not 0 <= impuesto <= 1:
            raise ValidacionError("El impuesto debe estar entre 0 y 1.")
        if not 0 <= descuento <= 1:
            raise ValidacionError("El descuento debe estar entre 0 y 1.")
        subtotal = self._tarifa_base * duracion
        subtotal_descuento = subtotal * (1 - descuento)
        return round(subtotal_descuento * (1 + impuesto), 2)

    @abstractmethod
    def validar_parametros(self, duracion: float):
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        pass

    def mostrar_informacion(self) -> str:
        return (
            f"Servicio ID: {self.identificador} | {self.nombre} | "
            f"Tarifa: ${self.tarifa_base:,.2f} | Disponible: {self.disponible}"
        )


class ReservaSala(Servicio):
    def __init__(self, identificador, nombre, tarifa_base, capacidad):
        super().__init__(identificador, nombre, tarifa_base)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ValidacionError("La capacidad de la sala debe ser un entero positivo.")
        self.capacidad = capacidad

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ValidacionError("La duración de la sala debe ser mayor que cero.")

    def describir_servicio(self):
        return f"Sala '{self.nombre}' para reuniones, capacidad de {self.capacidad} personas."


class AlquilerEquipo(Servicio):
    def __init__(self, identificador, nombre, tarifa_base, tipo_equipo):
        super().__init__(identificador, nombre, tarifa_base)
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise ValidacionError("Debe especificar el tipo de equipo.")
        self.tipo_equipo = tipo_equipo.strip()

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ValidacionError("La duración del alquiler debe ser mayor que cero.")

    def describir_servicio(self):
        return f"Alquiler de equipo: {self.tipo_equipo} ({self.nombre})."


class AsesoriaEspecializada(Servicio):
    def __init__(self, identificador, nombre, tarifa_base, especialidad):
        super().__init__(identificador, nombre, tarifa_base)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ValidacionError("Debe indicar la especialidad de la asesoría.")
        self.especialidad = especialidad.strip()

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ValidacionError("La duración de la asesoría debe ser mayor que cero.")
        if duracion > 8:
            raise ValidacionError("Una asesoría no puede superar 8 horas por reserva.")

    def describir_servicio(self):
        return f"Asesoría especializada en {self.especialidad}."


# ================================ RESERVA =====================================
class Reserva(Entidad):
    ESTADOS_VALIDOS = ("Pendiente", "Confirmada", "Cancelada", "Procesada")

    def __init__(self, identificador, cliente: Cliente, servicio: Servicio,
                 duracion: float, impuesto: float = 0.19, descuento: float = 0.0):
        super().__init__(identificador)
        if not isinstance(cliente, Cliente):
            raise ValidacionError("La reserva debe asociarse a un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ValidacionError("La reserva debe asociarse a un servicio válido.")
        servicio.validar_parametros(duracion)
        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{servicio.nombre}' no está disponible."
            )
        if not 0 <= impuesto <= 1 or not 0 <= descuento <= 1:
            raise ValidacionError("Impuesto o descuento fuera de rango.")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.impuesto = impuesto
        self.descuento = descuento
        self._estado = "Pendiente"
        self.fecha_creacion = datetime.now()

    @property
    def estado(self):
        return self._estado

    def confirmar(self):
        if self._estado != "Pendiente":
            raise ReservaError(f"No se puede confirmar una reserva en estado {self._estado}.")
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError("El servicio ya no está disponible.")
        self._estado = "Confirmada"
        logger.info("Reserva %s confirmada para cliente %s.", self.identificador,
                    self.cliente.identificador)
        return f"Reserva {self.identificador} confirmada."

    def cancelar(self):
        if self._estado in ("Cancelada", "Procesada"):
            raise ReservaError(f"No se puede cancelar una reserva en estado {self._estado}.")
        self._estado = "Cancelada"
        logger.info("Reserva %s cancelada.", self.identificador)
        return f"Reserva {self.identificador} cancelada."

    def procesar(self):
        if self._estado != "Confirmada":
            raise ReservaError("Solo se pueden procesar reservas confirmadas.")
        costo = self.servicio.calcular_costo(
            self.duracion, self.impuesto, self.descuento
        )
        self._estado = "Procesada"
        logger.info("Reserva %s procesada. Total: $%.2f.", self.identificador, costo)
        return costo

    def mostrar_informacion(self):
        return (
            f"Reserva {self.identificador} | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | Duración: {self.duracion} | "
            f"Estado: {self.estado}"
        )


# ============================= GESTOR =========================================
class GestorSoftwareFJ:
    """Controla listas internas de clientes, servicios y reservas."""

    def __init__(self):
        self.clientes: List[Cliente] = []
        self.servicios: List[Servicio] = []
        self.reservas: List[Reserva] = []

    def registrar_cliente(self, cliente: Cliente):
        if any(c.identificador == cliente.identificador for c in self.clientes):
            raise ValidacionError("Ya existe un cliente con ese identificador.")
        self.clientes.append(cliente)
        logger.info("Cliente registrado: %s.", cliente.identificador)
        return cliente

    def registrar_servicio(self, servicio: Servicio):
        if any(s.identificador == servicio.identificador for s in self.servicios):
            raise ValidacionError("Ya existe un servicio con ese identificador.")
        self.servicios.append(servicio)
        logger.info("Servicio registrado: %s.", servicio.identificador)
        return servicio

    def buscar_cliente(self, identificador: str) -> Cliente:
        for cliente in self.clientes:
            if cliente.identificador == identificador:
                return cliente
        raise ClienteNoEncontradoError(f"No se encontró cliente {identificador}.")

    def crear_reserva(self, identificador, id_cliente, id_servicio, duracion,
                      impuesto=0.19, descuento=0.0):
        cliente = self.buscar_cliente(id_cliente)
        servicio = next(
            (s for s in self.servicios if s.identificador == id_servicio), None
        )
        if servicio is None:
            raise ServicioNoDisponibleError(f"No se encontró servicio {id_servicio}.")
        reserva = Reserva(identificador, cliente, servicio, duracion, impuesto, descuento)
        if any(r.identificador == identificador for r in self.reservas):
            raise ValidacionError("Ya existe una reserva con ese identificador.")
        self.reservas.append(reserva)
        logger.info("Reserva creada: %s.", identificador)
        return reserva

    def listar_clientes(self):
        return [c.mostrar_informacion() for c in self.clientes]

    def listar_servicios(self):
        return [s.mostrar_informacion() for s in self.servicios]

    def listar_reservas(self):
        return [r.mostrar_informacion() for r in self.reservas]


# ============================ DEMOSTRACIÓN ====================================
def ejecutar_operacion(numero, descripcion, accion):
    """Ejecuta cada operación aislando errores para que la demo continúe."""
    print(f"\nOPERACIÓN {numero}: {descripcion}")
    try:
        resultado = accion()
    except ErrorSistema as error:
        logger.error("Operación %s fallida: %s", numero, error)
        print(f"ERROR CONTROLADO: {error}")
    except Exception as error:
        # Ejemplo de encadenamiento de excepciones.
        logger.exception("Error inesperado en operación %s.", numero)
        try:
            raise ErrorSistema(f"Fallo inesperado en operación {numero}") from error
        except ErrorSistema as error_encadenado:
            print(f"ERROR INESPERADO CONTROLADO: {error_encadenado}")
    else:
        logger.info("Operación %s completada.", numero)
        print(resultado)
    finally:
        print("Fin de operación (finally).")


def main():
    sistema = GestorSoftwareFJ()
    print("=" * 70)
    print("SOFTWARE FJ - DEMOSTRACIÓN DEL SISTEMA DE CLIENTES, SERVICIOS Y RESERVAS")
    print("=" * 70)

    # Operación 1: cliente válido.
    ejecutar_operacion(1, "Registro de cliente válido",
        lambda: sistema.registrar_cliente(
            Cliente("C001", "Ana Torres", "ana.torres@email.com", "3001234567")
        ).mostrar_informacion())

    # Operación 2: segundo cliente válido.
    ejecutar_operacion(2, "Registro de otro cliente válido",
        lambda: sistema.registrar_cliente(
            Cliente("C002", "Carlos Ruiz", "carlos.ruiz@email.com", "3119876543")
        ).mostrar_informacion())

    # Operación 3: registro inválido de correo.
    ejecutar_operacion(3, "Registro de cliente con correo inválido",
        lambda: sistema.registrar_cliente(
            Cliente("C003", "Laura Díaz", "correo-invalido", "3201112233")
        ))

    # Operación 4: servicio de sala válido.
    ejecutar_operacion(4, "Creación de servicio de sala",
        lambda: sistema.registrar_servicio(
            ReservaSala("S001", "Sala Ejecutiva", 80000, 12)
        ).describir_servicio())

    # Operación 5: servicio de alquiler de equipo válido.
    ejecutar_operacion(5, "Creación de servicio de alquiler de equipo",
        lambda: sistema.registrar_servicio(
            AlquilerEquipo("S002", "Proyector HD", 45000, "Proyector")
        ).describir_servicio())

    # Operación 6: servicio de asesoría válido.
    ejecutar_operacion(6, "Creación de asesoría especializada",
        lambda: sistema.registrar_servicio(
            AsesoriaEspecializada("S003", "Consultoría Python", 120000,
                                 "Programación Python")
        ).describir_servicio())

    # Operación 7: intento de crear servicio con tarifa negativa.
    ejecutar_operacion(7, "Creación de servicio con tarifa inválida",
        lambda: sistema.registrar_servicio(
            ReservaSala("S004", "Sala Inválida", -1000, 5)
        ))

    # Operación 8: reserva válida y confirmación.
    reserva_1 = None
    def crear_y_confirmar_reserva():
        nonlocal reserva_1
        reserva_1 = sistema.crear_reserva("R001", "C001", "S001", 2,
                                          impuesto=0.19, descuento=0.10)
        return reserva_1.confirmar()
    ejecutar_operacion(8, "Creación y confirmación de reserva válida",
                      crear_y_confirmar_reserva)

    # Operación 9: procesar reserva confirmada.
    ejecutar_operacion(9, "Procesamiento de reserva y cálculo de costo",
        lambda: f"Total de reserva R001: ${reserva_1.procesar():,.2f}")

    # Operación 10: reserva con duración inválida.
    ejecutar_operacion(10, "Intento de reserva con duración cero",
        lambda: sistema.crear_reserva("R002", "C002", "S002", 0))

    # Operación 11: reserva con cliente inexistente.
    ejecutar_operacion(11, "Reserva con cliente no registrado",
        lambda: sistema.crear_reserva("R003", "C999", "S001", 1))

    # Operación 12: servicio marcado no disponible.
    def reservar_servicio_no_disponible():
        servicio = next(s for s in sistema.servicios if s.identificador == "S002")
        servicio.cambiar_disponibilidad(False)
        return sistema.crear_reserva("R004", "C002", "S002", 1)
    ejecutar_operacion(12, "Reserva de servicio no disponible",
                      reservar_servicio_no_disponible)

    # Operación 13: cancelación de una reserva pendiente.
    def crear_y_cancelar():
        reserva = sistema.crear_reserva("R005", "C002", "S003", 1)
        return reserva.cancelar()
    ejecutar_operacion(13, "Creación y cancelación de reserva",
                      crear_y_cancelar)

    # Operación 14: intento de procesar reserva sin confirmar.
    ejecutar_operacion(14, "Procesar reserva pendiente (operación no permitida)",
        lambda: sistema.crear_reserva("R006", "C002", "S001", 1).procesar())

    # Operación 15: sobrecarga/sobrecarga simulada de cálculo de costos.
    def mostrar_variantes_costos():
        sala = next(s for s in sistema.servicios if s.identificador == "S001")
        valor_1 = sala.calcular_costo(2)  # duración solamente
        valor_2 = sala.calcular_costo(2, impuesto=0.19)  # con impuesto
        valor_3 = sala.calcular_costo(2, impuesto=0.19, descuento=0.10)
        return (
            "Variantes calcular_costo():\n"
            f"  Sin impuesto ni descuento: ${valor_1:,.2f}\n"
            f"  Con impuesto: ${valor_2:,.2f}\n"
            f"  Con impuesto y descuento: ${valor_3:,.2f}"
        )
    ejecutar_operacion(15, "Prueba de variantes del cálculo de costo",
                      mostrar_variantes_costos)

    # Resumen final.
    print("\n" + "=" * 70)
    print("RESUMEN DEL SISTEMA")
    print("=" * 70)
    print(f"Clientes registrados: {len(sistema.clientes)}")
    print(f"Servicios registrados: {len(sistema.servicios)}")
    print(f"Reservas almacenadas: {len(sistema.reservas)}")
    print("\nCLIENTES:")
    for item in sistema.listar_clientes():
        print(" -", item)
    print("\nSERVICIOS:")
    for item in sistema.listar_servicios():
        print(" -", item)
    print("\nRESERVAS:")
    for item in sistema.listar_reservas():
        print(" -", item)
    print("\nLos eventos y errores fueron registrados en software_fj.log")
    print("El sistema finalizó correctamente.")


if __name__ == "__main__":
    main()
