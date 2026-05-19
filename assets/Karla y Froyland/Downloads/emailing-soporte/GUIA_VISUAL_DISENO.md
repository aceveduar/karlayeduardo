# 🎨 Guía Visual del Diseño de Email - Sunname

## Estructura General del Email

```
┌─────────────────────────────────────────┐
│         HEADER (Gradiente Azul)         │
│           Logo de Sunname               │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│                                         │
│  Estimado/a [Nombre del cliente],      │
│                                         │
│  [Texto de agradecimiento]             │
│  [Introducción al nuevo esquema]       │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  🎟️ 3 Tickets de Soporte         │ │
│  │  Mensuales                        │ │
│  │  ───────                          │ │
│  │  ¡SIN COSTO!                      │ │
│  │                                   │ │
│  │  ✓ Dudas operativas              │ │
│  │  ✓ Soporte funcional             │ │
│  │  ✓ Ajustes menores               │ │
│  │  ✓ Acompañamiento en el uso      │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ⏱️ Gestión, horarios y tiempos        │
│  ───────                               │
│  [Texto sobre horarios]                │
│  Lunes a Viernes 9:00 - 18:00 hrs     │
│                                         │
│  🔧 Opciones adicionales               │
│  ───────                               │
│  [Texto introductorio]                 │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │         ⚙️                        │ │
│  │  Póliza de Soporte Mensual       │ │
│  │  • Atención prioritaria          │ │
│  │  • Soporte continuo              │ │
│  │  • Mejoras evolutivas            │ │
│  │  [Botón: Conocer Pólizas]       │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │         💰                        │ │
│  │  Pago por Demanda                │ │
│  │  • Solicitudes puntuales         │ │
│  │  • Desarrollos específicos       │ │
│  │  • Pago según necesidad          │ │
│  │  [Botón: Solicitar Cotización]  │ │
│  └───────────────────────────────────┘ │
│                                         │
│  [Texto de cierre]                     │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  [Botón: Agendar una Llamada]    │ │
│  └───────────────────────────────────┘ │
│                                         │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│          FIRMA (Fondo gris)             │
│  Un cordial saludo,                     │
│  María Dolores Martínez Martínez       │
│  Sunname | Soluciones ERP              │
│  📧 contacto@sunname.mx                │
│  📞 [Teléfono]                         │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│     FOOTER (Fondo azul oscuro)         │
│     © 2026 Sunname Technologies        │
└─────────────────────────────────────────┘
```

---

## Paleta de Colores Aplicada

### Colores Principales:

**#263980 - Azul Corporativo**
- Uso: Headers, títulos principales, textos destacados
- Dónde: Header del email, títulos H1-H3, nombre de contacto
- █████████ #263980

**#46C2CE - Turquesa**
- Uso: Elementos de acento, líneas decorativas, botón CTA principal
- Dónde: Líneas bajo títulos, borde de caja de tickets, botón "Agendar"
- █████████ #46C2CE

**#F59E0B - Naranja Acento**
- Uso: Destacar información importante
- Dónde: Texto "¡SIN COSTO!", botón de pago por demanda
- █████████ #F59E0B

**#2C1A56 - Púrpura Oscuro**
- Uso: Footer, elementos secundarios
- Dónde: Footer del email
- █████████ #2C1A56

### Colores Secundarios:

**#F7FAFC - Gris muy claro**
- Uso: Fondo general, área de firma
- █████████ #F7FAFC

**#E8F4F8 - Azul muy claro**
- Uso: Cajas de contenido destacado
- Dónde: Caja de tickets incluidos, tarjeta de póliza
- █████████ #E8F4F8

**#FFF4E6 - Amarillo muy claro**
- Uso: Tarjeta de pago por demanda
- █████████ #FFF4E6

---

## Tipografía

### Jerarquía de Texto:

**H1 - Saludo principal**
- Tamaño: 22-24px
- Color: #263980
- Peso: Bold (700)
- Ejemplo: "Estimado/a [Nombre],"

**H2 - Títulos de sección**
- Tamaño: 20-22px
- Color: #263980
- Peso: Bold (700)
- Ejemplo: "3 Tickets de Soporte Mensuales"
- Incluye línea decorativa debajo (3px altura, #46C2CE)

**H3 - Subtítulos**
- Tamaño: 18-20px
- Color: #263980
- Peso: Bold (700)
- Ejemplo: "Gestión, horarios y tiempos de atención"

**H4 - Títulos de tarjetas**
- Tamaño: 17-18px
- Color: #263980
- Peso: Bold (700)
- Ejemplo: "Póliza de Soporte Mensual"

**Párrafos normales**
- Tamaño: 15-16px
- Color: #333333
- Line-height: 1.6
- Peso: Regular (400)

**Texto destacado**
- Color: #F59E0B
- Peso: Bold (700)
- Ejemplo: "¡SIN COSTO!"

---

## Elementos Visuales

### 1. Iconos Circulares

**Diseño:**
```
┌─────────┐
│    ⚙️   │  ← 50-60px diámetro
└─────────┘
```

- Fondo: Color sólido o gradiente según contexto
- Borde redondeado: 50% (círculo perfecto)
- Icono: Emoji o imagen centrada
- Margin bottom: 10-15px

**Colores de fondo:**
- Póliza: #263980
- Pago por demanda: #F59E0B
- Check marks en lista: Gradiente #263980 → #46C2CE (24px)

### 2. Botones (CTAs)

**Botón Principal (Azul):**
```
┌──────────────────────────┐
│   Conocer Pólizas       │
└──────────────────────────┘
```
- Background: #263980 (o gradiente)
- Color texto: #FFFFFF
- Padding: 12-15px vertical, 30-35px horizontal
- Border-radius: 25px (redondeado completo)
- Font-weight: Bold
- Font-size: 14-16px

**Botón Secundario (Naranja):**
```
┌──────────────────────────┐
│   Solicitar Cotización  │
└──────────────────────────┘
```
- Background: #F59E0B
- Resto igual al botón principal

**Botón CTA Grande (Turquesa):**
```
┌──────────────────────────┐
│   Agendar una Llamada   │
└──────────────────────────┘
```
- Background: #46C2CE
- Padding: 15-16px vertical, 35-40px horizontal
- Font-size: 16px

### 3. Cajas de Contenido

**Caja de Tickets (Azul claro):**
- Background: #E8F4F8
- Border-left: 4px solid #46C2CE (solo versión completa)
- Padding: 20-30px
- Border-radius: 12px (opcional en versión simplificada)

**Tarjetas de Opciones:**
- Background: #E8F4F8 (Póliza) o #FFF4E6 (Demanda)
- Padding: 20-25px
- Text-align: center
- Border: 2px solid del color correspondiente (opcional)

### 4. Líneas Decorativas

Debajo de títulos H2 y H3:
- Altura: 3px
- Ancho: 50-80px
- Color: #46C2CE o gradiente
- Margin: 0 0 15px 0
- Border-radius: 999px (esquinas muy redondeadas)

---

## Responsive Design

### Desktop (>600px):
- Ancho máximo: 600px
- Dos columnas para tarjetas (en versión compleja)
- Padding generoso: 30-40px

### Mobile (<600px):
- Ancho: 100%
- Una columna (stacking)
- Padding reducido: 20-25px
- Tarjetas apiladas verticalmente
- Fuentes ligeramente reducidas si es necesario

---

## Animaciones y Efectos (Limitados en Email)

⚠️ **Nota:** Los emails tienen limitaciones de CSS. Evitar:
- Transiciones complejas
- Animaciones CSS
- Hover effects (pueden no funcionar)

**Lo que SÍ funciona:**
- Colores sólidos de fondo en hover de links (limitado)
- Sombras simples (box-shadow básico)
- Bordes

---

## Accesibilidad

✅ **Buenas prácticas implementadas:**

1. **Contraste de colores:**
   - Texto oscuro (#333333) sobre fondos claros
   - Texto blanco (#FFFFFF) sobre fondos oscuros
   - Ratio de contraste >4.5:1

2. **Tamaños de texto:**
   - Mínimo 14px para texto normal
   - Títulos claramente diferenciados

3. **Alt text en imágenes:**
   - Logo: alt="Sunname"
   - Iconos decorativos: pueden omitirse o usar alt=""

4. **Links claros:**
   - Botones con texto descriptivo
   - Color diferenciado para links
   - Underline en links de texto

5. **Estructura semántica:**
   - Uso de H1, H2, H3 para jerarquía
   - Párrafos apropiados

---

## Testing Checklist

### Pre-envío:

- [ ] **Desktop:**
  - [ ] Gmail
  - [ ] Outlook
  - [ ] Apple Mail
  - [ ] Yahoo Mail

- [ ] **Mobile:**
  - [ ] Gmail app (iOS)
  - [ ] Gmail app (Android)
  - [ ] Apple Mail (iPhone)
  - [ ] Outlook app

- [ ] **Funcionalidad:**
  - [ ] Todos los links funcionan
  - [ ] Logo se carga correctamente
  - [ ] Personalización del nombre funciona
  - [ ] Botones son clicables
  - [ ] Colores se ven correctamente

- [ ] **Contenido:**
  - [ ] Sin errores ortográficos
  - [ ] URLs correctas
  - [ ] Teléfono correcto
  - [ ] Email de contacto correcto

---

## Ejemplos de Personalización

### Variables de Odoo comunes:

```html
<!-- Nombre del contacto -->
{{object.name}}
{{object.partner_id.name}}

<!-- Empresa -->
{{object.company_id.name}}

<!-- Saludo con título -->
{{object.partner_id.title.name}} {{object.partner_id.name}}

<!-- Email del contacto -->
{{object.email}}
{{object.partner_id.email}}

<!-- Ciudad/País -->
{{object.partner_id.city}}
{{object.partner_id.country_id.name}}
```

---

## Variaciones Opcionales

### Opción 1: Header con imagen de fondo
En lugar de color sólido, usar una imagen de fondo relacionada con tecnología/ERP.

### Opción 2: Iconos personalizados
Reemplazar emojis con iconos SVG de tu biblioteca de iconos corporativa.

### Opción 3: Testimonial
Agregar una pequeña sección con un testimonial de otro cliente.

### Opción 4: FAQ
Incluir 2-3 preguntas frecuentes al final antes de la firma.

---

## Notas Técnicas Importantes

1. **Tablas, no divs:** Los emails se construyen con tablas para máxima compatibilidad.

2. **CSS Inline:** Todos los estilos deben estar inline (style="...") no en <style> tags.

3. **Imágenes absolutas:** Todas las URLs de imágenes deben ser absolutas (https://...).

4. **Evitar JavaScript:** Los emails no ejecutan JavaScript.

5. **Tested en Gmail:** Gmail tiene reglas CSS más estrictas que otros clientes.

6. **Width en px:** Usar píxeles, no porcentajes, para mayor control.

7. **Fallback fonts:** Siempre definir fonts de fallback (Arial, Helvetica, sans-serif).

---

## Recursos Adicionales

**Herramientas útiles:**
- Can I Email - Verificar compatibilidad CSS: https://www.caniemail.com/
- HTML Email Check - Validador de código: https://www.htmlemailcheck.com/
- Litmus - Testing de emails: https://www.litmus.com/
- Mail Tester - Verificar spam score: https://www.mail-tester.com/

**Inspiración de diseño:**
- Really Good Emails: https://reallygoodemails.com/
- Mails.best: https://mails.best/

---

Diseño creado: Febrero 2026
Versión: 1.0
Compatible con: Odoo Email Marketing, Mailchimp, SendGrid, y la mayoría de plataformas de email marketing

🚀 ¡Listo para implementar!
