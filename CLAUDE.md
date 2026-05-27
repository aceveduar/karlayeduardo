# CLAUDE.md — Invitación Premium Karla & Eduardo

## Contexto del Proyecto

Sistema completo de invitación digital premium para la boda de **Karla y Eduardo**, el **21 de noviembre de 2026** en Hacienda Zerezotla, San Andrés Cholula, Puebla. No es solo una invitación: es una plataforma de gestión de boda end-to-end.

---

## Instrucciones de Comportamiento (respetar siempre)

- Actuar como **experto UX/UI + arquitecto de sistemas + diseñador gráfico**
- Ser honesto y directo: evaluar cualquier propuesta del usuario con criterio propio antes de implementar
- Cuando el usuario diga "dale" o "sí" — implementar todo lo discutido de una sola vez sin preguntar más
- Auditar como diseñador gráfico experto en invitaciones digitales: cuidar UX, UI, tipografía, espaciado, contraste, jerarquía visual
- Cuando se audite, identificar problemas con evidencia del código (línea + valor real), no suposiciones
- Siempre leer el código antes de proponer cambios — nunca asumir el estado actual
- El usuario es Eduardo, el organizador; puede no tener siempre la razón técnica — decirlo con tacto
- WhatsApp en móvil es el canal principal — todas las decisiones de diseño deben priorizar mobile-first
- Priorizar funcionalidad real, interactividad y valor operativo para gestión de la boda

---

## Stack Técnico

| Capa | Tecnología |
|------|-----------|
| Frontend | HTML5 + Vanilla JS (ES6+) + CSS3 — sin frameworks |
| Base de datos | Supabase (PostgreSQL as a Service) |
| Autenticación admin | Password hardcodeado en JS (`KarlaEduardo2026`) |
| QR | QRCode.js via CDN |
| Tipografía | Google Fonts: Playfair Display, Montserrat, Great Vibes |
| Mensajería | WhatsApp (wa.me URLs) |
| Animaciones | Canvas API + CSS transitions + Intersection Observer |
| Imágenes | WebP (convertidas con cwebp, calidad 82-85) |
| PWA | manifest.json + sw.js (service worker con cache offline) |

### Variables de entorno expuestas (JS público)
```
SUPABASE_URL      = https://kdpgdgulrekryxqtewtr.supabase.co
SUPABASE_ANON_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtkcGdkZ3VscmVrcnl4cXRld3RyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzgzNTI0NDEsImV4cCI6MjA5MzkyODQ0MX0.T6_iQjxOWX82QQHPuBI5cewOoT3UWsOQ7bvjX9GP82E
ADMIN_PASSWORD    = KarlaEduardo2026
COUPLE_PHONE      = 527721204509
```

---

## Archivos Principales

| Archivo | Rol |
|---------|-----|
| `index.html` | Invitación pública + flujo RSVP completo (~5,200 líneas tras rediseño) |
| `admin.html` | Dashboard de gestión con tabs (~2,500 líneas tras rediseño) |
| `manifest.json` | PWA manifest — permite instalar la invitación en pantalla de inicio |
| `sw.js` | Service Worker — cache offline de recursos estáticos; NO cachea Supabase |
| `assets/flores-*.webp` | Arreglos florales decorativos (convertidos de PNG a WebP, ~85% más ligeros) |
| `assets/Karla y Froyland/` | Fotos de la pareja (JPG + WebP donde aplica) |

### Assets críticos (WebP convertidos)
```
flores-1.webp  556K  (era 3.1MB PNG)
flores-2.webp  240K  (era 2.4MB PNG)
flores-3.webp  424K  (era 2.1MB PNG)
flores-4.webp  264K  (era 1.9MB PNG)
flores-5.webp  244K  (era 1.8MB PNG)
novios.webp     76K  (era 120K JPG)
anillo.webp     56K  (era 104K JPG)
```

---

## Esquema de Base de Datos (Supabase)

### Tabla `families`
```
id            UUID        PK
code          TEXT        Código único (ej. ACEVEDO-01)
family_name   TEXT        Nombre de la familia
max_guests    INTEGER     Pases asignados
confirmed     BOOLEAN     ¿Confirmó asistencia?
group_name    TEXT        Familia novia / novio / Amigos / Trabajo / Otros
phone         TEXT        WhatsApp (sin código país)
guest_names   TEXT        Nombres separados por comas
table_number  INTEGER     Mesa asignada (1–18)
notes         TEXT        Notas internas (dieta, accesibilidad, etc.)
```

### Tabla `rsvps`
```
id             UUID       PK
family_id      UUID       FK → families
contact_name   TEXT       Quien confirmó
guest_count    INTEGER    Cuántos asisten
attending      BOOLEAN    true = asiste, false = no asiste
attending_names TEXT      Nombres de quienes asisten (coma)
created_at     TIMESTAMP
```

---

## Funcionalidades Implementadas

### Para Invitados (index.html)
- [x] Invitación personalizada por código URL (`?code=ACEVEDO-01`)
- [x] Flujo RSVP multi-paso (verificar → seleccionar → nombre → ticket)
- [x] Ticket digital con QR y datos de mesa
- [x] Countdown timer al evento
- [x] Descarga de ICS (agregar al calendario)
- [x] Reproductor de música con autoplay fade-in al primer toque del usuario
- [x] Link a WhatsApp de pareja para cambiar RSVP
- [x] Animaciones de partículas (Canvas)
- [x] **Sistema floral completo**: 20 instancias de arreglos florales usando flores-1 a flores-5.webp con `mix-blend-mode: multiply` en secciones claras y `screen` en secciones oscuras
- [x] **Galería interactiva** con lightbox (el div del lightbox está fuera de `.invitation` para evitar el bug de `transform` containment)
- [x] **Sección ¿Cómo Llegar?** con 3 tarjetas escaneables (bullets con punto dorado, no párrafos)
- [x] **Timeline/Itinerario** del evento (recepción → entrada novios → brindis → banquete → fiesta)
- [x] **Nuestra Historia** con 4 momentos (El Encuentro, Crecer Juntos, La Propuesta, 21·Nov·2026)
- [x] **Dresscode** "Semi Formal" con paleta de swatches y colores prohibidos (Blanco ✕ / Beige ✕)
- [x] **Sección de Regalos** con lluvia de sobres (CLABE con copy-to-clipboard) + wishlist WhatsApp
- [x] **RSVP FAB flotante** que desaparece al llegar al formulario (IntersectionObserver)
- [x] **Open Graph meta tags** para preview en WhatsApp (imagen, título, descripción)
- [x] **PWA**: manifest.json + service worker (funciona offline después de primer carga)
- [x] **Preload** de imágenes above-the-fold (flores-5, flores-1, novios)
- [x] **37 imágenes** con `loading="lazy"`
- [x] **noscript fallback** — si JS falla, el contenido sigue visible

### Para Admin (admin.html)
- [x] Login con contraseña persistente en `localStorage` (no sessionStorage — no se pierde al cerrar)
- [x] CRUD completo de familias
- [x] **Modal para Nueva Familia** (antes era inline expandible)
- [x] **Auto-generación de código único** desde el nombre (GARCIA-01, GARCIA-02... consultando allData en memoria)
- [x] Estadísticas con **colores semánticos**: verde=confirmadas, ámbar=pendientes
- [x] **Badge de pendientes** en el tab de Resumen (punto rojo con número)
- [x] **Countdown** al evento en el Resumen
- [x] Asignación de mesas (20 mesas × 12 pax)
- [x] Alerta de sobrecapacidad por mesa
- [x] Modo check-in (día del evento)
- [x] Export a CSV
- [x] Envío de invitación por WhatsApp por familia
- [x] Filtros por grupo (chips horizontales con scroll)
- [x] Búsqueda en tiempo real con ícono lupa
- [x] **Warning visual** cuando la URL del sitio es `file://` o `localhost`
- [x] **Auto-detect URL** del sitio desde window.location al primer login

---

## Arquitectura del Admin — Sistema de Tabs

El admin es una **app shell** con `position: fixed; inset: 0`:

```
┌──────────────────────────────┐
│  App Header (56px)           │
│  ← Invitación  K&E   ⚙      │
├──────────────────────────────┤
│                              │
│  .tab-content                │
│  (overflow-y: auto)          │
│                              │
├──────────────────────────────┤
│  Bottom Nav (62px)           │
│  📊 Resumen │ 👥 Familias    │
│  🪑 Mesas   │ ✅ Check-in    │
└──────────────────────────────┘
```

### Tabs y su contenido:
- **`#tab-resumen`** — Hero countdown, stats 4 cards, progress bars, sin-mesa alert, recordatorios, acciones rápidas (actualizar/CSV), botón check-in, cerrar sesión
- **`#tab-familias`** — Toolbar (filtros + botón Nueva), search, tabla de familias
- **`#tab-mesas`** — Leyenda de colores, grid de 20 mesas
- **Check-in** — Abre el overlay existente `#checkin-overlay`

### Settings modal (`#settings-overlay`)
URL del sitio — accesible con el ícono ⚙ del header. No estorba en el flujo diario.

### JS clave del admin:
- `switchTab(name)` — cambia entre tabs, hace scroll al top del contenido
- `showMesasView()` → llama a `switchTab('mesas')`
- `openNfModal()` / `closeNfModal()` — modal nueva familia
- `autoGenerateCode(name)` — genera GARCIA-01, GARCIA-02... evitando duplicados contra allData
- `updatePendingBadge(count)` — badge rojo en nav de Resumen
- `openSettings()` / `closeSettings()` — modal de configuración URL
- Login: `localStorage.setItem("ke-admin", "1")` / `classList.add("is-visible")`

---

## Diseño & Identidad Visual

```
Color primario:   #c9a96e  (Oro)
Color secundario: #b76e49  (Terracota)
Fondo claro:      #f7f4ee  (Pergamino)
Texto oscuro:     #1e1410  (Oscuro profundo)
Texto normal:     #2c2c2c
Confirmado:       #7ec8a0  (Verde suave)
Alerta:           #e08888  (Rojo suave)
```

### Sistema Floral
Las 5 imágenes florales se usan con estas reglas:
- Sobre fondo pergamino → `mix-blend-mode: multiply` (todas)
- Sobre fondo oscuro (footer, countdown) → `mix-blend-mode: screen`
- flores-4 y flores-5 tienen **fondo blanco** → blend perfecto en multiply
- flores-1, 2, 3 tienen fondos cálidos → crean vignette artístico en multiply

### Estructura del Header de la Invitación (orden correcto)
```
1. Top floral band (flores-5 izq + flores-1 der + flores-4 centro sutil)
2. Monograma K|E + "¡Nos Casamos!"
3. Foto de la pareja (96% width, marco dorado)
4. Floral ornament (flores-4) — arriba de los nombres
5. Karla & Eduardo (script dorado shimmer)
6. Floral ornament (flores-4 flipped) — debajo de los nombres
7. Texto de invitación ("Con el corazón lleno de alegría...")
8. Versículo Colosenses 3:14
9. Padres de la novia y del novio
10. Degradado de transición parchment → oscuro (::after del inv-header)
11. Countdown oscuro (dark section)
```

---

## Detalles del Evento (Hardcodeados)

- **Fecha:** 21 de noviembre de 2026, 5:00 PM
- **Venue:** Hacienda Zerezotla, San Andrés Cholula, Puebla
- **Dirección:** Calle 15 Poniente #1531, Barrio de Santa María Xixitla
- **Deadline RSVP:** 20 de septiembre de 2026, 23:59
- **WhatsApp pareja:** +52 772 120 4509

---

## Bugs Corregidos en Esta Sesión (no volver a introducir)

1. **Lightbox no cerraba** — Causa: `.invitation` tiene `animation: card-rise` con `fill-mode: both`, dejando `transform: scale(1)` activo. Eso convierte `.invitation` en containing block de `position: fixed`. **Fix: mover `#gallery-lightbox` fuera de `<main>`, como hijo directo de `<body>`.**

2. **Admin panel no respetaba CSS `order`** — Causa: JS hacía `panel.style.display = 'block'` como inline style, anulando el `display: flex` del media query. **Fix: usar `classList.add('is-visible')` y definir `.is-visible { display: flex }` en el CSS.**

3. **Flores del bottom band invisibles** — Causa: `mix-blend-mode: multiply` sobre fondo oscuro oscurece los colores a negro. **Fix: `mix-blend-mode: screen` para elementos sobre fondos oscuros.**

4. **Galería llama `onload` duplicado** — Algunos `<img>` tenían `loading="lazy"` dos veces tras el `sed` masivo. **Fix: verificar con `grep -c 'loading="lazy".*loading="lazy"'`.**

5. **iOS auto-zoom en formularios** — Causa: inputs con `font-size < 1rem` (16px) disparan zoom automático en Safari iOS. **Fix: todos los `input` y `textarea` con mínimo `font-size: 1rem`.**

---

## Guía de Desarrollo

### Convenciones
- Sin frameworks — seguir con Vanilla JS
- Supabase como único backend — no agregar otro servidor
- Cambios en `index.html` afectan a invitados; cambios en `admin.html` son para Eduardo
- Mantener el estilo visual premium: dorado, serif, elegante
- WhatsApp es el canal de comunicación principal (no email)
- Imágenes nuevas → convertir a WebP con `cwebp -q 82 -m 6 input.png -o output.webp`
- Verificar siempre que `mix-blend-mode` sea `multiply` (claro) o `screen` (oscuro)

### Patrones de código
- Fetch API para todas las llamadas a Supabase
- `localStorage` para sesión admin (persiste aunque cierren el navegador)
- `URLSearchParams` para leer el código de la URL (`?code=`)
- Intersection Observer para animaciones de scroll y RSVP FAB
- `Canvas API` para partículas decorativas
- `cwebp` CLI para comprimir imágenes PNG → WebP

### Checklist antes de hacer cambios en floral/layout
1. ¿El elemento está sobre fondo claro (pergamino) o oscuro? → determina el blend mode
2. ¿El elemento usa `transform`? → puede afectar `position: fixed` de hijos
3. ¿El JS del lightbox sigue siendo hijo de `<body>` y no de `.invitation`?
4. ¿Los nuevos `<img>` tienen `loading="lazy"` (excepto above-the-fold)?

---

## Notas Operativas

- La boda es en **noviembre 2026** — hay tiempo para iterar
- El deadline RSVP es **20 sep 2026**
- El sistema se usa principalmente desde **WhatsApp en móvil**
- Eduardo gestiona el admin; los invitados solo ven index.html
- No hay servidor propio — todo es estático + Supabase
- **Supabase Free tier pausa proyectos sin actividad por 7 días.** Si el admin muestra "Error de conexión", verificar si el proyecto está pausado en supabase.com
- **La CLABE en la sección de Regalos tiene `XXXX` de placeholder** — Eduardo debe reemplazarla con sus datos reales de cuenta bancaria

---

## Pendientes / Próximas Iteraciones

### Alto impacto (aún no implementado)
- [ ] **QR Scanner en admin** — para check-in real el día del evento usando jsQR + cámara del celular
- [ ] **Libro de visitas digital** — invitados dejan mensajes pre-boda (requiere tabla Supabase nueva)
- [ ] **Despliegue en GitHub Pages o Netlify** — actualmente solo funciona en `file://` local; los links de WhatsApp no funcionarán hasta que esté en una URL pública
- [ ] **Llenar CLABE real** en la sección de Regalos de index.html

### Nice to have
- [ ] Hashtag #KarlaEduardo2026 en la invitación
- [ ] Historial de cambios de RSVP
- [ ] Gráficas de dona/barras en el admin (Chart.js CDN)
