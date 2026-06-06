---
# 7. Configuración del webhook de recepción de ventas
---

## 7.1. Descripción

El webhook de recepción de ventas permite que MiTienda notifique automáticamente a odoo cuando una venta ha sido aprobado. Al recibir la notificación, odoo iniciará el proceso de sincronización de la venta, validando la información del cliente, productos y demás datos necesarios para su registro.

## 7.2. URL del webhook

La siguiente URL debe configurarse en MiTienda para el envío automático de eventos de ventas:

-   Reemplace `dominio.test` por la dirección o dominio donde se encuentre publicado su servidor Odoo.

__Nota importante:__ Si el dominio tiene multiples bases de datos, Odoo no podrá determinar la base de datos a la cual se dirige la solicitud y el webhook no podrá ser procesado. Se recomienda usar un dominio para identificar la base de datos, caso contrario no tener más de una base de datos en su servidor odoo.

```
https://dominio.test/webhook/sale_order

```

## 7.3. Estructura de datos recibida

A continuación se presenta un ejemplo de la estructura mínima de datos que debe ser enviada desde MiTienda al webhook de Odoo.


```json
{
    "object": "order",
    "id": 861359,
    "status": 1,
    "date_created": "2026-05-29 09:57:45",
    "code": "WEB12965ABCAE79",
    "items": [
        {
            "id": 4380755,
            "sku": "PROD-112",
            "quantity": 2,
            "unit_price": 99.99
        }
    ],
    "total_items": 199.98,
    "total_amount": 199.98,
    "billing_info": {
        "name": "Juán",
        "last_name": "Pérez",
        "email": "jperez@test.com",
        "phone_number": "56456456",
        "doc_number": "9647695"
    },
    "customer": {
        "id": 43225,
        "name": "Juán",
        "last_name": "Pérez",
        "email": "jperez@test.com",
        "phone_number": "56456456",
        "doc_number": "9647695"
    }
}
```

## 7.4. Resultado de la sincronización

Cuando se recibe la información, Odoo realiza las siguientes acciones:

-   Verifica existencia del cliente, si no existe registra el cliente (dependiente de la configuración)
-   Verifica la existencia de los productos, si no existe algún producto, no se procede con el registro de la venta
-   Registra orden de venta
-   Confirma orden de venta (dependiente de la configuración)
-   Crea factura de orden de venta (dependiente de la configuración)
-   Confirma factura (dependiente de la configuración)
-   En caso de existir inconsistencias en los datos recibidos el sistema registrará el error en el log

## 7.5. Para pruebas del webhook también puede usar curl

```
curl -X POST -H "Content-Type: application/json" -d @body.json http://dominio.test/webhook/sale_order
```

-   **Donde:**
    -  `body.json` Contiene la información de la venta en formato JSON
    -  `http://dominio.test/webhook/sale_order`  Es la URL configurada para la recepción de ventas

-   **Resultado esperado**

````json
{
    "success": true,
    "message":"Venta sincronizada"
}
````

-   **Posibles errores**

| Código | Descipcion |
|--------|------------|
| 404 | No se encontró una configuración activa |
| 422 | Estructura de datos inválida |
| 500 | error interno |


-   **Verificación en odoo** Despues de ejecutar la prueba:
    -   Ingrese al módulo ventas
    -   Verifique la bitácora de ventas
    -   Verifique que la orden se haya registrado
