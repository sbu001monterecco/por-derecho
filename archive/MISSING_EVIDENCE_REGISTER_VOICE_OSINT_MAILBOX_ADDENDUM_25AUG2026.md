# Continuación especializada del registro de evidencia faltante — voz, buzón privado y OSINT

**Fecha:** 25 de agosto de 2026

**Ámbito:** adquisición completa del buzón privado de la declarante reservada; autenticación y adopción de declaraciones de voz; cierre de relaciones OSINT

**Relación:** continuación namespaced de `MISSING_EVIDENCE_REGISTER.md`; no renumera ni duplica `ME-001`–`ME-087`

**Crosswalk canónico:** este archivo descompone trabajo operativo; no crea un segundo registro maestro. `ME-MAIL-RDM-001` desarrolla ME-090; `ME-VTT-001`–`ME-VTT-003` desarrollan ME-091; y `ME-OSINT-001` desarrolla principalmente ME-088/ME-089. El estado superior se cierra primero en `MISSING_EVIDENCE_REGISTER.md` y después se propaga aquí.

| ID | Evidencia necesaria | Qué resolvería | Estado actual | Acción de cierre | Estado |
|---|---|---|---|---|---|
| `ME-MAIL-RDM-001` | exportación nativa completa y autorizada de `RDM-PRIVATE-MAILBOX-01`, perfiles/etiquetas, manifiesto, hashes y reconciliación | denominador completo, autenticación, mensajes ausentes de la copia conectada, adjuntos, borrados/etiquetas y procedencia | tras el aviso de las 22:49 UTC, el buzón receptor autenticado verificó aproximadamente a las 23:13 UTC una transmisión de la titular. El mensaje nativo recibido y un libro-manifiesto quedaron preservados y hash-controlados en privado. La Fase A pública-segura reconcilia aproximadamente 10,6 mil filas de correo, 4,3 mil hilos, 9,0 mil filas de adjuntos, 4,9 mil filas de procedencia/variantes y cientos de filas de actores/direcciones y búsquedas, pero no entregó los correos ni adjuntos nativos indexados; Drive no estuvo disponible/conectado; no existen hashes de los adjuntos subyacentes; y la marca «probablemente ausente» no fue contrastada con el archivo contraparte. El corpus contraparte de más de 2.400 mensajes sigue siendo un conjunto parcial separado. El manifiesto no añade apoyo probatorio a `ALG-ENT-018`; todo original decisivo no adquirido queda `NOT YET TESTABLE FROM MANIFEST` | ejecutar `prompts/RDM_PRIVATE_MAILBOX_UNITARY_CRIMINAL_ENTERPRISE_ANALYSIS_PROMPT_26AUG2026.md`; completar Takeout y/o API RAW; adquirir por lotes los correos y adjuntos nativos; obtener Drive propio/compartido/enlazado, exportaciones nativas y revisiones; hash-controlar, registrar errores y reconciliar Message-ID/hilos/MIME/archivos con el corpus contraparte; aplicar privilegio, privacidad, relevancia y revisión favorable/adversa/contradictoria; tras búsqueda completa, convertir la ausencia en no establecida/material contrario | **FASE A MANIFIESTO COMPLETA / FASE B PARCIAL Y CRÍTICA — ORIGINALES, DRIVE Y RECONCILIACIÓN ABIERTOS** |
| `ME-VTT-001` | audios nativos, orden de segmentos, metadatos, exportación y hashes de las declaraciones derivadas de voz | atribución por hablante, integridad, cortes, fidelidad y continuidad | textos y atribuciones conversacionales disponibles; audio nativo/hash no controlado para todo el corpus | inventario V0–V4 y grados S0–S4 bajo el protocolo de 25-ago | **PARCIAL / CRÍTICA** |
| `ME-VTT-002` | revisión y adopción separada de la declarante reservada | qué texto acepta, corrige o rechaza; qué conoció directamente o por documentos/terceros | Declaración 011 no ratificada palabra por palabra; tensiones delimitadas | cerrar `VQ-P-001`–`VQ-P-010` mediante entrevista separada y tabla de cambios | **ABIERTA / CRÍTICA** |
| `ME-VTT-003` | adopción separada de Gil de las proposiciones que afirma como propias | impide convertir atribución o coordinación en declaración conjunta | Gil atribuyó el relato, pero no adopta automáticamente sus frases | cerrar `VQ-G-001`–`VQ-G-008` y conservar divergencias | **ABIERTA / ALTA** |
| `ME-OSINT-001` | certificados/expedientes y mandatos que cierren capacidades históricas y relaciones alegadas | vigencia, homónimos, encargo por asunto, relevo profesional, título/poder/voto y relaciones no probadas | BORME/BOE/ICALPA y actas verifican relaciones limitadas; amistad, coordinación, handoff, conflicto y varias aristas societarias no probadas | certificados actuales/históricos, hojas de encargo, venia, escritos, poderes, notas simples y derecho de respuesta | **PARCIAL / ALTA** |

## Reglas de uso

- No publicar la dirección exacta de `RDM-PRIVATE-MAILBOX-01`, contenidos de correos, audios, identificadores o localizadores privados.
- Un recuento de mensajes o una coincidencia nominal no acredita relevancia, autenticidad, conocimiento, intención ni responsabilidad.
- La respuesta de un declarante no sustituye la del otro.
- Cerrar un ID requiere actualizar el protocolo, la declaración afectada, el registro de correcciones y cualquier página pública que reproduzca la proposición.
