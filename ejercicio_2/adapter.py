"""
PATRÓN ESTRUCTURAL: Adapter
-----------------------------
Permite la colaboración entre objetos con interfaces incompatibles.
Actúa como un "traductor" entre dos clases que no pueden trabajar
juntas directamente.

Ejemplo concreto: Integración de pasarelas de pago.
El sistema espera una interfaz uniforme (PasarelaPago), pero
cada proveedor externo (PayPal, MercadoPago) tiene su propia API
con métodos y formatos distintos.
El Adapter traduce las llamadas sin modificar las clases externas.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


# ---------- Interfaz esperada por el sistema ----------

class PasarelaPago(ABC):
    @abstractmethod
    def cobrar(self, monto: float, moneda: str) -> dict:
        pass

    @abstractmethod
    def reembolsar(self, id_transaccion: str) -> bool:
        pass


# ---------- Clases externas (incompatibles) ----------
# Simulan SDKs de terceros que no podemos modificar.

class PayPalSDK:
    """API de PayPal (externa, no modificable)."""

    def make_payment(self, amount_usd: float, description: str) -> str:
        return f"PP-TXN-{int(amount_usd * 100)}"

    def refund_transaction(self, paypal_txn_id: str) -> dict:
        return {"success": True, "refunded_id": paypal_txn_id}


class MercadoPagoSDK:
    """API de MercadoPago (externa, no modificable)."""

    def crear_pago(self, valor: float, divisa: str) -> dict:
        return {"id": f"MP-{int(valor)}", "estado": "aprobado", "divisa": divisa}

    def devolver_pago(self, mp_id: str) -> bool:
        return True


# ---------- Adaptadores ----------

class AdapterPayPal(PasarelaPago):
    def __init__(self):
        self._sdk = PayPalSDK()

    def cobrar(self, monto: float, moneda: str) -> dict:
        txn_id = self._sdk.make_payment(monto, f"Pago de {monto} {moneda}")
        return {"id_transaccion": txn_id, "monto": monto, "moneda": moneda, "proveedor": "PayPal"}

    def reembolsar(self, id_transaccion: str) -> bool:
        resultado = self._sdk.refund_transaction(id_transaccion)
        return resultado["success"]


class AdapterMercadoPago(PasarelaPago):
    def __init__(self):
        self._sdk = MercadoPagoSDK()

    def cobrar(self, monto: float, moneda: str) -> dict:
        respuesta = self._sdk.crear_pago(monto, moneda)
        return {"id_transaccion": respuesta["id"], "monto": monto, "moneda": moneda, "proveedor": "MercadoPago"}

    def reembolsar(self, id_transaccion: str) -> bool:
        return self._sdk.devolver_pago(id_transaccion)


# ---------- Código cliente (no sabe qué proveedor usa) ----------

def procesar_compra(pasarela: PasarelaPago, monto: float, moneda: str):
    """Trabaja únicamente con la interfaz PasarelaPago."""
    print(f"  Cobrando {monto} {moneda}...")
    resultado = pasarela.cobrar(monto, moneda)
    print(f"  Transacción: {resultado}")

    print(f"  Reembolsando transacción {resultado['id_transaccion']}...")
    exito = pasarela.reembolsar(resultado["id_transaccion"])
    print(f"  Reembolso exitoso: {exito}")


if __name__ == "__main__":
    print("=== Adapter: Pasarelas de Pago ===\n")

    proveedores = {
        "PayPal": AdapterPayPal(),
        "MercadoPago": AdapterMercadoPago(),
    }

    for nombre, pasarela in proveedores.items():
        print(f"-- Proveedor: {nombre} --")
        procesar_compra(pasarela, 150.0, "USD")
        print()
