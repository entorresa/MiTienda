---
### 6. Acción Planificada
---

### Procedimiento
-   [6.1. Ingresar al formulario de accion planificada](#61-ingresar-al-formulario-de-accion-planificada)
-   [6.2. Activar/Desactivar acción planificada](#62-activardesactivar-accion-planificada)
-   [6.3. Ejecutar de forma manual](#63-ejecutar-de-forma-manual)

Al instalar o actualizar el módulo creará automáticamente la acción planificada configurado para ejecutarse cada 4horas. Esta acción sincronizará las venta de la fecha actual.

No es necesario realizar ninguna configuración de parte del usuario.

### 6.1. Ingresar al formulario de accion planificada
-   Ingrese al módulo de `Ajustes ->Técnico ->Aciones planificadas`

![menu de ingreso](/docs/assets/accion_planificada/1_menu_accion_planificada.png)

-   La accion planificada es __`Sincronizar ventas API MiTienda.pe`__, click sobre el registro para ingresar al formulario.

![listado](/docs/assets/accion_planificada/2_listado_accion_planificada.png)

-   Aqui puede verificar los datos de la acción planificada, también puede modificar los intervalos de tiempo, o fecha de proxima ejecución,

___Nota importante:___ La fecha de próxima ejecución nunca debe estar en el pasado, cada contrario no se ejecutará la acción planificada, siempre debe registrar una fecha a futuro

![formulario de accion planificada](/docs/assets/accion_planificada/4_accion_planifica.png)

### 6.2. Activar/Desactivar acción planificada

Si desea  **Deshabilitar** la ejecución automática de la acción planificada, debe desmarcar la opción _**Activo**_.

una vez desactivado, la acción planificada dejará de ejecutarse de forma automática según la frecuencia configurada.

![desactivar](/docs/assets/accion_planificada/accion_planificada_desactivo.png)

-   Para habilitar debe activar en el campo _**Activo**_, debe quedar como se muestra en la imagen

![activar](/docs/assets/accion_planificada/accion_planificada_activo.png)

### 6.3. Ejecutar de forma manual

Permite ejecutar de manera manual mediante el boton __`Ejecutar de forma manual`__

![sincronizacion manual](/docs/assets/accion_planificada/3_accion_planificada.png)