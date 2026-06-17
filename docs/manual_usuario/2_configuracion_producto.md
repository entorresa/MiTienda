---
### 2. Configuración de productos
---

### Procedimiento
-   [2.1. Registrar producto y establecer un SKU ](#21-registrar-producto-y-establecer-un-sku)
-   [2.2. Registrar variante de producto y establecer un SKU](#22-registrar-variante-de-producto-y-establecer-un-sku)
-   [2.3.  Verificar SKU](#23-verificar-sku)
### 2.1. Registrar producto y establecer un SKU
Antes de realizar la sincronización de ventas, debe registrar todos los productos de ventas que existen en el sistema externo.

La sincronización de ventas del modulo MiTienda.pe __NO REGISTRA PRODUCTOS AUTOMÁTICAMENTE__.

Para registrar un producto que no tiene variantes, debe registrar desde menu `ventas/Productos`.

![Productos](/docs/assets/productos/1_registrar_producto.png)

-   Se debe establecer el **`SKU`** en la pestaña de `MiTienda.pe`. La sincronización de ventas buscará cada producto mediante del **SKU**. si el producto no existe en Odoo la venta no se registrará.

![registro de sku](/docs/assets/productos/2_registrar_producto.png)

### 2.2. Registrar variante de producto y establecer un SKU
Si el producto tiene variantes debe registrar el **SKU** en cada variante de producto.

![variantes de productos](/docs/assets/productos/1_variantes.png)

![registro de sku](/docs/assets/productos/2_variantes.png)

### 2.3. Verificar SKU
-   Si un producto no tiene variantes , puede realizar la __`verificación de SKU`__  desde el formulario **Producto**.

-   Si el producto tiene N variantes debe __`verificar el SKU`__ desde el formulario de variantes de producto. Cada variante tiene su propio SKU

- Para verificar haga click sobre el botón **Verificar SKU**, Si el ID actual es diferente al ID de miTienda.pe se actualizará por el valor que contiene miTienda.pe.

![Verificar sku](/docs/assets/productos/3_verificar_sku.png)

![Verificar sku](/docs/assets/productos/4_verificar_sku.png)