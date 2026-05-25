---
### 3. Sincronización manual de ventas
---

### Procedimiento
-   [Paso #1: Datos para sincronización manual](#paso-1-datos-para-sincronizacion-manual)
-   [Paso #2: Sincronización](#paso-2-sincronizacion)
-   [Paso #3: Verificar bitácora de sincronización de ventas](#paso-3-verificar-bitacora-de-sincronizacion-de-ventas)
-   [Paso #4: Verificar bitacorá de clientes](#paso-4-verificar-bitacora-de-clientes)

---

### Paso #1: Datos para sincronización manual
Ingresar al menú de ventas,`MiTienda.pe->Sincronización->ventas`.

![menu sincronizacion de ventas](/docs/assets/sincronizacion_ventas/0_sincronizacion_manual_ventas.png)

-   Se habilitará un formulario con los siguientes campos:
    -   __Fecha inicio__: Ingrese una fecha inicio para obtener ventas desde el sistema externo de miTienda
    -   __Fecha fin__: Ingrese una fecha límite para obtener ventas desde el sistema externo de miTienda.

![sincronizar](/docs/assets/sincronizacion_ventas/1_sincronizar.png)

### Paso #2: Sincronización
-   Para sincronizar haga click sobre el botón ___Sincronizar___, esta acción realizará el procedimiento de obtener las ventas en un rango de fecha desde la api externa y registrar , validar , crear facturas y publicarlo en odoo, en base a la **configuración de conexion** realizado.

-   En caso de `Exito o Error`  es visible la notificacion como se muestra en la imagen.

![0 ventas registrados](/docs/assets/sincronizacion_ventas/2_sincronizacion_sin_venta.png)

![venta registrado](/docs/assets/sincronizacion_ventas/3_sincronizacion.png)

### Paso #3: Verificar bitácora de sincronización de ventas
Verificamos el registro de la venta en la bitácora. ingresando al menú `MiTienda.pe->Bitácora->ventas`.

-   Se puede observar que se registro una venta, para ingresar a la venta haga click sobre el codigo de la venta, y este direccionará al formulario de venta.

![bitacora venta](/docs/assets/sincronizacion_ventas/4_venta_sincronizado.png)

-   Como se puede ver en la imagen, se creó y confirmó la venta dejando en estado de `Orden de venta`, ademas de eso creó la factura como se logra ver en la imagen en el botón inteligente.

![venta](/docs/assets/sincronizacion_ventas/5_venta.png)

-   Accedemos a la factura atraves del botón inteligente.
-   verificamos que efectivamente se creo la factura y ademas se valido dejando en estado `Registrado`

![factura](/docs/assets/sincronizacion_ventas/6_factura.png)

### Paso #4: Verificar bitacorá de clientes
-   Verificamos también la bitacorá de clientes.
-   Si el cliente no existe en la base de odoo, se registra como un nuevo cliente.
-   Como es el caso del ejemplo, el cliente de la venta no existe y se procede a registrarlo como nuevo y se asocia a la venta de odoo de manera automática.

![bitacora](/docs/assets/sincronizacion_ventas/7_cliente.png)

-   Nuevo cliente

![Nuevo contacto](/docs/assets/sincronizacion_ventas/8_clientes_api.png)
