# Documentación Técnica — Boda Karla & Eduardo

> Sistema completo de invitación digital premium + gestión de boda.  
> Stack: HTML5 · Vanilla JS (ES6+) · CSS3 · Supabase (PostgreSQL) · PWA

---

## Índice

1. [Arquitectura general](#1-arquitectura-general)
2. [Base de datos (Supabase)](#2-base-de-datos-supabase)
3. [index.html — Invitación pública](#3-indexhtml--invitación-pública)
   - 3.1 [Secciones HTML](#31-secciones-html)
   - 3.2 [Módulos JavaScript](#32-módulos-javascript)
4. [admin.html — Panel de administración](#4-adminhtml--panel-de-administración)
   - 4.1 [Estructura de la app shell](#41-estructura-de-la-app-shell)
   - 4.2 [Tabs y su contenido](#42-tabs-y-su-contenido)
   - 4.3 [Funciones JavaScript](#43-funciones-javascript)
5. [sw.js — Service Worker](#5-swjs--service-worker)
6. [manifest.json — PWA](#6-manifestjson--pwa)
7. [Identidad visual y sistema de diseño](#7-identidad-visual-y-sistema-de-diseño)
8. [Variables de entorno y credenciales](#8-variables-de-entorno-y-credenciales)

---

## 1. Arquitectura general

```
┌─────────────────────────────────────────────────────┐
│  Invitado (WhatsApp link)                           │
│  index.html?code=GARCIA-01                          │
│  └─ RSVP → Supabase (families + rsvps)             │
└─────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────┐
│  Eduardo (admin)                                    │
│  admin.html                                         │
│  └─ CRUD · Mesas · Check-in QR · Fotos · Mensajes  │
│     → Supabase (families + rsvps + messages)        │
│     → Supabase Storage (fotos-boda bucket)          │
└─────────────────────────────────────────────────────┘
```

- **Sin servidor propio.** Todo es estático + Supabase REST API.
- **Sin frameworks.** Vanilla JS ES6+ en ambos archivos.
- **Mobile-first.** El canal principal de distribución es WhatsApp.
- **PWA.** La invitación se puede instalar en pantalla de inicio (manifest + service worker).

---

## 2. Base de datos (Supabase)

### Tabla `families`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | UUID PK | Identificador único |
| `code` | TEXT UNIQUE | Código de invitación (ej. `GARCIA-01`) |
| `family_name` | TEXT | Nombre completo de la familia |
| `max_guests` | INTEGER | Pases asignados |
| `confirmed` | BOOLEAN | ¿Ya confirmó (o fue marcada)? |
| `group_name` | TEXT | Segmento: Familia novia / novio / Amigos novia / novio / Trabajo / Otros |
| `phone` | TEXT | WhatsApp sin código de país |
| `guest_names` | TEXT | Nombres separados por coma |
| `notes` | TEXT | Notas internas (dieta, accesibilidad, etc.) |
| `checked_in` | BOOLEAN | Llegó al evento el día de la boda |
| `checked_in_at` | TIMESTAMPTZ | Hora de llegada registrada por QR |
| `table_number` | INTEGER | Mesa asignada (1–20) |
| `created_at` | TIMESTAMPTZ | Auto-generado |

### Tabla `rsvps`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | UUID PK | Identificador único |
| `family_id` | UUID FK | Referencia a `families.id` |
| `contact_name` | TEXT | Nombre de quien confirmó |
| `guest_count` | INTEGER | Cuántos asistirán |
| `attending` | BOOLEAN | `true` = asiste · `false` = no asiste |
| `attending_names` | TEXT | Nombres de quienes asisten (separados por coma) |
| `created_at` | TIMESTAMPTZ | Auto-generado |

### Tabla `messages`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | UUID PK | Identificador único |
| `name` | TEXT | Nombre del invitado que escribió |
| `message` | TEXT | Contenido del mensaje |
| `created_at` | TIMESTAMPTZ | Auto-generado |

### Relaciones

```
families (1) ──── (N) rsvps      via family_id
families (1) ──── (N) messages   [sin FK — el nombre es texto libre]
```

---

## 3. index.html — Invitación pública

Archivo de ~5 200 líneas. Contiene todo el HTML, CSS y JS de la invitación que recibe cada invitado.

### 3.1 Secciones HTML

#### `<head>` — Meta y recursos

| Elemento | Descripción |
|----------|-------------|
| `<link rel="preload">` | Precarga `flores-5.webp`, `flores-1.webp`, `novios.webp` (above-the-fold) |
| `<link rel="manifest">` | Enlaza `manifest.json` para soporte PWA |
| Open Graph tags | `og:title`, `og:image`, `og:description` para el preview en WhatsApp |
| Google Fonts | Playfair Display · Montserrat · Great Vibes |

#### `#js-reveal` — Overlay de revelación de página

Pantalla negra que desaparece en 120 ms con fade-out de 1.1 s. Evita el flash de contenido sin estilos.

#### `#gold-canvas` — Partículas doradas

`<canvas>` fullscreen fijo detrás de todo el contenido. Las partículas flotan suavemente usando la Canvas API.

#### `#rsvp-fab` — Botón flotante RSVP

Botón dorado fijo en la esquina inferior derecha. Lleva al usuario directo a la sección RSVP con scroll suave. Se oculta automáticamente cuando el usuario llega a la sección RSVP o cuando el deadline venció (20 sep 2026).

#### `#js-music-player` — Reproductor de música

Botón circular fijo en la esquina inferior izquierda. Muestra ícono de nota musical (play) o pausa. Intenta autoplay al primer toque del usuario en la página.

#### `<main class="invitation">` — Cuerpo de la invitación

Contiene todas las secciones en orden:

---

##### `.inv-header` — Encabezado principal

El bloque visual más importante de la invitación. Estructura interna:

1. **Top floral band** — `flores-5` izq + `flores-1` der + `flores-4` centro, con `mix-blend-mode: multiply`
2. **Monograma K|E** — Iniciales con separador dorado y texto "¡Nos Casamos!"
3. **Foto de la pareja** — `novios.webp`, 96% de ancho, con marco dorado
4. **Floral ornament** — `flores-4` encima de los nombres
5. **Nombres** — "Karla & Eduardo" en Great Vibes con animación shimmer dorado
6. **Floral ornament invertido** — `flores-4` con `transform: scaleX(-1)` debajo de los nombres
7. **Texto de invitación** — párrafo principal "Con el corazón lleno de alegría..."
8. **Versículo** — Colosenses 3:14
9. **Padres** — Padres de la novia y del novio en dos columnas
10. **Degradado de transición** — `::after` del header que va de pergamino a oscuro

El encabezado usa `::before` con un patrón diagonal dorado sobre fondo pergamino.

---

##### `#js-countdown` — Countdown

Sección oscura con cuatro contadores animados: días · horas · minutos · segundos. Cada número tiene una animación `flip` al cambiar. Cuando la fecha llega a cero agrega la clase `.countdown--is-done` y muestra el mensaje de día de boda.

**Destino:** 21 de noviembre de 2026 a las 17:30 hrs.

---

##### `.photo-break` — Separadores fotográficos

Dos bloques de imagen a pantalla completa (`photo-break-1` y `photo-break-2`) que dividen las secciones de contenido. Usan `object-fit: cover` con paralax visual en desktop.

---

##### `.event-details` — Detalles del evento

Tres tarjetas de información:
- **Fecha y hora** — Sábado 21 de noviembre 2026 · 17:30 hrs
- **Lugar** — Hacienda Zerezotla, San Andrés Cholula, Puebla
- **Botones de acción** — "Agregar al calendario" (descarga `.ics`) + "Cómo llegar" (Google Maps)

Incluye también una tarjeta animada del mapa del venue dibujada con Canvas API (20 mesas + pista de baile).

---

##### `.how-to-get` — Cómo Llegar

Tres tarjetas informativas con bordes dorados:
- **Hospedaje recomendado** — Hotel Camino Real Puebla
- **Estacionamiento** — Gratuito en el venue
- **Cómo llegar** — Instrucciones con bullets de punto dorado + link a Google Maps

---

##### `.itinerary` — Itinerario del evento

Timeline vertical con cinco momentos del día:
1. 17:30 — Recepción y cóctel
2. 18:00 — Boda civil
3. 18:40 — Comida
4. 19:30 — Fiesta y baile
5. 01:30 AM — Salida

---

##### `.our-story` — Nuestra Historia

Cuatro tarjetas en grid 2×2 con los momentos clave de la pareja:
1. **El Encuentro** — Primer momento juntos
2. **Crecer Juntos** — La relación
3. **La Propuesta** — El compromiso
4. **21·Nov·2026** — La boda

---

##### `.gallery` — Galería de fotos

Grid de fotos de la pareja con layout responsivo (filas de distinto número de columnas). Cada imagen tiene `data-gallery-index` para activar el lightbox al hacer tap. Usa `loading="lazy"` en todas las imágenes excepto las above-the-fold.

---

##### `#gallery-lightbox` — Lightbox de fotos

`<div>` hijo directo de `<body>` (no de `.invitation`) para evitar el bug de `transform` containment. Muestra la foto en pantalla completa con:
- Navegación anterior/siguiente (botones + teclado + swipe touch)
- Contador "X / N"
- Botón cerrar
- Cierre al hacer tap en el fondo

---

##### `.dresscode` — Dress Code

Sección "Semi Formal" con:
- Dos filas de swatches de colores (sugeridos y a evitar)
- Colores prohibidos indicados con tachado: Blanco ✕ · Beige ✕

---

##### `.gifts` — Regalos

Dos tarjetas:
1. **Mesa de Regalos Amazon** — Link directo a la lista
2. **Transferencia bancaria** — CLABE + número de cuenta (copiables)

---

##### `.guestbook` — Libro de Visitas

Formulario de mensaje pre-boda con:
- Campo de nombre
- Textarea de mensaje (máx. 500 caracteres con contador)
- Lista de mensajes anteriores (cargados desde Supabase)
- Estado de éxito tras enviar

---

##### `#rsvp` — Formulario RSVP

El flujo más complejo de la invitación. Tiene 6 pasos (solo uno visible a la vez):

| Paso | ID | Descripción |
|------|----|-------------|
| Verificar código | `rsvp-step-code` | Input de código + botón verificar |
| Formulario | `rsvp-step-form` | Nombre · selección de asistentes · counter de pases |
| Éxito | `rsvp-step-success` | Ticket digital + QR + mesa asignada |
| Ya confirmado | `rsvp-step-already` | Muestra el ticket existente |
| Declinado | `rsvp-step-declined` | Mensaje de no asistencia |
| Cerrado | `rsvp-step-closed` | Se muestra cuando el deadline (20 sep 2026) venció |

Los indicadores de progreso (3 dots) se actualizan en cada paso.

El **ticket digital** (paso éxito/ya confirmado) es un `<canvas>` generado en JS con: nombres de la pareja · fecha · hora · lugar · mesa asignada · código QR con el código único de la familia. Tiene botón para compartir (Web Share API) o descargar como imagen.

---

### 3.2 Módulos JavaScript

Todos los módulos en `index.html` son IIFEs (immediately invoked function expressions) para mantener el scope aislado.

---

#### Módulo: Mapa animado del venue

**Función:** `window.drawVenueMap(el, highlight)`  
**Propósito:** Dibuja en un `<canvas>` el plano de Hacienda Zerezotla con las 20 mesas, la pista de baile y las sillas animadas con un efecto de pulso.

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `el` | HTMLCanvasElement | Canvas donde dibujar |
| `highlight` | number \| null | Número de mesa a resaltar en dorado |

**Función interna:** `gLine(y1, y2)`  
Dibuja una línea divisoria horizontal con gradiente transparente→dorado→transparente.

**Función interna:** `frame()`  
Loop de animación con `requestAnimationFrame`. Dibuja el fondo, las líneas, la pista de baile, las mesas (círculos) y las sillas (círculos pequeños). La mesa resaltada pulsa suavemente usando `Math.sin(phase)`.

**Función:** `window.stopMapAnim()`  
Cancela el loop de animación. Se llama cuando el canvas sale del viewport.

---

#### Módulo: Lightbox de galería

**Función:** `getGalleryPhotos() → string[]`  
Lee los `src` actuales de todas las imágenes `.gallery__img`. Opera en runtime para ser compatible con fotos cargadas desde Supabase Storage.

**Función:** `openLightbox(index)`  
Abre el lightbox en la posición `index`. Agrega `.is-open` al overlay y bloquea el scroll del body.

**Función:** `closeLightbox()`  
Cierra el lightbox. Quita `.is-open` y restaura el scroll.

**Función:** `showPhoto(index)`  
Precarga la imagen en un `Image()` temporal antes de asignarla al `<img>` visible. Muestra el spinner de carga (`.is-loading`) hasta que `onload` dispara.

**Eventos registrados:**
- `click` en cada `[data-gallery-index]` → `openLightbox(index)`
- `click` en `#lightbox-close` → `closeLightbox()`
- `click` en `#lightbox-prev` / `#lightbox-next` → navega con wrap circular
- `click` en el fondo del lightbox → `closeLightbox()`
- `keydown` Escape / ArrowLeft / ArrowRight
- `touchstart` + `touchend` → swipe horizontal con umbral de 40 px; ignora movimientos más verticales que horizontales (no interfiere con scroll)

---

#### Módulo: Reproductor de música

**Función:** `fadeIn(targetVol, durationMs)`  
Sube el volumen gradualmente de 0 a `targetVol` en `durationMs` ms usando 60 pasos con `setInterval`.

**Función:** `tryAutoStart()`  
Intenta reproducir el audio automáticamente. Si el navegador lo permite (algunos permiten autoplay en móvil tras interacción previa), inicia el fade-in a volumen 0.4. Si falla silenciosamente, espera el primer toque del usuario.

**Evento:** Primer `click` en `document` → llama a `tryAutoStart()` y se desregistra.  
**Evento:** `click` en `#js-music-btn` → alterna play/pause con fade-in o pausa directa.

---

#### Módulo: Libro de Visitas (invitados)

**Función:** `esc(s) → string`  
Escapa caracteres HTML (`&`, `<`, `>`, `"`) para prevenir XSS al insertar texto en innerHTML.

**Función:** `loadMessages()`  
Consulta `GET /rest/v1/messages?order=created_at.desc&limit=50` y renderiza las tarjetas en `#guestbook-list`.

**Eventos:**
- `input` en el textarea → actualiza contador de caracteres
- `click` en botón "Otro nombre" → limpia el nombre y foca el input
- `click` en botón "Enviar" → valida campos → `POST /rest/v1/messages` → muestra estado éxito

---

#### Módulo: Saludo personalizado

Lee el parámetro `?code=` de la URL, consulta `families?code=eq.XXXX&select=family_name` y muestra el saludo "¡Hola, Familia García!" en `#js-greeting`. Si no hay código o no existe en BD, el elemento permanece oculto.

---

#### Módulo: Agregar al calendario

**Evento:** `click` en `#btn-calendar`  
Genera un archivo `.ics` (iCalendar) con los datos del evento, crea un `Blob`, genera una URL temporal y simula click en un `<a download>`. Descarga `boda-karla-eduardo.ics`.

Datos del evento en el ICS:
- `DTSTART`: 2026-11-21T17:30:00 (America/Mexico_City)
- `DTEND`: 2026-11-22T01:30:00
- `LOCATION`: Calle 15 Poniente #1531, San Andrés Cholula, Puebla

---

#### Módulo: Page Reveal

Selecciona `#js-reveal`, espera 1 frame + 120 ms y hace fade-out (`opacity: 0`) durante 1.1 s. Luego elimina el elemento del DOM.

---

#### Módulo: Countdown

**Variable:** `WEDDING = new Date("2026-11-21T17:30:00")`

**Función:** `pad(n) → string`  
Devuelve `n` como string de 2 dígitos con cero inicial.

**Función:** `setVal(el, val)`  
Actualiza el texto del elemento solo si cambió. Agrega la clase `.countdown__number--flip`, fuerza reflow (`void el.offsetWidth`) y la quita para reiniciar la animación CSS cada segundo.

**Función:** `tick()`  
Calcula `diff = WEDDING - Date.now()`. Si `diff <= 0` agrega `.countdown--is-done` al wrapper y cancela el intervalo. En caso contrario llama a `setVal` para cada unidad de tiempo.

El ticker corre con `setInterval(tick, 1000)`.

---

#### Módulo: Scroll fade-in (Intersection Observer)

Observa todos los elementos `.js-fade` con `threshold: 0.1` y `rootMargin: "0px 0px -40px 0px"`. Al entrar en el viewport agrega `.is-visible` y deja de observar el elemento.

---

#### Módulo: RSVP FAB (botón flotante)

**Variable:** `FAB_DEADLINE = new Date("2026-09-20T23:59:00")`

**Función:** `window._fabHidePermanent()`  
Agrega `.is-hidden` al FAB, lo saca del flujo (`display: none`) y desconecta el observer. Se llama cuando el usuario llega a un paso terminal del RSVP (éxito, declinado, ya confirmado, cerrado) o cuando el deadline venció.

Si la fecha actual supera el deadline, llama a `_fabHidePermanent()` inmediatamente y no registra el observer.

El **`IntersectionObserver`** observa `#rsvp`: cuando la sección es visible agrega `.is-hidden` al FAB; cuando sale del viewport la quita.

---

#### Módulo: RSVP (flujo completo)

El módulo más extenso del archivo. Gestiona todo el flujo de confirmación de asistencia.

**Variables de estado:**
- `family` — objeto de la familia consultada (o `null`)
- `guestCount` — número de pases seleccionados
- `selectedMembers` — array de nombres que asistirán
- `RSVP_DEADLINE` — `new Date("2026-09-20T23:59:00")`

---

**Función:** `showStep(id)`  
Oculta todos los pasos `.rsvp-step` y muestra el identificado por `id`. Actualiza los 3 dots de progreso según el mapa `{ code: 1, form: 2, success: 3, already: 3 }`. En pasos terminales llama a `_fabHidePermanent()`.

---

**Función:** `api(path, opts) → Promise`  
Wrapper de `fetch` para Supabase REST. Agrega automáticamente `apikey`, `Authorization` y `Content-Type`. Lanza error si la respuesta no es `ok`.

---

**Función:** `patch(table, filter, data) → Promise`  
Wrapper `PATCH` para Supabase. Construye la URL como `table?filter` y envía el body como JSON.

---

**Función:** `updateCounter()`  
Actualiza el texto de `#rsvp-count` con el valor de `guestCount`. Habilita/deshabilita los botones `−` y `+` según los límites `[1, family.max_guests]`.

---

**Función:** `buildMemberList(names)`  
Construye la lista interactiva de invitados en `#rsvp-member-list`. Cada fila es un `<div class="member-row">` con un checkmark SVG, el nombre y la etiqueta "No asistirá". Al hacer click en una fila: si estaba seleccionada la quita de `selectedMembers`, aplica clase `.is-off` y muestra la etiqueta; si no estaba, la agrega y restaura el estado. Llama a `updateMemberLbl()` y `updateSubmitBtn()` tras cada cambio.

---

**Función:** `updateMemberLbl()`  
Actualiza el label de pases: **"X de N pases seleccionados"**.

---

**Función:** `updateSubmitBtn()`  
Deshabilita el botón de confirmación si `guestCount === 0`.

---

**Evento (Paso 1 — Verificar código):**  
`click` en `#rsvp-code-btn` → Normaliza el código a mayúsculas → `GET families?code=eq.CODIGO&select=*` → Si no existe muestra error. Si ya tiene RSVP va al paso `already`. De lo contrario carga la familia en `family`, pre-llena el nombre si hay `guest_names` (usa `buildMemberList`), y va al paso `form`.

---

**Evento (Paso 2 — Formulario):**  
`click` en `#rsvp-submit-btn` →  
1. Valida que haya nombre de contacto  
2. `PATCH families?id=eq.UUID` con `{ confirmed: true }`  
3. `POST rsvps` con `{ family_id, contact_name, guest_count, attending: true, attending_names }`  
4. Refresca datos de la familia  
5. `buildTicketCanvas()` con los datos actualizados  
6. Va al paso `success`

---

**Evento (Paso 2 — No asistir):**  
`click` en `#rsvp-decline-btn` →  
1. `PATCH families?id=eq.UUID` con `{ confirmed: true }`  
2. `POST rsvps` con `{ attending: false, guest_count: 0 }`  
3. Va al paso `declined`

---

**Función:** `buildTicketCanvas()`  
Dibuja el ticket digital en `#ticket-canvas` (600×340 px) usando Canvas API:
- Fondo degradado oscuro
- Líneas de adorno doradas con gradiente transparente
- Foto de la pareja (si está disponible)
- Nombre de la familia en Playfair Display
- Filas de datos: FECHA · HORA · LUGAR
- Mesa asignada (si hay)
- Código QR generado con QRCode.js

---

**Función:** `shareOrDownload(canvas)`  
Intenta `navigator.share({ files: [blob] })`. Si el dispositivo no soporta Web Share API llama a `_fallbackSave(canvas)`.

**Función:** `_fallbackSave(canvas)`  
Convierte el canvas a URL, crea un `<a download="ticket-boda.png">` y simula click.

---

#### Módulo: Partículas doradas

IIFE que inicializa un sistema de partículas en `#gold-canvas`.

**Función:** `rand(a, b) → number`  
Genera un número aleatorio entre `a` y `b`.

**Función:** `resize()`  
Ajusta el canvas al tamaño de la ventana. Se llama en `init()` y en `window.resize`.

**Función:** `make() → object`  
Crea una partícula con posición aleatoria, velocidad, radio, opacidad y un ángulo de oscilación.

**Función:** `init()`  
Inicializa el array de partículas (densidad calculada según área de pantalla) y arranca el loop.

**Función:** `loop()`  
Loop de animación con `requestAnimationFrame`. Limpia el canvas y dibuja cada partícula. Cada partícula avanza verticalmente, oscila horizontalmente según `Math.sin(phase)`, y se reinicia al salir de la pantalla.

---

#### Módulo: Service Worker

```js
window.addEventListener("load", function () {
    navigator.serviceWorker.register("./sw.js")
});
```

Registra el service worker para soporte PWA offline.

---

## 4. admin.html — Panel de administración

Archivo de ~5 100 líneas. App shell con navegación por tabs. Solo accesible con contraseña.

### 4.1 Estructura de la app shell

```
┌──────────────────────────────────────┐
│  #app-header (56px fijo)             │
│  ← Invitación   K&E   ☀/🌙   ⚙     │
├──────────────────────────────────────┤
│  .tab-content                        │
│  (overflow-y: auto)                  │
│  └─ #tab-resumen (activo por defecto)│
│  └─ #tab-familias                    │
│  └─ #tab-mesas                       │
│  └─ #tab-fotos                       │
│  └─ #tab-mensajes                    │
├──────────────────────────────────────┤
│  .bottom-nav (62px fijo)             │
│  📊 Resumen  👥 Familias  🪑 Mesas   │
│  📸 Fotos    💬 Mensajes             │
└──────────────────────────────────────┘
```

El panel completo (`#panel`) usa `position: fixed; inset: 0`. El tab activo es el único con clase `.is-active`.

**Persistencia de tab:** El tab activo se guarda en `localStorage("ke-tab")`. Al hacer login se restaura el último tab visitado.

### 4.2 Tabs y su contenido

#### Tab 1: Resumen (`#tab-resumen`)

- **Hero countdown** — Días restantes para la boda (calculado al cargar)
- **Alertas contextuales** — Banner rojo/ámbar con familias sin confirmar o confirmadas sin mesa
- **4 tarjetas de estadísticas** — Familias confirmadas · Pendientes · Pases confirmados · Check-in
- **3 barras de progreso** — Familias confirmadas / total · Pases invitados / capacidad · Personas confirmadas / capacidad
- **Alerta sin mesa** — Familias confirmadas sin mesa asignada (enlace al tab de mesas)
- **Sección de recordatorios** — Lista de pendientes con botón WhatsApp por cada uno
- **Acciones rápidas** — Botón Actualizar datos + Exportar CSV
- **Modo Check-in** — Abre el overlay de check-in del día del evento
- **Cerrar sesión** — Limpia localStorage y vuelve al gate

#### Tab 2: Familias (`#tab-familias`)

- **Barra de herramientas** — Botón "Nueva Familia" (abre el modal)
- **Filtros de grupo** — Chips horizontales con scroll: Todos · Novia · Novio · Amigos novia · Amigos novio · Trabajo · Otros · **Sin confirmar**
- **Barra de acción masiva** — Visible solo con el chip "Sin confirmar". Muestra el conteo y el botón "Marcar todas como No asiste"
- **Búsqueda** — Input en tiempo real que filtra por nombre o código
- **Contador** — "X familias · Y confirmadas · Z pendientes"
- **Lista de tarjetas** — Una tarjeta por familia, ordenadas: pendientes → confirmadas → declinadas

Cada tarjeta muestra:
- Nombre + badge de estado (Pendiente / Confirmada / No asiste)
- Grupo + mesa + pases
- Botón código (copia el link de invitación)
- Botón WhatsApp (genera el mensaje pre-armado)
- Botón "Detalle" (despliega panel con toda la info + editar)
- Botón "✕" eliminar (solo en pendientes)

El panel de detalle muestra: teléfono · grupo · mesa · quién confirmó · pax confirmados · fecha RSVP · lista de asistencia por persona · notas.

#### Tab 3: Mesas (`#tab-mesas`)

- **Stats rápidos** — Mesas ocupadas · Pax asignados · Lugares libres
- **Banner sin mesa** — Familias confirmadas sin mesa
- **Banner capacidad excedida** — Si alguna mesa supera 12 pax
- **Leyenda de colores** — Vacía · Parcial · Llena · Excedida
- **Grid de 20 tarjetas** — Una por mesa con: número · pax/12 · barras de asientos · nombres de familias

Al tocar una mesa se abre el **Mesa Detail Bottom Sheet** con:
- Barra de capacidad con color semántico
- Lista de familias en esa mesa (con botón "Quitar")
- Dropdown para asignar una familia sin mesa

#### Tab 4: Fotos (`#tab-fotos`)

Grid de slots de fotos para cargar desde el dispositivo a Supabase Storage. Slots disponibles:
- `portada` — Foto de Portada
- `galeria-0` a `galeria-6` — Fotos de la galería

Cada slot muestra la vista previa si tiene foto, o un placeholder. Permite subir (comprimida a 1200px/82%) o eliminar.

#### Tab 5: Mensajes (`#tab-mensajes`)

- Lista de mensajes del libro de visitas con nombre · texto · fecha
- Búsqueda en tiempo real
- Botón eliminar por mensaje
- Badge en el nav con mensajes nuevos desde la última visita al tab

---

### 4.3 Funciones JavaScript

#### Autenticación y sesión

**Función:** `enterPanel()`  
Guarda `"ke-admin": "1"` en `localStorage`, oculta el gate, muestra el panel con `.is-visible` y llama a `loadData()`.

**Función:** `exitPanel()`  
Elimina `"ke-admin"` de `localStorage`, limpia el intervalo de auto-refresh, muestra el gate y oculta el panel.

**Auto-login:** Al cargar la página, si `localStorage.getItem("ke-admin") === "1"` llama a `enterPanel()` directamente.

**Tema al inicio:**
```js
(function () {
    var t = localStorage.getItem("ke-theme") || "light";
    document.documentElement.setAttribute("data-theme", t);
})();
```
Aplica el tema antes del primer render para evitar flash.

---

#### Utilidades globales

**Función:** `api(path) → Promise<any>`  
`GET` a `SUPABASE_URL + "/rest/v1/" + path` con headers de autenticación. Lanza error si `!r.ok`.

**Función:** `esc(s) → string`  
Escapa `&`, `<`, `>` en strings para inserción segura en innerHTML.

**Función:** `showToast(msg)`  
Crea un `<div>` toast fijo centrado en la parte inferior, lo inserta en el body, hace fade-out a los 3 s y lo elimina a los 3.4 s.

---

#### Carga de datos

**Función async:** `loadData()`  
Consulta `families?select=*,rsvps(*)&order=family_name.asc` → guarda en `allData` → llama a `renderStats` + `renderProgress` + `renderTable`. En el primer login restaura el tab guardado en `localStorage`.

**Auto-refresh:** `setInterval(loadData, 60000)`. Compara el conteo de confirmados con `lastConfirmedCount` y muestra un toast de celebración si hay nuevas confirmaciones.

---

#### Estadísticas y resumen

**Función:** `renderStats(data)`  
Actualiza las 4 tarjetas del tab Resumen:
- Confirmadas (verde si > 0)
- Pendientes (ámbar si > 5, neutral si ≤ 5, verde si = 0)
- Pax confirmados
- Check-in (calculado sobre familias con `checked_in: true`)

También genera el banner de alertas contextuales y llama a `updatePendingBadge`.

**Función:** `renderProgress(data)`  
Actualiza las 3 barras de progreso:
1. **Familias** — confirmadas / total (porcentaje)
2. **Pases invitados** — sum de `max_guests` / capacidad total (20 mesas × 12 = 240). Rojo si supera capacidad
3. **Personas confirmadas** — sum de `guest_count` en RSVPs con `attending: true` / 240

También actualiza el banner "sin mesa" en el tab Resumen.

---

#### Links y WhatsApp

**Función:** `getSiteUrl() → string`  
Lee la URL del sitio desde `localStorage("ke-site-url")` o del input de configuración. Elimina el `/` final.

**Función:** `buildLink(code) → string`  
Combina `getSiteUrl()` + `"?code=" + code`. Si no hay URL configurada devuelve solo `"?code=CODIGO"`.

**Función:** `copyLink(code, btn)`  
Copia `buildLink(code)` al portapapeles usando `navigator.clipboard.writeText`. Cambia el texto del botón a "✓ Copiado" por 2 s. Fallback: `prompt()`.

**Función:** `famCopyLink(code, id)`  
Igual que `copyLink` pero actualiza el botón de código de la tarjeta de familia (que incluye el ícono SVG).

**Función:** `buildWaUrl(family, code, phone, tableNum) → string`  
Construye la URL `wa.me` con un mensaje pre-armado que incluye:
- Saludo con el nombre de la familia
- Fecha, hora, lugar
- Mesa asignada (si hay)
- Link personalizado

Normaliza el teléfono: si tiene más de 10 dígitos lo usa tal cual, si no le agrega `"52"` (México).

**Función:** `groupBadge(g) → string`  
Devuelve el HTML de un `<span class="group-badge">` con color y fondo según el grupo. Colores definidos en `GROUP_COLORS`.

---

#### Lista de familias

**Función:** `renderTable(data)`  
Renderiza la lista de tarjetas en `#fam-list`. Ordena: pendientes → confirmadas → declinadas (dentro de cada grupo, alfabético por nombre). Cada tarjeta construida con `innerHTML` contiene el panel de detalle colapsado.

**Función:** `toggleFamDetail(id)`  
Cierra todos los paneles de detalle abiertos, luego abre el del ID especificado (o lo cierra si ya estaba abierto). Actualiza el botón "Detalle" / "Cerrar ✕".

**Función:** `buildFamDetailContent(f) → string`  
Genera el HTML del panel de detalle para tarjetas mobile: teléfono · grupo · mesa · quién confirmó · pax · fecha RSVP · lista de asistencia por persona (con íconos ✓ · ✗ · ·) · notas · botón "Editar familia".

**Función:** `buildDetailHtml(f) → string`  
Igual que `buildFamDetailContent` pero en formato de fila de tabla (`<td colspan="9">`). Usado por la tabla oculta de compatibilidad.

**Función:** `toggleDetail(id, btn)`  
Muestra/oculta filas de la tabla de compatibilidad.

---

#### Edición de familias

**Función:** `startEdit(id)`  
Reemplaza el HTML del panel de detalle `#di-{id}` con un formulario inline (nombre, pases, grupo, teléfono, nombres de invitados, notas) pre-poblado con los datos actuales.

**Función async:** `saveEdit(id)`  
Lee los campos del formulario inline, hace `PATCH families?id=eq.UUID` con el payload. En caso de error restaura el botón. Normaliza el nombre: elimina el prefijo "Familia " antes de guardar para re-agregarlo limpio.

---

#### Alta de familia (modal)

El modal `#nf-modal-overlay` contiene el formulario de nueva familia. La lógica es una IIFE con las siguientes funciones internas:

**Función:** `createGuestRow(num, val) → HTMLElement`  
Crea una fila con número, input de nombre y botón ✕. El ✕ llama a `renumberRows()`.

**Función:** `renumberRows()`  
Re-numera todos los `.gn-num` en el contenedor tras eliminar una fila.

**Función:** `syncGuestRows(count)`  
Agrega o elimina filas para que el total coincida con `count`.

**Función:** `collectGuestNames() → string`  
Lee todos los inputs del contenedor y devuelve los valores no vacíos unidos por coma.

**Función:** `clearGuestRows()`  
Vacía el contenedor y re-inicializa con las filas según el valor actual de pases.

**Evento `input` en pases:** Llama a `syncGuestRows` con el nuevo valor.  
**Evento `click` en "Agregar invitado":** Agrega una fila y auto-incrementa el contador de pases si excede.  
**Evento `input` en nombre:** Llama a `autoGenerateCode(name)`.  
**Evento `input` en código:** Fuerza mayúsculas y elimina caracteres no alfanuméricos ni guión.

**Evento `click` en "Agregar" (submit):**  
1. Normaliza el nombre
2. Valida: nombre · código · formato `[A-Z0-9]+-\d+` · pases 1–20 · teléfono ≥ 10 dígitos
3. `POST /rest/v1/families` con todos los campos
4. Si el código está duplicado (error 23505 de Postgres), llama a `autoGenerateCode` y muestra error
5. En éxito: `closeNfModal()` + `loadData()`

**Función:** `deleteFamily(id, name)`  
Bloquea la eliminación si la familia ya confirmó. Pide confirmación, luego `DELETE families?id=eq.UUID`.

---

#### Mesas

**Constantes:**
- `TOTAL_MESAS = 20`
- `CAP_POR_MESA = 12`

**Función:** `buildMesaMap() → object`  
Construye un mapa `{ [numero]: { pax, names, over } }` con la ocupación actual de cada mesa. Suma los `guest_count` de RSVPs con `attending: true`. Calcula `over = pax > 12`.

**Función:** `buildMesaSelect(id, current) → string`  
Genera el HTML de un `<select>` con las 20 mesas. Cada opción muestra `M1 (3/12)` con aviso `⚠` si está sobre capacidad o `✓` si está llena.

**Función async:** `assignTable(id, val)`  
Si la mesa quedaría sobre capacidad pide confirmación. `PATCH families?id=eq.UUID` con `{ table_number: val }`. Actualiza `allData` en memoria para evitar re-fetch. Llama a `renderProgress`.

**Función:** `renderMesasGrid()`  
Dibuja el grid de 20 tarjetas de mesa. Para cada mesa calcula el estado (`empty / partial / full / over`), genera 12 barras de asiento (llenas/vacías) y los nombres de familias (máx. 2 + "+" si hay más). Actualiza los stats resumen y el banner sin mesa.

**Función:** `openMesaDetail(n)`  
Construye el contenido del bottom sheet para la mesa `n`: barra de capacidad con color semántico · lista de familias con botón "Quitar" · dropdown de familias sin mesa para asignar. Abre el overlay con `.is-open`.

**Función:** `closeMesaDetail()`  
Quita `.is-open` del overlay.

**Función:** `closeMesaDetailIfBackdrop(e)`  
Cierra el detail sheet solo si el click fue directamente sobre el backdrop (no sobre el contenido).

**Función async:** `removeFromMesa(id, mesaNum)`  
`PATCH families?id=eq.UUID` con `{ table_number: null }`. Actualiza en memoria y re-renderiza la mesa y el progress.

**Función async:** `assignFromDetail()`  
Lee el dropdown del detail sheet, verifica capacidad y `PATCH families` con el número de mesa. Actualiza en memoria y re-renderiza.

---

#### Progress bars

**Función:** `renderProgress(data)`  
Calcula y actualiza las 3 barras del tab Resumen. Si `totalGuests > VCAP` la barra de pases invitados se pone roja. Si `confGuests >= VCAP * 0.9` la barra de pax confirmados se pone ámbar. También actualiza la alerta "sin mesa" del Resumen.

---

#### Recordatorios de pendientes

**Función:** `showReminders()`  
Filtra `allData` por `!f.confirmed`, renderiza la lista en `#reminder-list` con nombre + código + teléfono + botón WhatsApp. Hace scroll suave a la sección.

**Función:** `hideReminders()`  
Oculta `#reminder-section`.

---

#### Check-in (día del evento)

**Variable:** `ciData` — Array de familias confirmadas con `attending: true`.

**Función:** `openCheckin()`  
Filtra las familias confirmadas en `ciData`, llama a `renderCheckin`, muestra el overlay, limpia la búsqueda, bloquea el scroll del body.

**Función:** `closeCheckin()`  
Detiene el scanner QR, oculta el overlay, restaura el scroll y llama a `loadData()`.

**Función:** `filterCheckin(q)`  
Filtra `ciData` por nombre o código y llama a `renderCheckin(filtered, true)`.

**Función:** `renderCheckin(data, keepStats)`  
Actualiza los contadores del overlay: familias llegadas / total · personas llegadas / total · barra de progreso porcentual. Renderiza la lista de tarjetas de check-in con estado visual (llegó / pendiente).

**Función async:** `checkIn(id)`  
`PATCH families?id=eq.UUID` con `{ checked_in: true, checked_in_at: new Date().toISOString() }`. Actualiza `ciData` en memoria.

**Función async:** `uncheckIn(id)`  
`PATCH families?id=eq.UUID` con `{ checked_in: false, checked_in_at: null }`.

---

#### QR Scanner

**Variables de estado:**
- `_qrActive` — `boolean`, si el scanner está corriendo
- `_qrStream` — `MediaStream` de la cámara
- `_qrFrame` — ID del `requestAnimationFrame`
- `_qrLast` — Último código escaneado (evita procesar el mismo dos veces)

**Función:** `toggleQrScanner()`  
Alterna entre `startQrScanner()` y `stopQrScanner()`.

**Función async:** `startQrScanner()`  
Solicita acceso a la cámara trasera con `navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })`. Asigna el stream a `<video id="qr-video">`, inicia reproducción y arranca `tickQrScan()`.

**Función:** `stopQrScanner()`  
Detiene todos los tracks del stream, cancela el `requestAnimationFrame`, oculta el viewport y restaura la UI.

**Función:** `tickQrScan()`  
Loop de animación. En cada frame dibuja el video en `<canvas id="qr-canvas">` y pasa los datos de imagen a `jsQR()`. Si detecta un código diferente al último, extrae el parámetro `?code=` de la URL (o usa el valor directo) y llama a `onQrDetected(code)`.

**Función:** `onQrDetected(code)`  
Busca el código en `ciData`. Si no existe muestra tarjeta de error. Si ya hizo check-in muestra la hora de llegada. Si no ha llegado muestra el botón "✓ Llegó" que llama a `qrCheckIn(id, code)`.

**Función async:** `qrCheckIn(id, code)`  
Llama a `checkIn(id)`, refresca el resultado con `onQrDetected(code)` y agrega el botón "Escanear siguiente".

---

#### Filtros y acción masiva

**Variable:** `activeGroup` — String con el grupo activo (`""` = Todos, `"__pending__"` = Sin confirmar, o el nombre de un grupo).

**Evento:** `click` en `#group-filter` → detecta el botón con `.closest(".gf-btn")` → actualiza `activeGroup` → si es `"__pending__"` muestra la barra de acción masiva con el conteo actualizado → llama a `applyFilters()`.

**Función:** `applyFilters()`  
Combina el filtro de grupo con la búsqueda de texto. Si `activeGroup === "__pending__"` filtra por `!f.confirmed`. Llama a `renderTable(filtered)`.

**Función async:** `markAllPendingAsDeclined()`  
Filtra las familias sin confirmar, pide confirmación con el conteo exacto. Para cada familia en paralelo (`Promise.all`):
1. `PATCH families?id=eq.UUID` con `{ confirmed: true }`
2. `POST rsvps` con `{ attending: false, guest_count: 0, contact_name: "Sin respuesta" }`

Tras completar llama a `loadData()`, cierra la barra de acción masiva y vuelve al filtro "Todos".

---

#### Navegación de tabs

**Función:** `switchTab(name)`  
Quita `.is-active` de todos los `.tab-panel` y `.bottom-nav__item`. Agrega `.is-active` al panel `#tab-{name}` y al botón `#nav-{name}`. Hace scroll al top del `.tab-content`. Si es `"mesas"` llama a `renderMesasGrid()`. Si es `"fotos"` llama a `loadPhotos()`. Si es `"mensajes"` llama a `loadMsgs()`. Guarda en `localStorage("ke-tab")`.

---

#### Modal Settings / Configuración

**Función:** `openSettings()`  
Abre `#settings-overlay` y pobla el dropdown de simulación de RSVP con las familias pendientes.

**Función:** `closeSettings()`  
Cierra el overlay.

**Función:** `closeSettingsIfBackdrop(e)`  
Cierra solo si el click fue en el backdrop.

**Validación de URL:**
```js
function checkUrl(url) { ... }
```
Verifica que la URL tenga dominio válido (no `file://`, no `localhost`). Muestra un indicador verde ✓ o un aviso ⚠.

---

#### Modal Nueva Familia

**Función:** `openNfModal()`  
Agrega `.is-open` al overlay, foca `#nf-name`, bloquea scroll.

**Función:** `closeNfModal()`  
Quita `.is-open`, restaura scroll, limpia todos los campos y reinicia los nombres de invitados.

**Función:** `closeNfModalIfBackdrop(e)`  
Cierra solo si el click fue en el backdrop.

El modal también se cierra con la tecla `Escape`.

---

#### Badge de pendientes

**Función:** `updatePendingBadge(count)`  
Actualiza el badge rojo en el nav de Resumen. Si `count > 0` muestra el número y agrega `.is-visible`. Si `count === 0` lo oculta.

---

#### Tab: Fotos (Supabase Storage)

**Constante:** `STORAGE_BUCKET = "fotos-boda"`

**Slots definidos:**

| Key | Label | Descripción |
|-----|-------|-------------|
| `portada` | Foto de Portada | Header, footer y preview WhatsApp |
| `galeria-0` | Galería: Foto Principal | Foto ancha al inicio de la galería |
| `galeria-1` | Galería 1 + Separadora | |
| `galeria-2` | Galería 2 | |
| `galeria-4` | El Anillo | |
| `galeria-5` | Retrato Karla | |
| `galeria-6` | Retrato Eduardo | |

**Función:** `storagePublicUrl(filename) → string`  
Genera la URL pública de Supabase Storage: `SUPABASE_URL + "/storage/v1/object/public/fotos-boda/" + filename`.

**Función async:** `loadPhotos()`  
`POST /storage/v1/object/list/fotos-boda` → recibe lista de archivos → construye `_photoUrls` (mapa de slot-key a URL pública) → llama a `renderPhotosTab()`.

**Función:** `renderPhotosTab()`  
Construye el grid de slots. Cada slot muestra la imagen si existe (con badge "✓ Subida") o un placeholder. Incluye botón subir/reemplazar + botón eliminar + `<input type="file" hidden>`.

**Función:** `triggerPhotoUpload(slotKey)`  
Simula click en el `<input type="file">` del slot.

**Función:** `compressImage(file, maxPx, quality) → Promise<Blob>`  
Carga la imagen en un canvas oculto, la escala proporcionalmente si supera `maxPx` en cualquier dimensión, y exporta como JPEG con la calidad dada. Siempre devuelve JPEG independientemente del formato original.

**Función async:** `handlePhotoUpload(slotKey, input)`  
1. Comprime la imagen (máx. 1200px, calidad 0.82)
2. Si ya existe una foto en ese slot, la elimina primero (`DELETE`)
3. Sube la nueva con `POST /storage/v1/object/fotos-boda/{slotKey}.jpg`
4. Actualiza la barra de progreso en 4 etapas (15% → 35% → 55% → 85% → 100%)
5. Llama a `loadPhotos()` tras 300 ms

Si hay error (permisos de Storage no configurados), muestra un `alert()` con instrucciones exactas de Supabase.

**Función async:** `deletePhoto(slotKey)`  
Pide confirmación, `DELETE /storage/v1/object/fotos-boda` con el nombre del archivo, llama a `loadPhotos()`.

---

#### Tab: Mensajes (Libro de Visitas — admin)

**Función:** `escMsg(s) → string`  
Escapa `&`, `<`, `>`, `"` para inserción segura en innerHTML.

**Función:** `renderMsgsList(msgs)`  
Renderiza tarjetas de mensajes en `#msgs-list`. Cada tarjeta tiene nombre · fecha · texto · botón eliminar.

**Función async:** `loadMsgs()`  
`GET /rest/v1/messages?order=created_at.desc&limit=200` → actualiza `_allMsgs` → calcula mensajes nuevos (comparando con `localStorage("ke-msgs-seen-at")`) → actualiza el badge en el nav → marca todos como vistos → llama a `filterMsgs`.

**Función:** `filterMsgs(q)`  
Filtra `_allMsgs` por nombre o mensaje y llama a `renderMsgsList`.

**Función async:** `deleteMsg(id)`  
`DELETE /rest/v1/messages?id=eq.UUID` → llama a `loadMsgs()`.

---

#### Herramientas de prueba (Settings modal)

Solo visibles en el modal de configuración `⚙`. Útiles para tests y demos.

**Función async:** `seedTestFamilies()`  
Crea 8 familias `TEST-01…08` con diferentes estados (confirmada, pendiente, declinada, con/sin mesa). Para cada una hace `POST families` y, si corresponde, `POST rsvps`.

**Función async:** `simulateFullCheckIn()`  
Marca como `checked_in: true` todas las familias confirmadas. Útil para simular el día del evento.

**Función async:** `resetAllCheckIn()`  
`PATCH families?confirmed=eq.true` con `{ checked_in: false, checked_in_at: null }` para todas las confirmadas.

**Función async:** `simRsvp(attending)`  
Confirma/declina una familia pendiente seleccionada en el dropdown: `PATCH families` + `POST rsvps`.

**Función async:** `cleanupTestData()`  
`DELETE families?code=like.TEST-%` para eliminar todos los datos de prueba.

---

#### Tema claro / oscuro

**Función:** `toggleTheme()`  
Lee el tema actual de `data-theme` en `<html>`. Alterna entre `"light"` y `"dark"`. Guarda en `localStorage("ke-theme")`. El ícono del header usa CSS para mostrar sol (modo oscuro) o luna (modo claro).

---

#### Auto-generación de código

**Función:** `autoGenerateCode(name)`  
Normaliza el nombre: elimina acentos, espacios iniciales/finales y el prefijo "Familia ". Extrae la primera palabra relevante (apellido), la convierte a mayúsculas y agrega el sufijo `-NN` buscando el primer número disponible que no exista en `allData`.

Ejemplo: "García López" → base `GARCIA` → verifica `GARCIA-01`, `GARCIA-02`... hasta encontrar uno libre.

Muestra el código generado en `#nf-code` y una nota informativa en `#nf-code-hint`.

---

#### CSV Export

**Evento:** `click` en `#btn-export`  
Genera un CSV con columnas: Código · Familia · Pases · Mesa · Estado · Confirmó · Asistentes · Fecha. Crea un `Blob` con tipo `text/csv`, genera URL temporal y simula descarga.

---

## 5. sw.js — Service Worker

Estrategia: **Cache First** para recursos estáticos.

**Evento `install`:** Precachea el shell: `index.html`, `admin.html`, `manifest.json`, `fondo.mp3`, los 5 `.webp` de flores y `novios.webp`.

**Evento `activate`:** Elimina cachés antiguas (versiones anteriores).

**Evento `fetch`:** Para cada request intenta responder desde caché. Si no hay caché hace la petición a red y guarda la respuesta (solo para recursos del mismo origen). Las peticiones a `supabase.co` **nunca** se cachean para garantizar datos frescos.

---

## 6. manifest.json — PWA

```json
{
  "name": "Boda Karla & Eduardo",
  "short_name": "K & E 2026",
  "start_url": "./index.html",
  "display": "standalone",
  "background_color": "#f7f4ee",
  "theme_color": "#c9a96e",
  "icons": [...]
}
```

Permite "instalar" la invitación en la pantalla de inicio de un smartphone. Al abrirla desde el ícono instalado funciona como una app nativa (sin barra del navegador).

---

## 7. Identidad visual y sistema de diseño

### Paleta de colores

| Variable CSS | Valor | Uso |
|-------------|-------|-----|
| `--c-gold` / `--gold` | `#c9a96e` | Color primario dorado |
| `--c-terra` | `#b76e49` | Terracota secundaria |
| `--c-parchment` | `#f7f4ee` | Fondo pergamino |
| `--text` / fondo oscuro | `#1e1410` | Texto y secciones oscuras |
| `--text-mid` | `#2c2c2c` | Texto normal |
| `--confirm-green` | `#7ec8a0` | Estado confirmado |
| `--alert-red` | `#e08888` | Estado error / alerta |

### Tipografía

| Fuente | Uso |
|--------|-----|
| Playfair Display | Títulos, nombres, encabezados |
| Montserrat | Cuerpo de texto, UI, labels |
| Great Vibes | Nombres de la pareja (script caligráfico) |

### Sistema floral

Las 5 imágenes `.webp` de flores se aplican en 20 instancias a lo largo de la invitación. La regla de `mix-blend-mode` es estricta:

| Fondo | `mix-blend-mode` |
|-------|-----------------|
| Claro (pergamino) | `multiply` |
| Oscuro (countdown, footer) | `screen` |

`flores-4` y `flores-5` tienen fondo blanco → blend perfecto en `multiply`.  
`flores-1`, `flores-2`, `flores-3` tienen fondos cálidos → crean viñeta artística en `multiply`.

### Animaciones CSS clave

| Clase / keyframe | Efecto |
|-----------------|--------|
| `card-rise` | Sube el contenido en el primer render (fill-mode: both) |
| `countdown__number--flip` | Flip vertical al cambiar cada dígito |
| `gold-shimmer` | Barrido de luz dorada sobre los nombres K&E |
| `js-fade` + `.is-visible` | Fade-in con translate al entrar en viewport |

---

## 8. Variables de entorno y credenciales

> Estas variables están expuestas en el JS público. Son seguras porque Supabase las protege con Row Level Security (RLS) y la anon key solo tiene permisos limitados.

| Variable | Valor |
|----------|-------|
| `SUPABASE_URL` | `https://kdpgdgulrekryxqtewtr.supabase.co` |
| `SUPABASE_ANON_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` |
| `ADMIN_PASSWORD` | `KarlaEduardo2026` |
| `COUPLE_PHONE` | `524444382498` (+52 444 382 498) |

> **Nota:** La contraseña del admin está hardcodeada en JS. Si alguien inspecciona el código fuente de `admin.html` puede verla. Esto es aceptable para un evento privado de una sola persona, pero no para un sistema multi-usuario.

---

## Notas importantes para desarrollo

### Bugs conocidos y sus fixes permanentes

1. **Lightbox con `position: fixed`** — El `#gallery-lightbox` debe ser hijo directo de `<body>`, nunca de `.invitation`. La razón: `.invitation` tiene `animation: card-rise` con `fill-mode: both`, lo que convierte ese elemento en containing block de `position: fixed`.

2. **Admin CSS `display`** — Nunca usar `panel.style.display = 'block'` inline para mostrar el panel, porque anula el `display: flex` del CSS. Siempre usar `classList.add('is-visible')`.

3. **`mix-blend-mode` en fondo oscuro** — `multiply` sobre negro = negro. En secciones oscuras usar siempre `screen`.

4. **iOS auto-zoom** — Todos los `input` y `textarea` deben tener `font-size: 1rem` mínimo para evitar el zoom automático de Safari iOS.

### Convenciones de desarrollo

- **Sin frameworks.** Vanilla JS, no agregar React/Vue/etc.
- **Supabase único backend.** No agregar otro servidor.
- **Imágenes nuevas → WebP.** `cwebp -q 82 -m 6 input.png -o output.webp`
- **Sin comentarios redundantes.** Solo cuando el porqué no es obvio.
- **Mobile-first.** El canal principal es WhatsApp en móvil.

### Checklist antes de modificar layout/floral

1. ¿El elemento está sobre fondo claro o oscuro? → determina `mix-blend-mode`
2. ¿Usa `transform`? → puede afectar `position: fixed` de sus hijos
3. ¿El lightbox sigue siendo hijo de `<body>` y no de `.invitation`?
4. ¿Los nuevos `<img>` tienen `loading="lazy"` (excepto above-the-fold)?
