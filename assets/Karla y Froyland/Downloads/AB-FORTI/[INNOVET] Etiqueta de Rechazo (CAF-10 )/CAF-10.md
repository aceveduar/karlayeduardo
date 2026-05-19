[INNOVET] Etiqueta de Rechazo (CAF-10 )

---

### 📋 Especificación de Requerimientos: Módulo de Etiqueta de Rechazo MP (CAF-10)

**Información General del Proyecto**

- **Proyecto:** ab-forti (Innovet)
- **Cliente:** INNOVET
- **Versión de Odoo:** 19 / SH
- **Responsables:** Diego Martinez (Funcional), Osvaldo Maye / Miguel (Técnico)
- **Fechas:** Solicitud: 21/Abril/26 | Objetivo: 26/Abril/26
- **Prioridad:** Alta

**Contexto General**

Innovet requiere la implementación de la **"Etiqueta de Rechazo de MP" (CAF-10)** para el control de materiales comprados. Esta etiqueta se genera cuando la materia prima recibida no cumple con los estándares de calidad en la ubicación de inspección ("Storage") y debe ser identificada claramente para su devolución o disposición final.

---

#### 1. Objetivo General

Desarrollar un botón en el flujo de Control de Calidad de Inventario que permita imprimir una etiqueta de rechazo (PDF 101x52 mm) cuando un producto de compra sea marcado como "Falla", extrayendo automáticamente los datos del proveedor y el lote.

#### 2. Requerimientos Funcionales (Flujo TO-BE)

1. **Recepción:** Compras realiza el pedido y el equipo de Inventario recibe el producto en la ubicación temporal **Storage**.
2. **Control de Calidad:** Se realiza la inspección antes de mover al almacén general.
3. **Registro de la Falla:** Si el producto está roto o en malas condiciones, el usuario selecciona **"Falla" (Fail)** en el control de calidad e ingresa el porqué en el campo de **Notas**.
4. **Acción de Rechazo:** Al registrarse la falla, debe aparecer el botón **"Etiqueta de Rechazo"**.
5. **Impresión:** Al hacer clic, se genera el PDF configurado para el rollo de etiquetas rojas de 101x52 mm.

#### 3. Requerimientos Técnicos (Odoo 19)

- **Modelos Involucrados:** `quality.check`, `stock.picking` (Recepciones), `res.partner` (Proveedor), `stock.lot`.
- **Vistas (Views):**
  - Heredar la vista de Control de Calidad asociada a Recepciones de Compra.
  - El botón de impresión debe estar condicionado: **Visible solo si el estado es 'Falla' (Failed)**.
- **Reporte QWeb (`ir.actions.report`):**
  - **Tipo:** PDF.
  - **Paperformat:** Width: 101 mm | Height: 52 mm | Margins: Mínimos.
  - **Mapeo de Datos en QWeb (Según imagen CAF-10):**
    - **Texto Fijo Superior:** (Según el diseño de tabla superior del cliente).
    - **Texto Fijo Central:** "Control de calidad producto rechazado".
    - **MOTIVO:** Extraer del campo de notas/comentarios del control de calidad (`notes`).
    - **MATERIAL:** Nombre del producto (`product_id.name`).
    - **PROVEEDOR:** Nombre del proveedor asociado a la compra/recepción (`partner_id.name`).
    - **N° LOTE:** Número de lote asignado en la entrada (`lot_id.name`).
    - **FECHA:** Fecha de la inspección.
    - **VÁLIDO / RECHAZA:** Nombre del usuario que realizó la validación del control (`user_id.name`).

#### 4. Reglas de Negocio

- **Ubicación Crítica:** La funcionalidad debe estar activa en la etapa de "Storage" (tránsito antes de almacén).
- **Dependencia de Acción:** El botón para generar esta etiqueta es dependiente de que el control de calidad sea marcado como fallido. Si es aprobado (Pass), este botón no debe mostrarse.
- **Color Físico:** El diseño del reporte es monocromático (negro). La alerta visual se da por el uso físico de papel rojo en la impresora.

#### 5. Criterios de Aceptación

- [ ] El botón de "Etiqueta de Rechazo" solo aparece cuando el control de calidad en recepciones falla.
- [ ] El sistema extrae correctamente el nombre del Proveedor desde el documento de recepción (`stock.picking`).
- [ ] El campo "Motivo" en la etiqueta refleja fielmente lo escrito en las notas del control de calidad.
- [ ] El formato de salida es un PDF de 101x52 mm que respeta el diseño de la etiqueta CAF-10.
- [ ] El número de lote y la fecha se muestran correctamente según los datos del registro.

---
