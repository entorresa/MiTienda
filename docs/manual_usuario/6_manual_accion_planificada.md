---
### 6. Acción Planificada
---

### Procedimiento

-   [6.1. Ingresar al formulario de acción planificada](#61-ingresar-al-formulario-de-accion-planificada)
-   [6.2. Activar/Desactivar acción planificada](#62-activardesactivar-accion-planificada)
-   [6.3. Ejecutar de forma manual](#63-ejecutar-de-forma-manual)

Al instalar o actualizar el módulo creará automáticamente la acción planificada configurada para ejecutarse cada 4 horas. Esta acción sincronizará las ventas de la fecha actual.

No es necesario realizar ninguna configuración por parte del usuario.

### 6.1. Ingresar al formulario de acción planificada

-   Ingrese al módulo de `Ajustes -> Técnico -> Aciones planificadas`

![menú de ingreso](/docs/assets/accion_planificada/1_menu_accion_planificada.png)

-   La acción planificada se denomina __`Sincronizar ventas API MiTienda.pe`__, click sobre el registro para ingresar al formulario

![listado](/docs/assets/accion_planificada/2_listado_accion_planificada.png)

-   En el formulario puede verificar los datos de la acción planificada, también puede modificar los intervalos de tiempo, o fecha de proxima ejecución

__Nota importante:__ La fecha de próxima ejecución no se debe establecer en el pasado, caso contrario NO se ejecutará la acción planificada, siempre debe registrar una fecha a futuro

![formulario de acción planificada](/docs/assets/accion_planificada/4_accion_planifica.png)

### 6.2. Activar/Desactivar acción planificada

Si desea **Deshabilitar** la ejecución automática de la acción planificada, debe desmarcar la opción _**Activo**_

Una vez desactivada, la acción planificada dejará de ejecutarse de forma automática

![desactivar](/docs/assets/accion_planificada/accion_planificada_desactivo.png)

-   Para habilitar debe activar en el campo _**Activo**_, como se muestra en la imagen

![activar](/docs/assets/accion_planificada/accion_planificada_activo.png)

### 6.3. Ejecutar de forma manual

Se permite ejecutar la acción planificada de manera manual mediante el boton __`Ejecutar de forma manual`__

![sincronización manual](/docs/assets/accion_planificada/3_accion_planificada.png)
