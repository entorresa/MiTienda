## Configuración de productos
---
## Índice
-   [Registrar producto y establecer un SKU ](#registrar-producto-y-establecer-un-sku)
-   [Registrar variante de producto y establecer un SKU](#registrar-variante-de-producto-y-establecer-un-sku)
---

## Registrar producto y establecer un SKU
Antes de realizar la sincronización de ventas, debe registrar todos los productos de ventas que existen en el sistema externo.

La sincronización de ventas del modulo MiTienda.pe __NO CREA PRODUCTOS__.

Para registrar un producto que no tiene variantes, debe registrar desde menu `ventas/Productos`.

![Productos](/docs/assets/productos/1_registrar_producto.png)

-   Se debe establecer el **`SKU`** en la pestaña de `MiTienda.pe`. La sincronización de ventas buscará el producto atravez del **SKU**. si el producto no existe en odoo la venta no se registrará.

![registro de sku](/docs/assets/productos/2_registrar_producto.png)

---

## Registrar variante de producto y establecer un SKU
Si el producto tiene variantes debe registrar el **SKU** en cada variante de producto.

![variantes de productos](/docs/assets/productos/1_variantes.png)

![registro de sku](/docs/assets/productos/2_variantes.png)

---