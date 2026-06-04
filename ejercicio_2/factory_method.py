"""
PATRÓN CREACIONAL: Factory Method
----------------------------------
Proporciona una interfaz para crear objetos en una superclase,
pero permite a las subclases alterar el tipo de objeto que se creará.

Ejemplo concreto: Sistema de notificaciones.
Una app puede enviar notificaciones por Email, SMS o Push.
El Factory Method permite que cada canal tenga su propia lógica
de creación sin que el código cliente dependa de clases concretas.
"""

from abc import ABC, abstractmethod


# ---------- Producto abstracto ----------

class Notificacion(ABC):
    @abstractmethod
    def enviar(self, destinatario: str, mensaje: str) -> str:
        pass


# ---------- Productos concretos ----------

class NotificacionEmail(Notificacion):
    def enviar(self, destinatario: str, mensaje: str) -> str:
        return f"[EMAIL] Para: {destinatario} | Mensaje: {mensaje}"


class NotificacionSMS(Notificacion):
    def enviar(self, destinatario: str, mensaje: str) -> str:
        return f"[SMS] Para: {destinatario} | Mensaje: {mensaje}"


class NotificacionPush(Notificacion):
    def enviar(self, destinatario: str, mensaje: str) -> str:
        return f"[PUSH] Para: {destinatario} | Mensaje: {mensaje}"


# ---------- Creador abstracto (Factory) ----------

class NotificacionFactory(ABC):
    @abstractmethod
    def crear_notificacion(self) -> Notificacion:
        """Factory Method: cada subclase decide qué objeto crear."""
        pass

    def notificar(self, destinatario: str, mensaje: str) -> str:
        """Usa el factory method; el cliente no sabe qué clase concreta se usa."""
        notificacion = self.crear_notificacion()
        return notificacion.enviar(destinatario, mensaje)


# ---------- Creadores concretos ----------

class EmailFactory(NotificacionFactory):
    def crear_notificacion(self) -> Notificacion:
        return NotificacionEmail()


class SMSFactory(NotificacionFactory):
    def crear_notificacion(self) -> Notificacion:
        return NotificacionSMS()


class PushFactory(NotificacionFactory):
    def crear_notificacion(self) -> Notificacion:
        return NotificacionPush()


# ---------- Uso del patrón ----------

def procesar_alerta(factory: NotificacionFactory, usuario: str, texto: str):
    """El código cliente trabaja con la interfaz, no con clases concretas."""
    resultado = factory.notificar(usuario, texto)
    print(resultado)


if __name__ == "__main__":
    print("=== Factory Method: Sistema de Notificaciones ===\n")

    canales = [
        EmailFactory(),
        SMSFactory(),
        PushFactory(),
    ]

    for canal in canales:
        procesar_alerta(canal, "juan@ejemplo.com", "Tu pedido fue despachado.")

    print()

    # Se puede elegir el canal dinámicamente según configuración
    tipo = "sms"
    factories = {"email": EmailFactory, "sms": SMSFactory, "push": PushFactory}
    factory_elegida = factories[tipo]()
    procesar_alerta(factory_elegida, "+59891234567", "Código de verificación: 4821")
