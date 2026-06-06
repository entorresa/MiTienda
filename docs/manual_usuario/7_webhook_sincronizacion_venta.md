---
# 7. Configuración del webhook de recepción de ventas
---

## 7.1. Descripción

El webhook de recepción de ventas permite que MiTienda notifique automáticamente a odoo cuando una venta ha sido aprobado. Al recibir la notificación, odoo iniciará el proceso de sincronización de la venta, validando la información del cliente, productos y demas datos necesarios para su registro.

## 7.2. URL del webhook

La siguiente URL debe configurarse en MiTienda para el envío automático de eventos de ventas:

-   Reemplace `localhost:8070`  por la dirección o dominio donde se encuentre publicado su servidor ODOO.

__Nota importante:__ Si el dominio tiene multiples bases de datos, Odoo no podrá determinar aque base de datos debe dirigir la solicitud y el webhook no podrá ser procesado. se recomienda usar un dominio para identificar la base de datos, caso contrario no debe tener mas de una instancia en su servidor odoo.


```
http://localhost:8070/webhook/sale_order

```
## 7.3. Estructura de datos recibida
A continuación se encuentra un ejemplo del contenido enviado por MiTienda al webhook.


```json
{
    "object": "order",
    "id": 861359,
    "status": 1,
    "status_detail": "aprobado",
    "date_created": "2026-05-29 09:57:45",
    "receive_type": "shipping",
    "date_payment": "",
    "code": "WEB12965ABCAE79",
    "referral_name": "",
    "referral_code": "",
    "note": "",
    "items": [
        {
            "id": 4380755,
            "sku": "PROD-112",
            "title": "Producto de Ejemplo",
            "variation_attributes": "",
            "variation_attributes_detail": {},
            "discount": {},
            "quantity": 2,
            "unit_price": 99.99,
            "kind_of_item": 1,
            "currency_id": 1,
            "currency_iso": "PEN",
            "type_iva": 1
        }
    ],
    "discount": [],
    "discount_global": 0,
    "total_items": 199.98,
    "total_amount": 199.98,
    "payment_gateway_id": 5,
    "payment_gateway": "DEPÓSITO / TRANSFERENCIA",
    "payment_method": "",
    "payment_gateway_transaction_code": "",
    "billing_info": {
        "name": "DOMICELIA",
        "last_name": "DIAZ PEREIRA",
        "email": "domicita098@gamil.com",
        "phone_number": "56456456",
        "billing_address": [],
        "doc_id": "1",
        "doc_type": "DNI",
        "doc_number": "9647695",
        "business_name": "",
        "e-billing": {}
    },
    "shipping": {
        "status": "pago_confirmado",
        "status_id": 31,
        "name": "ELGAR JOB",
        "last_name": "SERRANO GALVEZ",
        "phone_number": "56456456",
        "billing_address": [],
        "doc_id": 0,
        "doc_type": null,
        "doc_number": null,
        "date_delivered": "",
        "receiver_address": {
            "address_line": "Av Arequipa 4130",
            "address_line2": null,
            "address_reference": "",
            "zip_code": null,
            "country": {
                "id": 1,
                "name": "PERÚ"
            },
            "state": {
                "id": 15,
                "name": "LIMA"
            },
            "city": {
                "id": 1,
                "name": "LIMA"
            },
            "district": {
                "id": 10,
                "name": "COMAS"
            },
            "latitude": null,
            "longitude": null,
            "comment": "",
            "erp_code": ""
        },
        "cost": 0,
        "courier": {},
        "comment": "",
        "erp_code": ""
    },
    "pickup_store": {},
    "customer": {}
}
```

## 7.4. Resultado de la sincronización
Cuando se reciba la información, Odoo realizará las siguientes acciones:

-   Verifica existencia del cliente, si no existe registra el cliente.
-   Verifica la existencia de los productos, si no existe algún producto, no se procede con el registro de venta.
-   Registra orden de venta
-   Confirma orden de venta
-   Crea factura de orden de venta
-   Confirma factura.
-   En caso de existir inconsistencias en los datos recibidos, el sistema registrará el error en el log.

## 7.5. Para pruebas del webhook también puede usar curl.

```
curl -X POST -H "Content-Type: application/json" -d @body.json http://localhost:8070/webhook/sale_order
```
-   **Donde:**
    -  `body.json` Contiene la información de la venta en formato JSON.
    -  `http://localhost:8070/webhook/sale_order`  Es la URL configurada para la recepción de ventas

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
| 404 | No se encontró una configuración activa|
| 422 | Estructura de datos inválida|
| 500 | error interno|


-   **Verificación en odoo** Despues de ejecutar la prueba:
    -   Ingrese al módulo ventas
    -   Verifique que la orden se haya registrado
    -   Verifique también la bitácora de ventas.