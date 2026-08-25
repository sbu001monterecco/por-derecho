# Protocolo de adquisición y custodia del buzón privado de la declarante reservada

**Fecha:** 25 de agosto de 2026

**Alias público de la fuente:** `RDM-PRIVATE-MAILBOX-01`

**Objeto:** preservar y revisar, con autorización de la titular, el buzón privado que contiene correspondencia material de los periodos relevantes

**Estado actual:** tras el aviso de las 22:49 UTC del 25 de agosto de 2026, el buzón receptor autenticado verificó aproximadamente a las 23:13 UTC una transmisión de la titular. El mensaje RFC 2822 recibido y un libro-manifiesto fueron preservados y hash-controlados en custodia privada. El libro reconcilia un amplio índice de Gmail, pero no contiene los correos ni adjuntos nativos indexados; Drive no estuvo disponible/conectado y la comparación con el buzón contraparte sigue abierta. Existe además una copia parcial reflejada en un buzón contraparte conectado y autorizado

**Privacidad:** la dirección exacta, cuerpos, asuntos, participantes, identificadores de Google y localizadores de mensajes no se publican en GitHub

## 1. Hallazgo de preservación

La declarante reservada indicó que su cuenta privada contiene muchos correos clave de los periodos relevantes. Separadamente, una búsqueda paginada completa **dentro de una consulta definida** del buzón contraparte actualmente conectado localizó **más de 2.400 mensajes relacionados** enviados a o desde `RDM-PRIVATE-MAILBOX-01`; aproximadamente mil contienen adjuntos y más del 90% se concentran en 2011–2019. Estos agregados gruesos demuestran la existencia de una colección reflejada sustancial y justifican preservación prioritaria. **No** demuestran que el lado conectado contenga el buzón completo, que cada coincidencia sea probatoria ni que la afirmación de la declarante sobre relevancia esté corroborada elemento por elemento.

Los recuentos exactos por año, término, remitente, destinatario, hilo y adjunto pertenecen exclusivamente al manifiesto privado. Los términos de descubrimiento se solapan y no constituyen una suma, una medida de relevancia, una conclusión sobre conocimiento ni corroboración independiente.

## 2. Autoridad y límites

La adquisición completa requiere autorización verificable de la titular de `RDM-PRIVATE-MAILBOX-01` o acceso concedido por ella mediante el mecanismo oficial de Google. No se pedirán ni recibirán contraseñas por chat. La autorización de Gil, el acceso a un buzón corporativo o la presencia de mensajes reenviados no sustituyen la autorización de la titular para adquirir su cuenta completa.

Hasta entonces pueden preservarse y analizarse, dentro de la autorización existente, únicamente los mensajes reflejados en el buzón contraparte conectado. No se borrará, moverá, reetiquetará, reenviará, migrará ni marcará correo durante la adquisición.

La autorización para conectar o preservar, la autorización para revisar contenido, la autorización para presentar ante una institución y la **autorización para publicar** son decisiones distintas. La autorización para preservar o revisar no autoriza por sí sola otra de esas actuaciones.

## 3. Ruta de adquisición preferente

### A. Exportación nativa completa mediante Google Takeout

1. La titular inicia sesión directamente en su propia cuenta y selecciona sólo Gmail, salvo que autorice otros productos.
2. Registra fecha/hora/zona, opciones, etiquetas incluidas, formato, método de entrega y todos los volúmenes que genere la exportación.
3. Descarga los archivos desde un equipo controlado; no comparte credenciales.
4. Conserva cada ZIP/TGZ original sin abrir ni modificar como copia maestra y crea una copia de trabajo separada.
5. Calcula SHA-256, tamaño y nombre exacto de cada volumen; crea un manifiesto de cada MBOX y archivo asociado.
6. Mantiene dos copias controladas en ubicaciones separadas y una copia de trabajo derivada.
7. Registra las etiquetas Gmail preservadas en cabeceras `X-Gmail-Labels` y cualquier aviso de exclusión o cambio durante la generación.
8. No ofrece una exportación por fecha si la interfaz no la permite: exporta el conjunto autorizado y aplica el filtro temporal sólo sobre la copia de trabajo.

Google explica el procedimiento y las limitaciones en [Descargar tus datos de Google](https://support.google.com/accounts/answer/3024190) y describe que la exportación de Gmail puede incluir contenido, cabeceras, adjuntos y etiquetas en [Qué datos se exportan de Gmail](https://support.google.com/mail/answer/10016932). Takeout no recupera correo eliminado permanentemente.

### B. Adquisición por Gmail API o conector autorizado

Después de verificar el perfil de la cuenta correcta:

1. enumerar todas las etiquetas y mensajes accesibles, incluyendo spam, papelera y material todavía retenido por el proveedor; no prometer recuperación de correo eliminado permanentemente;
2. guardar el denominador total y cada identificador en el registro privado;
3. recuperar cada mensaje en formato `RAW`, que devuelve el mensaje RFC 2822 completo codificado en base64url;
4. recuperar y hash-controlar adjuntos y cuerpos MIME;
5. registrar errores, mensajes no recuperables, reintentos y límites de API; y
6. reconciliar los resultados contra Takeout y contra la copia corporativa.

Referencias oficiales: [Gmail API — users.messages](https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages) y [Gmail API — Format](https://developers.google.com/workspace/gmail/api/reference/rest/v1/Format).

## 4. Reconciliación y deduplicación

La adquisición no se declara completa hasta comparar:

- total de mensajes y cobertura temporal de Takeout, API y buzón contraparte conectado;
- `Message-ID` de cabecera, fecha, remitente/destinatario normalizados, tamaño y hash del cuerpo/adjuntos;
- mensajes enviados, recibidos, archivados, spam, papelera, borradores y etiquetas;
- cadenas reenviadas o citadas frente al mensaje nativo;
- duplicados exactos, variantes MIME y copias con adjuntos distintos; y
- cambios producidos durante la creación de la exportación.

La deduplicación conserva la procedencia de cada copia. Un mensaje reenviado o impreso no sustituye al original nativo.

## 5. Revisión probatoria y de privilegio

Antes de examinar o publicar contenido:

1. separar comunicación directa, reenvío, cita, borrador y adjunto;
2. autenticar cabeceras, cronología y participantes sin suponer que una cuenta identifica siempre al autor humano;
3. clasificar cada proposición como hecho documental, manifestación de parte, inferencia o cuestión abierta;
4. revisar privilegio abogado–cliente, estrategia, datos fiscales/bancarios y datos de terceros;
5. buscar correcciones, respuestas, mensajes anteriores/posteriores y documentos adjuntos que cambien el sentido;
6. conservar evidencia adversa y exculpatoria; y
7. publicar sólo derivados necesarios, redactados y enlazados mediante un localizador público seguro.

## 6. Manifiesto privado mínimo

| Campo | Contenido |
|---|---|
| Source ID | `RDM-PRIVATE-MAILBOX-01` |
| Titular y autorización | referencia privada y fecha |
| Perfil de cuenta verificado | sí/no; nunca dirección pública |
| Periodo y etiquetas | inicio/fin y alcance |
| Método | Takeout / API / copia corporativa |
| Archivo nativo | nombre privado, tamaño y SHA-256 |
| Denominador | mensajes, hilos, adjuntos y errores |
| Custodio | persona/sistema y transferencias |
| Privilegio/retención | reglas aplicadas |
| Derivados | IDs, hashes y relación con la fuente |

## 7. Criterio de cierre y estado actual

`RDM-PRIVATE-MAILBOX-01` permanece **PARCIAL / NO ADQUIRIDO EN SU TOTALIDAD**. La transmisión recibida preserva un mensaje nativo y un libro-manifiesto en custodia privada; el libro reconcilia aproximadamente 10,6 mil filas de correo, 9,0 mil filas de adjuntos y 4,3 mil hilos. No entrega los originales subyacentes, no contiene una adquisición de Drive y no prueba la ausencia definitiva indicada por su clasificación de prioridad. El corpus reflejado de más de 2.400 mensajes relacionados preserva un punto de partida contraparte importante, pero tampoco autoriza la expresión «todos los correos de la declarante».

## 8. Primer traspaso privado recibido — 25 de agosto de 2026

El estado operativo y el resultado verificado constan en `RDM_PRIVATE_MAILBOX_PENDING_INBOUND_CONTROL_25AUG2026.md`. Se ejecutó `prompts/RDM_PRIVATE_MAILBOX_INBOUND_EVIDENCE_INGEST_PROMPT_25AUG2026.md`: el mensaje y libro recibidos quedaron preservados con metadatos y hashes en privado, y el denominador interno del libro fue reconciliado. La entrega debe clasificarse como **manifiesto/índice**, no como transferencia de los originales descritos. `ME-090` / `ME-MAIL-RDM-001` siguen abiertos hasta la adquisición nativa, Drive, privilegio, deduplicación, comparación contraparte y recuperación independiente. No se realizó respuesta, reenvío, recordatorio, compartición, publicación ni cambio de buzón.
