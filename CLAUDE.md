# CLAUDE.md — Invitación Premium Karla & Eduardo

## Contexto del Proyecto

Sistema completo de invitación digital premium para la boda de **Karla y Eduardo**, el **21 de noviembre de 2026** en Hacienda Zerezotla, San Andrés Cholula, Puebla. No es solo una invitación: es una plataforma de gestión de boda end-to-end.

## Rol de Trabajo

- Actuar como **experto UX/UI + arquitecto de sistemas**
- Ser honesto y directo: si el usuario propone algo, evaluarlo con criterio propio antes de implementar
- Priorizar funcionalidad real, interactividad y valor para gestión de la boda
- El usuario es el organizador principal; puede no tener siempre la razón técnica o de diseño — decirlo con tacto

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

### Variables de entorno expuestas (JS público)
```
SUPABASE_URL    = https://kdpgdgulrekryxqtewtr.supabase.co
SUPABASE_ANON_KEY = sb_publishable_7qv3hB-J6RqLsJZyMcpTgA_9bQorv4O
ADMIN_PASSWORD  = KarlaEduardo2026
COUPLE_PHONE    = 527721204509
```

---

## Archivos Principales

| Archivo | Rol |
|---------|-----|
| `index.html` | Invitación pública + flujo RSVP completo (~4,290 líneas) |
| `admin.html` | Dashboard de gestión (~2,180 líneas) |
| `assets/` | Imágenes, logos, fotos de pareja |
| `familias.csv` | Seed/export de familias (eliminado en working tree) |

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

## Funcionalidades Actuales

### Para Invitados (index.html)
- [x] Invitación personalizada por código URL (`?code=ACEVEDO-01`)
- [x] Flujo RSVP multi-paso (verificar → seleccionar → nombre → ticket)
- [x] Ticket digital con QR y datos de mesa
- [x] Countdown timer al evento
- [x] Descarga de ICS (agregar al calendario)
- [x] Mapa textual de la hacienda (salón)
- [x] Reproductor de música
- [x] Link a WhatsApp de pareja para cambiar RSVP
- [x] Animaciones de partículas (Canvas)

### Para Admin (admin.html)
- [x] Login con contraseña
- [x] CRUD completo de familias
- [x] Estadísticas en tiempo real (confirmadas, pendientes, pax total)
- [x] Asignación de mesas (18 mesas × 10 pax)
- [x] Alerta de sobrecapacidad por mesa
- [x] Modo check-in (día del evento, filtro por código/nombre)
- [x] Export a CSV
- [x] Envío de invitación por WhatsApp por familia
- [x] Filtros por grupo (novia/novio/amigos/trabajo)
- [x] Búsqueda en tiempo real

---

## Diseño & Identidad Visual

```
Color primario:   #c9a96e  (Oro)
Color secundario: #b76e49  (Terracota)
Fondo claro:      #f7f4ee  (Pergamino)
Texto oscuro:     #1e1410  (Oscuro profundo)
Texto normal:     #2c2c2c
```

Estilo: Lujo premium. Bandas florales, bordes dorados, tipografía serif cursiva, gradientes elegantes.

---

## Detalles del Evento (Hardcodeados)

- **Fecha:** 21 de noviembre de 2026, 5:00 PM
- **Venue:** Hacienda Zerezotla, San Andrés Cholula, Puebla
- **Dirección:** Calle 15 Poniente #1531, Barrio de Santa María Xixitla
- **Deadline RSVP:** 5 de noviembre de 2026, 23:59
- **WhatsApp pareja:** +52 772 120 4509

---

## Análisis Competitivo: ¿Qué tienen los mejores sistemas de invitación?

Sistemas analizados: **Zola, The Knot, Joy (withjoy.com), RSVPify, Paperless Post, Minted**.

### Lo que YA tiene este proyecto (ventaja real)
- Personalización por código — Zola y The Knot también lo tienen
- RSVP con selección de nombres específicos — pocas plataformas lo hacen así
- Check-in para el día del evento — RSVPify lo tiene de pago; aquí es gratis
- Integración WhatsApp — único en el mercado latinoamericano
- Sin subscripción mensual — Zola cobra hasta $99/mes por features equivalentes

### Mejoras Prioritarias (GAP vs. competencia)

#### 🔴 Críticas — Faltan en el sistema, muy impactantes

1. **Mapa interactivo embebido** — Zola y Joy usan Google Maps embed o Waze. Actualmente solo hay texto y un mapa SVG decorativo del salón. Los invitados necesitan cómo llegar fácilmente desde el celular.

2. **Información práctica del evento** — Todos los sistemas top tienen una sección con:
   - Código de vestimenta (dress code)
   - Cómo llegar (auto, Uber, estacionamiento)
   - Hotel/hospedaje recomendado
   - Hora de apertura de puertas vs. ceremonia

3. **Mesa de regalos / lista de bodas** — Zola y The Knot lo integran nativamente. Una sección con link a Amazon, Liverpool, o cuenta bancaria directa es estándar.

4. **Libro de visitas digital** — Joy lo tiene como feature estrella. Guests pueden dejar mensajes/fotos pre-boda. Genera mucho engagement y es un recuerdo valioso.

5. **Notificaciones automáticas de RSVP** — RSVPify envía emails automáticos. Aquí todo es manual por WhatsApp. Al menos una notificación automática al confirmar (al admin) mejoraría mucho.

#### 🟡 Importantes — Mejoran significativamente la UX

6. **Check-in por escaneo de QR** — El ticket ya tiene QR generado, pero el admin no tiene un modo de escaneo real. Con la cámara del celular y un escáner JS podría funcionar como check-in real.

7. **Restricciones dietéticas estructuradas** — Joy y Zola tienen checkboxes para vegetariano/vegano/sin gluten. Aquí es solo texto libre en `notes`. Datos desestructurados hacen difícil planificar con el catering.

8. **Estadísticas visuales (charts)** — RSVPify muestra gráficas de confirmación en tiempo real. El admin actual solo tiene números. Una gráfica de dona o barras con Chart.js (CDN) daría mucha visibilidad.

9. **Galería de fotos interactiva** — Minted y Joy tienen slider de fotos de la pareja. Las fotos están en assets pero no hay galería presentada.

10. **Timeline/Itinerario del evento** — "5pm recepción → 7pm cena → 10pm baile → 1am cierre". Joy lo muestra como línea de tiempo vertical animada.

#### 🟢 Nice-to-have — Diferenciadores premium

11. **Hashtag para redes sociales** — #KarlaEduardo2026 con instrucciones y galería live. Zola genera uno automático.

12. **Modo PWA (Progressive Web App)** — Agregar manifest.json y service worker para que invitados puedan "instalar" la invitación en su celular. Cero costo, alto impacto.

13. **Acompañante/+1 con nombre propio** — Actualmente los nombres son texto libre. Permitir que el invitado registre el nombre de su +1 en el RSVP.

14. **Historial de cambios de RSVP** — Si una familia cambia de "sí" a "no" o viceversa, no hay log. Para bodas grandes, este historial es valioso.

15. **Dashboard de mesas visual** — Un mapa visual drag-and-drop de mesas como Zola ofrece sería el feature más premium. Por ahora solo hay listas.

---

## Guía de Desarrollo

### Convenciones
- Sin frameworks — seguir con Vanilla JS
- Supabase como único backend — no agregar otro servidor
- Cambios en `index.html` afectan a invitados; cambios en `admin.html` son para Eduardo/Karla
- Mantener el estilo visual premium: dorado, serif, elegante
- WhatsApp es el canal de comunicación principal (no email)

### Patrones de código usados
- Fetch API para todas las llamadas a Supabase
- `localStorage`/`sessionStorage` para sesión admin
- `URLSearchParams` para leer el código de la URL (`?code=`)
- Intersection Observer para animaciones de scroll
- `Canvas API` para partículas decorativas

### Cómo agregar un feature nuevo
1. Decidir si va en `index.html` (guest-facing) o `admin.html`
2. Si necesita datos nuevos → agregar columna en Supabase primero
3. Mantener el estilo visual existente (variables CSS definidas)
4. Probar en móvil — la mayoría de invitados abrirán desde WhatsApp (WebView)

---

## Notas Operativas

- La boda es en **noviembre 2026** — hay tiempo para iterar
- El deadline RSVP es **5 nov 2026**
- El sistema se usa principalmente desde **WhatsApp en móvil**
- Eduardo gestiona el admin; los invitados solo ven index.html
- No hay servidor propio — todo es estático + Supabase

---

## Pendientes Conocidos (al momento de este análisis)

- `familias.csv` y `README.md` fueron eliminados del working tree (git status muestra `D`)
- Nuevas fotos en `assets/Karla y Froyland/` sin commitear
- Password de admin en texto plano en JS — aceptable para este caso de uso
