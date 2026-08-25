# Protocolo de adquisición y custodia del buzón privado de la declarante reservada

**Fecha:** 25 de agosto de 2026

**Alias público de la fuente:** `RDM-PRIVATE-MAILBOX-01`

**Objeto:** preservar y revisar, con autorización de la titular, el buzón privado que contiene correspondencia material de los periodos relevantes

**Estado actual:** el buzón completo no está conectado ni adquirido; existe una copia parcial reflejada en un buzón corporativo autorizado

**Privacidad:** la dirección exacta, cuerpos, asuntos, participantes, identificadores de Google y localizadores de mensajes no se publican en GitHub

## 1. Hallazgo de preservación

La búsqueda paginada y completa del buzón corporativo actualmente conectado localizó **2.413 mensajes** enviados a o desde `RDM-PRIVATE-MAILBOX-01`. Este resultado demuestra que existe una colección reflejada sustancial y que la cuenta privada probablemente contiene correspondencia clave de los periodos relevantes. **No** demuestra que el buzón corporativo contenga todos los mensajes de la cuenta privada ni que cada coincidencia sea probatoria.

### Distribución temporal de la copia reflejada

| Periodo | Mensajes localizados |
|---|---:|
| 2008–2010 | 0 |
| 2011 | 0 |
| 2012 | 399 |
| 2013–2016 | 775 |
| 2017–2018 | 951 |
| 2019–2022 | 152 |
| 2023–2026 | 136 |
| **Total** | **2.413** |

Los periodos son disjuntos. Los recuentos reflejan mensajes, no hilos ni documentos únicos.

### Búsquedas de descubrimiento dentro de esa copia

| Término/familia | Coincidencias |
|---|---:|
| Sun Park | 1.488 |
| Pink Canary | 68 |
| Monterecco | 844 |
| CEXP | 12 |
| Comunidad | 384 |
| Pamanil/Pamalexsha | 60 |
| Concurso | 371 |
| Bankia | 179 |
| Garrigues | 161 |
| Campanario | 14 |
| Prieto Puente/López Noriega | 26 |
| Borja/Rodríguez-Batllori | 109 |

Estos recuentos se solapan y son sólo una herramienta de descubrimiento. No son una suma, una medida de relevancia, una conclusión sobre conocimiento ni corroboración independiente.

## 2. Autoridad y límites

La adquisición completa requiere autorización verificable de la titular de `RDM-PRIVATE-MAILBOX-01` o acceso concedido por ella mediante el mecanismo oficial de Google. No se pedirán ni recibirán contraseñas por chat. La autorización de Gil, el acceso a un buzón corporativo o la presencia de mensajes reenviados no sustituyen la autorización de la titular para adquirir su cuenta completa.

Hasta entonces pueden preservarse y analizarse, dentro de la autorización existente, únicamente los mensajes reflejados en el buzón corporativo. No se borrará, moverá, reetiquetará, reenviará, migrará ni marcará correo durante la adquisición.

## 3. Ruta de adquisición preferente

### A. Exportación nativa completa mediante Google Takeout

1. La titular inicia sesión directamente en su propia cuenta y selecciona sólo Gmail, salvo que autorice otros productos.
2. Registra fecha/hora/zona, opciones, etiquetas incluidas, formato y método de entrega.
3. Descarga el archivo desde un equipo controlado; no comparte credenciales.
4. Conserva el ZIP/TGZ original sin abrir ni modificar como copia maestra.
5. Calcula SHA-256, tamaño y nombre exacto; crea un manifiesto de cada MBOX y archivo asociado.
6. Mantiene dos copias controladas en ubicaciones separadas y una copia de trabajo derivada.
7. Registra las etiquetas Gmail preservadas en cabeceras `X-Gmail-Labels` y cualquier aviso de exclusión o cambio durante la generación.

Google explica el procedimiento y las limitaciones de la exportación en [Descargar tus datos de Google](https://support.google.com/accounts/answer/3024190).

### B. Adquisición por Gmail API o conector autorizado

Después de verificar el perfil de la cuenta correcta:

1. enumerar todas las etiquetas y mensajes, incluyendo `in:anywhere` y correo eliminado todavía recuperable;
2. guardar el denominador total y cada identificador en el registro privado;
3. recuperar cada mensaje en formato `RAW`, que devuelve el mensaje RFC 2822 completo codificado en base64url;
4. recuperar y hash-controlar adjuntos y cuerpos MIME;
5. registrar errores, mensajes no recuperables, reintentos y límites de API; y
6. reconciliar los resultados contra Takeout y contra la copia corporativa.

Referencias oficiales: [Gmail API — users.messages](https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages) y [Gmail API — Format](https://developers.google.com/workspace/gmail/api/reference/rest/v1/Format).

## 4. Reconciliación y deduplicación

La adquisición no se declara completa hasta comparar:

- total de mensajes y cobertura temporal de Takeout, API y buzón corporativo;
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

`RDM-PRIVATE-MAILBOX-01` permanece **PARCIAL / NO ADQUIRIDO EN SU TOTALIDAD** hasta que la titular autorice y complete Takeout o conecte la cuenta correcta, se verifique el perfil y se reconcilien los denominadores. Los 2.413 mensajes reflejados preservan un punto de partida importante, especialmente desde 2012, pero no autorizan la expresión «todos los correos de la declarante».
