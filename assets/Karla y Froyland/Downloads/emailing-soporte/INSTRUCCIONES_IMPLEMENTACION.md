# Guía de Implementación - Email Sunname en Odoo

## 📋 Resumen del Diseño

Este diseño de email utiliza los colores y branding de Sunname Technologies con una estructura limpia de una sola columna, optimizada para email marketing.

---

## 🎨 Paleta de Colores Utilizada

- **Azul Principal:** `#263980`
- **Turquesa:** `#46C2CE`
- **Púrpura:** `#2C1A56`
- **Acento Naranja:** `#F59E0B`
- **Fondo Claro:** `#F7FAFC`
- **Blanco:** `#FFFFFF`

**Gradientes utilizados:**
- Header: `linear-gradient(135deg, #263980 0%, #46C2CE 100%)`
- Botones principales: `linear-gradient(135deg, #263980, #46C2CE)`
- Botón amarillo: `linear-gradient(135deg, #F59E0B, #FCD34D)`

---

## 🔧 Pasos para Implementar en Odoo

### 1. Preparación del Logo

**Opción A - Subir el logo a tu servidor:**
1. Sube el archivo `SUN001_Rebranding_Sunname_LogotipoS.svg` (o versión PNG) a tu servidor
2. Obtén la URL pública del logo
3. Reemplaza `[INSERTAR_URL_LOGO]` en el HTML con tu URL

**Opción B - Usar el módulo de Odoo:**
1. En Odoo, ve a Ajustes > Técnico > Archivos adjuntos
2. Sube tu logo
3. Copia la URL generada

### 2. Configurar URLs de los Botones

Reemplaza estos placeholders en el HTML:

- `[URL_POLIZA]` - URL a la página de pólizas de soporte
- `[URL_DEMANDA]` - URL al formulario de cotización/contacto
- `[URL_AGENDAR]` - URL a tu calendario/sistema de agendamiento (ej: Calendly)
- `[TELEFONO]` - Número de teléfono de contacto

### 3. Configurar Personalización en Odoo

Para que el nombre del cliente aparezca dinámicamente:

**En el HTML, busca:**
```html
<h1>Estimado/a [Nombre del cliente],</h1>
```

**Reemplaza con:**
```html
<h1>Estimado/a {{object.name}},</h1>
```

O utiliza el campo específico de tu modelo. Ejemplos comunes en Odoo:
- `{{object.partner_id.name}}` - Nombre del contacto/cliente
- `{{object.name}}` - Nombre del registro
- `{{object.partner_id.title.name}} {{object.partner_id.name}}` - Título + Nombre

### 4. Importar en Odoo Email Marketing

**Método 1 - Constructor Drag & Drop:**
1. Ve a Marketing por correo electrónico > Mailings
2. Crea un nuevo mailing
3. Selecciona "Editar" en el editor
4. Usa bloques de "Estructura" > "Tabla" o "Columna"
5. Copia y pega secciones del HTML en bloques de "Código HTML"

**Método 2 - Editor de Código (Recomendado para este diseño):**
1. En el editor de email, busca el botón "</> Código" o "Ver código"
2. Pega el HTML completo
3. Guarda y previsualiza

### 5. Ajustes Específicos para Odoo

**a) Compatibilidad de gradientes:**
Si los gradientes no se ven correctamente en algunos clientes de email, usa colores sólidos como fallback:

```css
/* En lugar de gradiente */
background: linear-gradient(135deg, #263980, #46C2CE);

/* Usa color sólido */
background: #263980;
```

**b) Iconos de emojis:**
Los emojis (🎟️, ⏱️, 🔧, ⚙️, 💰, 📧, 📞, 📅) están incluidos en el HTML. Si no se visualizan correctamente:
- Reemplázalos con imágenes de iconos
- Usa fuentes de iconos como FontAwesome (pero verifica compatibilidad)
- O simplemente elimínalos

---

## 📱 Consideraciones de Diseño Responsive

El diseño incluye una tabla de 600px de ancho que se adapta automáticamente en móviles. Sin embargo, **las dos tarjetas (Póliza y Pago por Demanda) podrían necesitar ajustes**.

**Para mejorar la visualización móvil:**

En el HTML, busca la sección de las dos tarjetas y considera usar esta versión alternativa:

```html
<!-- Versión apilada para mejor visualización móvil -->
<table width="100%" cellpadding="0" cellspacing="0" border="0">
    <tr>
        <td style="padding-bottom: 15px;">
            <!-- Tarjeta Póliza -->
        </td>
    </tr>
    <tr>
        <td>
            <!-- Tarjeta Pago por Demanda -->
        </td>
    </tr>
</table>
```

---

## ✅ Checklist Final

Antes de enviar el email, verifica:

- [ ] Logo de Sunname cargado y URL actualizada
- [ ] Todas las URLs de botones configuradas
- [ ] Personalización del nombre del cliente funcionando
- [ ] Teléfono de contacto actualizado
- [ ] Email de contacto actualizado
- [ ] Previsualización en desktop
- [ ] Previsualización en móvil
- [ ] Envío de prueba a tu email personal
- [ ] Verificación en diferentes clientes de email (Gmail, Outlook, Apple Mail)

---

## 🎯 Sugerencias de Iconos Personalizados

Si quieres usar iconos personalizados en lugar de emojis:

**Opción 1 - Iconos SVG en línea:**
Puedes reemplazar los emojis con SVGs inline de:
- https://heroicons.com/
- https://lucide.dev/
- https://iconify.design/

**Opción 2 - Imágenes de iconos:**
Sube iconos en formato PNG (24x24px o 32x32px) y usa:
```html
<img src="URL_ICONO" width="24" height="24" alt="Icono" style="display: inline-block; vertical-align: middle;">
```

**Iconos sugeridos:**
- 🎟️ → Icono de ticket/cupón
- ⏱️ → Icono de reloj/tiempo
- 🔧 → Icono de herramienta/configuración
- ⚙️ → Icono de engranaje
- 💰 → Icono de dinero/monedas
- 📧 → Icono de email
- 📞 → Icono de teléfono
- 📅 → Icono de calendario

---

## 🔍 Testing de Email

**Herramientas recomendadas:**
1. **Litmus** - Para probar en múltiples clientes de email
2. **Email on Acid** - Testing de compatibilidad
3. **Mail Tester** - Verificar spam score
4. **Pruebas manuales:**
   - Gmail (desktop y móvil)
   - Outlook (desktop y web)
   - Apple Mail
   - Yahoo Mail

---

## 💡 Tips Adicionales

1. **Línea de asunto sugerida:**
   - "Nuevo esquema de soporte - Tu aliado estratégico"
   - "Mejoramos nuestro servicio de soporte para ti"
   - "3 tickets mensuales de soporte sin costo"

2. **Texto de previsualización (preheader):**
   ```
   Conoce nuestro nuevo esquema de soporte con 3 tickets mensuales incluidos sin costo adicional.
   ```

3. **Segmentación sugerida:**
   - Todos los clientes activos con licencia Odoo
   - Excluir clientes que ya tienen póliza de soporte premium
   - Priorizar clientes con mayor uso del sistema

4. **Momento de envío:**
   - Martes o miércoles
   - Entre 9:00 AM - 11:00 AM (hora local del cliente)
   - Evitar lunes (sobrecarga de emails) y viernes (fin de semana)

---

## 🆘 Solución de Problemas Comunes

**Problema: Los gradientes no se visualizan**
- Solución: Algunos clientes de email no soportan gradientes CSS. Usa colores sólidos como fallback.

**Problema: El email se ve descuadrado en Outlook**
- Solución: Outlook usa el motor de Word para renderizar emails. Asegúrate de usar tablas en lugar de divs y evita CSS complejos.

**Problema: Las imágenes no cargan**
- Solución: Verifica que las URLs sean públicas y accesibles. Usa URLs absolutas, no relativas.

**Problema: Los botones no son clicables**
- Solución: Asegúrate de que los enlaces `<a>` estén correctamente cerrados y tengan las URLs correctas.

**Problema: El espaciado se ve diferente en móvil**
- Solución: Usa padding en píxeles en lugar de porcentajes para mejor control.

---

## 📞 Contacto y Soporte

Si necesitas ayuda adicional para implementar este diseño, contacta al equipo técnico de Sunname.

**Fecha de creación:** Febrero 2026
**Versión:** 1.0
**Compatible con:** Odoo 14, 15, 16, 17, 18+

---

¡Éxito con tu campaña de email marketing! 🚀
