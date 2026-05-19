[INNOVET] Etiqueta de liberación (CAF-11)

### 1. Información General

| Campo                 | Detalle             |
| --------------------- | ------------------- |
| Proyecto              | ab-forti            |
| Cliente               | INNOVET             |
| Versión de Odoo       | 19 / SH             |
| Tipo de desarrollo    | Nuevo               |
| Prioridad             | Alta                |
| Responsable Funcional | Diego Martinez      |
| Responsable Técnico   | Osvaldo Maye/Miguel |
| Fecha solicitud       | 20/Abril/26         |
| Fecha objetivo        | 25/Abril/26         |

---

### 2. Contexto del Negocio

| Campo                                 | Detalle                                                                                                                                                                                                                            |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ¿Por qué se necesita este desarrollo? | Innovet maneja diferentes etiquetas para los productos fabricados dependiendo el status del producto (aprobado, rechazado, validado, etc.). Por este motivo se necesitará el desarrollo de diferentes etiquetas según el producto. |
| Proceso actual                        | Actualmente no usan Odoo. Las etiquetas se usarán en la primera fase para la parte de fabricación.                                                                                                                                 |
| Problema detectado                    | Manejan muchas etiquetas dentro del área de calidad en fabricación.                                                                                                                                                                |
| Impacto si no se resuelve             | No hay una trazabilidad de los productos aprobados para liberación.                                                                                                                                                                |
| Objetivo del desarrollo               | Generar etiquetas cuando el producto se valide. Un botón o dos (aprobado o rechazado). Al hacer clic en el botón de aprobado, que genere la impresión de la etiqueta de validación.                                                |

---

### 3. Flujo Esperado (TO-BE)

Cuando el área de calidad apruebe que el producto cumple con las especificaciones y requisitos establecidos, una vez que se apruebe el control de calidad debe generar un botón de **Liberación**. Si damos clic, que se genere la etiqueta de aprobación.

**Características de la etiqueta:**

| Propiedad | Valor                          |
| --------- | ------------------------------ |
| Medida    | 101 mm largo x 52 mm ancho     |
| Color     | Verde (etiqueta de liberación) |

**Contenido de la etiqueta:**

| Campo                                        | Descripción                                         |
| -------------------------------------------- | --------------------------------------------------- |
| Texto "Control de calidad producto liberado" | Fijo, no se cambia                                  |
| Valida                                       | Inspector: persona que valida el control de calidad |
| Libero                                       | Coordinador: persona de manufactura                 |

**Video de referencia:**  
https://www.awesomescreenshot.com/video/51743787?key=2761bf88ae31d928a7db6c593b750dec

---

### 4. Reglas de Negocio

| Regla            | Descripción                                                |
| ---------------- | ---------------------------------------------------------- |
| Aplicar un botón | Al momento de validar el control de calidad en fabricación |

---

### 5. Detalle Técnico Requerido

| Elemento                  | Especificación                 |
| ------------------------- | ------------------------------ |
| Modelo(s) afectados       | Calidad, Fabricación           |
| Campos nuevos/modificados | Botones de liberación, rechazo |

---

### 6. Lógica / Comportamiento Esperado

Cuando el producto terminado se fabrica, antes de hacer la validación para pasarlo al almacén, pasa por un control de calidad.

Al momento de dar clic en la tecla de **"Aprobar"** o **"Falla"**:

- Si da clic en **Aprobar** → que genere el botón de **etiqueta de liberación**
- Si da clic en **Falla** → que genere el botón de **etiqueta de rechazo**

Una vez que demos clic al botón de liberación o falla, que genere la etiqueta correspondiente.

---

### 7. Impacto en Odoo

| Aplicación  | Impacto |
| ----------- | ------- |
| Calidad     | Sí      |
| Fabricación | Sí      |

---

### 8. Dependencias

| Tipo                    | Descripción                                                                   |
| ----------------------- | ----------------------------------------------------------------------------- |
| Otros desarrollos       | Los botones dependerán de este desarrollo y también de la etiqueta de rechazo |
| Configuraciones previas | Botones para generar la etiqueta                                              |
