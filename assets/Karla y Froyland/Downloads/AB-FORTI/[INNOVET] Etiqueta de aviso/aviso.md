[INNOVET] Etiqueta de aviso

### 📋 Especificación de Requerimientos: Módulo de Etiqueta de Aviso (Almacén)

**Información General del Proyecto**

- **Proyecto:** ab-forti
- **Cliente:** INNOVET
- **Versión de Odoo:** 19 / SH
- **Responsables:** Diego Martinez (Funcional), Osvaldo Maye / Miguel (Técnico)
- **Fechas:** Solicitud: 20/Abril/26 | Objetivo: 25/Abril/26
- **Prioridad:** Alta

**Contexto General**

Innovet requiere la implementación de una **"Etiqueta de Aviso"** para el área de Almacén/Entregas. Esta etiqueta se adhiere a todos los productos que ya están listos para su embarque y venta. Su objetivo es proporcionar una advertencia clara al cliente final sobre el manejo del producto, específicamente relacionada con la temperatura.

---

#### 1. Objetivo General

Desarrollar un botón en el módulo de Inventario (específicamente en las Órdenes de Entrega / Salidas) que permita imprimir un reporte en PDF estático con formato de etiqueta (102x152 mm) que contenga la advertencia de no exponer el producto al calor.

#### 2. Requerimientos Funcionales (Flujo TO-BE)

1. **Preparación del Embarque:** El equipo de almacén prepara una Orden de Entrega (`Delivery Order`) para enviar los productos al cliente.
2. **Validación:** Al momento de validar la salida del producto (o justo antes de embarcarlo), el usuario necesita imprimir la advertencia.
3. **Generación:** El usuario visualiza y hace clic en un botón llamado **"Etiqueta de aviso"** dentro de la orden de entrega.
4. **Impresión:** El sistema descarga inmediatamente un PDF con la etiqueta para ser enviada a la impresora (la cual estará cargada con rollo de etiquetas color amarillo).

#### 3. Requerimientos Técnicos (Odoo 19)

- **Modelos Involucrados:** `stock.picking` (Inventario / Transferencias).
- **Vistas (Views):**
  - Heredar la vista de formulario de `stock.picking`.
  - Agregar el botón **"Etiqueta de aviso"** (`action_print_warning_label`) en el `header` de la vista.
  - **Condición de visibilidad:** El botón debe estar visible de preferencia solo en transferencias de salida (donde `picking_type_code == 'outgoing'`).
- **Reporte QWeb (`ir.actions.report`):**
  - **Tipo:** PDF.
  - **Paperformat:** \* Width: 102 mm
    - Height: 152 mm (Nota: Esta etiqueta es más grande que las de calidad, formato vertical u horizontal según acomodo del texto).
    - Margins: Estándar para etiquetas.
  - **Mapeo de Datos en QWeb:**
    - **Contenido 100% Estático.** No requiere extraer datos de variables.
    - **Texto Único a mostrar:** "No exponer a fuentes de calor".
    - El diseño debe centrar este texto y hacerlo lo suficientemente grande y legible para cumplir su función de advertencia.

#### 4. Reglas de Negocio

- **Naturaleza Estática:** A diferencia de las etiquetas de calidad, esta etiqueta no cambia por lote, producto o cliente. Siempre imprime el mismo mensaje.
- **Ubicación:** Exclusiva para salidas/entregas, no es necesaria en recepciones ni fabricación interna.
- **Color Físico:** El diseño se realiza en texto negro convencional. El color amarillo que resalta la advertencia provendrá del tipo de papel (rollo amarillo) utilizado físicamente en la impresora.

#### 5. Criterios de Aceptación

- [ ] El botón "Etiqueta de aviso" aparece en las Órdenes de Entrega (`stock.picking` de salida).
- [ ] Al presionar el botón, se genera un PDF correctamente formateado a 102x152 mm.
- [ ] El PDF contiene únicamente el texto estático: "No exponer a fuentes de calor".
- [ ] No se producen errores al imprimir la etiqueta sin importar el estado de validación de la entrega.

---
