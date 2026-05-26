---
### 1. Configuración de conexión
---

### Procedimiento
-   [Paso #1: Solicitar token de acceso al proveedor de API](#paso-1-solicitar-token-de-acceso-al-proveedor-de-api)
-   [Paso #2: Configurar parámetros de conexión](#paso-2-configurar-parametros-de-conexion)
-   [Paso #3: Probar conexión](#paso-3-probar-conexion)

### Paso #1: Solicitar token de acceso al proveedor de API

Para comenzar a sincronizar datos entre Odoo y MiTienda.pe necesita obtener un token de consumo de la [API MiTienda.pe versión 1.1](https://publicapi.mitienda.pe/docs/)


### Paso #2: Configurar parámetros de conexión
Acceder al modulo de MiTienda.pe

![acceso al modulo](/docs/assets/configuracion/modulo_mitienda.png)

Para registrar una conexion, debe ingresar al formulario de _parámetros de conexion_

![parametros de conexion](/docs/assets/configuracion/1_configuracion.png)

![registro](/docs/assets/configuracion/2_configuracion.png)

En el formulario de parámetros de conexion debe registrar los datos solicitados en los campos:

-   **Parámetros de conexión**
    -   **API Host**: Registre el host, por ejemplo: `https://publicapi.mitienda.pe/api/v1`
    -   **Entorno**: Seleccione una opción entre `Produccion` y `Pruebas`
    -   **Token API**: Registre el token de acceso para consumo de API
    -   **Expiración token**: Registre la fecha de vencimiento del token de acceso
    -   **Timeout HTTP**: Registre el tiempo de espera en segundos para establecer la conexión con la API
    -   **Activo**: El sistema buscará una conexión activa, caso contrario se genera un error de conexión
-   **Sincronización de clientes**
    -   **Lógica de sincronización:** Seleccione una de las siguientes opciones:
        -  `Registrar nuevos clientes`: Permite que se registren nuevos clientes con los datos de los clientes que obtienen desde la venta
        -  `Usar cliente predefinido`: Permite que la venta se registre con el cliente predeterminado registrado en el campo `Cliente predefinido`

    -   **Cliente predefinido**: Permite establecer un clientes predefinido que se usará para registrar las ventas

-   **Sincronización de ventas**
    -   **Lógica de sincronización**: seleccione una de las siguientes opciones:
        -  `Registrar cotizaciones`: Permite que las ventas de la API se registren en Odoo en estado de `Cotización`
        -  `Registrar ventas`: Permite que las ventas de la API se registren en Odoo y además se confirman automáticamente dejando la venta en estado de `Orden de venta`

        -  `Registrar ventas y facturas en borrador`: Permite que las ventas de la API se registren en Odoo y además se confirman automáticamente dejando la venta en estado de `Orden de venta` y además crea la factura de cliente en estado de `Borrador`

        -  `Registrar ventas y facturas publicadas`: Permite que las ventas de la API se registren en Odoo y además se confirman automáticamente dejando la venta en estado de `Orden de venta` y además crea la factura de cliente y se confirma la factura de manera automática dejando en estado `Registrado`

![cliente predeterminado](/docs/assets/configuracion/3_configuracion.png)

### Paso #3: Probar conexión

Luego de concluir el registro debe _**Probar Conexión**_

Si la conexión se establece con éxito, se mostrará de manerá automática la notificación de _**Exito**_ como se ve en la imagén, caso contrario se visualizará una notificación de _**Error**_.

![probar conexion](/docs/assets/configuracion/4_probar_conexion.png)
