"""
PATRÓN DE COMPORTAMIENTO: Mediator
------------------------------------
Reduce las dependencias caóticas entre objetos. El patrón restringe
las comunicaciones directas entre objetos, forzándolos a colaborar
únicamente a través de un objeto mediador.

Ejemplo concreto: Chat de sala de reuniones.
En lugar de que cada usuario tenga referencias a todos los demás
(acoplamiento O(n²)), todos se comunican a través de un Mediador
(SalaDeChat). Si se agrega o elimina un participante, nadie
más necesita cambiar su código.

Sin Mediator: Usuario_A <-> Usuario_B <-> Usuario_C  (todos se conocen)
Con Mediator: Usuario_A -> SalaDeChat <- Usuario_B
                                      <- Usuario_C
"""

from abc import ABC, abstractmethod
from datetime import datetime


# ---------- Interfaz del Mediador ----------

class Mediador(ABC):
    @abstractmethod
    def enviar_mensaje(self, mensaje: str, remitente: "Participante") -> None:
        pass

    @abstractmethod
    def registrar(self, participante: "Participante") -> None:
        pass


# ---------- Interfaz del Participante ----------

class Participante(ABC):
    def __init__(self, nombre: str):
        self.nombre = nombre
        self._mediador: Mediador | None = None

    def unirse(self, mediador: Mediador) -> None:
        self._mediador = mediador
        mediador.registrar(self)

    @abstractmethod
    def enviar(self, mensaje: str) -> None:
        pass

    @abstractmethod
    def recibir(self, mensaje: str, remitente: str) -> None:
        pass


# ---------- Mediador concreto ----------

class SalaDeChat(Mediador):
    def __init__(self, nombre_sala: str):
        self.nombre_sala = nombre_sala
        self._participantes: list[Participante] = []
        self._historial: list[str] = []

    def registrar(self, participante: Participante) -> None:
        if participante not in self._participantes:
            self._participantes.append(participante)
            aviso = f"[{self.nombre_sala}] {participante.nombre} se unió a la sala."
            print(aviso)
            self._historial.append(aviso)

    def enviar_mensaje(self, mensaje: str, remitente: Participante) -> None:
        marca = datetime.now().strftime("%H:%M:%S")
        entrada = f"[{marca}] {remitente.nombre}: {mensaje}"
        self._historial.append(entrada)

        # Retransmite a todos excepto al remitente
        for participante in self._participantes:
            if participante is not remitente:
                participante.recibir(mensaje, remitente.nombre)

    def mostrar_historial(self) -> None:
        print(f"\n-- Historial de '{self.nombre_sala}' --")
        for linea in self._historial:
            print(f"  {linea}")


# ---------- Participantes concretos ----------

class UsuarioHumano(Participante):
    def enviar(self, mensaje: str) -> None:
        if self._mediador is None:
            raise RuntimeError("El usuario no está en ninguna sala.")
        print(f"{self.nombre} envía: \"{mensaje}\"")
        self._mediador.enviar_mensaje(mensaje, self)

    def recibir(self, mensaje: str, remitente: str) -> None:
        print(f"  [{self.nombre} recibe de {remitente}]: \"{mensaje}\"")


class BotAsistente(Participante):
    """Participante automatizado; responde a palabras clave."""

    RESPUESTAS = {
        "hola": "Hola! Soy el asistente de la sala. ¿En qué puedo ayudar?",
        "ayuda": "Comandos disponibles: /hora, /participantes.",
    }

    def enviar(self, mensaje: str) -> None:
        if self._mediador is None:
            return
        self._mediador.enviar_mensaje(mensaje, self)

    def recibir(self, mensaje: str, remitente: str) -> None:
        clave = mensaje.lower().strip()
        if clave in self.RESPUESTAS:
            print(f"  [{self.nombre} (bot) detectó palabra clave '{clave}']")
            self.enviar(self.RESPUESTAS[clave])


# ---------- Uso del patrón ----------

if __name__ == "__main__":
    print("=== Mediator: Sala de Chat ===\n")

    # Crear el mediador (sala)
    sala = SalaDeChat("Reunión de Proyecto")

    # Crear participantes
    ana = UsuarioHumano("Ana")
    carlos = UsuarioHumano("Carlos")
    bot = BotAsistente("AsistenteBot")

    # Todos se unen a través del mediador
    ana.unirse(sala)
    carlos.unirse(sala)
    bot.unirse(sala)

    print()

    # Los participantes se comunican sin conocerse directamente
    ana.enviar("Hola")
    print()
    carlos.enviar("Hola Ana! ¿Revisaste el informe?")
    print()
    ana.enviar("Ayuda")
    print()
    carlos.enviar("Bot, gracias por la info.")

    sala.mostrar_historial()
