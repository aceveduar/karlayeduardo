# CLAUDE.md — Boda Karla & Eduardo

## Proyecto
Landing page de invitación de boda. Archivo único `index.html` (HTML + CSS + JS inline).
Debe poder embeberse en Odoo sin conflictos de estilos.

## Decisiones de arquitectura

### CSS: BEM puro (sin Tailwind)
Tailwind fue eliminado completamente. Todo el CSS usa nomenclatura BEM con prefijos cortos
para garantizar aislamiento total al renderizar dentro de Odoo.

**Bloques definidos:**
| Bloque BEM        | Propósito                              |
|-------------------|----------------------------------------|
| `invitation`      | Contenedor principal                   |
| `floral-band`     | Imágenes decorativas superior/inferior |
| `inv-header`      | Sección de encabezado, monograma, foto |
| `ornament-divider`| Separadores florales SVG               |
| `names-display`   | Nombres en tipografía script           |
| `event-date`      | Fecha destacada (Sábado 20 Diciembre)  |
| `countdown`       | Contador regresivo en tiempo real      |
| `photo-break`     | Fotos de stock entre secciones         |
| `event-info`      | Dirección y hora del evento            |
| `timeline`        | Itinerario alternado izquierda/derecha |
| `story`           | Sección "Nuestra Historia"             |
| `dresscode`       | Código de vestimenta con paleta visual |
| `gifts`           | Datos bancarios para regalos           |
| `rsvp`            | Confirmación de asistencia via Odoo    |
| `inv-footer`      | Pie de página con agradecimiento       |
| `music-player`    | Botón flotante de reproducción         |
| `btn`             | Componente de botón reutilizable       |

### Design tokens (CSS custom properties)
Todos los valores de color, fuente y sombra están centralizados en `:root` con variables
prefijadas `--c-` (colores) y `--f-` (fuentes). Cambiar un valor actualiza toda la página.

**Paleta:**
- Fondo pergamino: `#f7f4ee`
- Terracota principal: `#b76e49`
- Terracota oscuro (hover): `#9a5c3a`
- Fondo exterior: `#8b7355`

**Tipografías (Google Fonts):**
- Playfair Display — fechas, tiempos, monograma
- Great Vibes — nombres Karla y Eduardo
- Montserrat — cuerpo de texto

### Animaciones
Clase utilitaria `.js-fade` + `IntersectionObserver`. Al entrar al viewport el elemento
recibe `.is-visible` (fade-in + slide-up). Una vez visible, deja de observarse.

### Countdown
IIFE autónomo. Fecha objetivo: `2025-12-20T17:00:00` (hora local del dispositivo).
IDs: `#cd-days`, `#cd-hours`, `#cd-min`, `#cd-sec`.

### Music player
Botón flotante fijo (bottom-right). Audio loop de ejemplo (bensound). El usuario puede
reemplazar el `<source src>` con cualquier archivo MP3 propio.

### RSVP / Odoo
El botón apunta a `https://tu-empresa.odoo.com/event/boda-karla-eduardo/register`.
**Pendiente:** reemplazar con la URL real del evento creado en Odoo > Eventos.

## TODOs pendientes (a completar por el cliente)

- [ ] Reemplazar fotos de Unsplash con fotos reales de la pareja
- [ ] Actualizar datos bancarios en sección `gifts` (banco, CLABE, titular)
- [ ] Actualizar link de Google Maps en botón "Ver ubicación"
- [ ] Actualizar URL de Odoo en botón "Confirmar mi asistencia"
- [ ] Reemplazar audio de ejemplo con la canción elegida por la pareja
- [ ] Actualizar años y textos de "Nuestra Historia" con los reales

## Integración con Odoo
Para embeber en Odoo sin conflictos:
1. Todos los bloques BEM usan nombres únicos (no coinciden con clases de Bootstrap/Odoo).
2. No hay variables globales JS expuestas (todo en IIFEs).
3. No hay dependencias externas salvo Google Fonts.
4. Las fuentes pueden cargarse localmente si Odoo bloquea dominios externos.
