# Protocolo unitario de declaraciones de voz a texto, hechos y veracidad

**Fecha de control:** 25 de agosto de 2026

**Ámbito:** Gil Marer; Testigo del perímetro de Gil Marer — identidad reservada; cualquier otra persona relacionada; todo audio, dictado, nota de voz, transcripción automática, resumen oral o texto preparado a partir de ellos

**Estado:** control obligatorio de adquisición, atribución, adopción, contradicción, privacidad y publicación

**No sustituye:** el audio nativo, una declaración firmada, una ratificación personal, un peritaje de voz, un documento primario ni una resolución

## 1. Regla rectora

Un texto presentado como procedente de una voz puede conservar información valiosa, pero deben separarse siempre cinco cuestiones:

1. **procedencia técnica:** de qué aplicación, cuenta, dispositivo, hilo, archivo o exportación procede;
2. **atribución de hablante:** por qué se atribuye cada segmento a una persona;
3. **fidelidad de transcripción:** qué palabras se oyen y qué cambios editoriales se hicieron;
4. **adopción personal:** si la persona revisó y adoptó la redacción exacta; y
5. **veracidad material:** qué proposiciones se corroboran, contradicen o permanecen abiertas.

Ninguna de esas capas demuestra automáticamente las otras. La atribución de un texto no autentica biométricamente una voz; una voz auténtica no hace verdadero su contenido; una transcripción fiel no equivale a ratificación; y la expresión «declaración de veracidad» sólo puede utilizarse como adopción personal cuando el declarante ha revisado y adoptado el texto exacto.

Mientras falte esa adopción, la denominación correcta es **declaración registrada derivada de fuente** o **transcripción de trabajo atribuida**, según corresponda.

### 1.1 Regla de pausa y captura exclusiva

Si el hablante anuncia que seguirá con otro audio o pide expresamente que todavía no se analice, el sistema entra en **modo de captura**: conserva el orden y la atribución provisional, pero no analiza, sintetiza, corrige, finaliza ni publica. Una pausa, desconexión o cambio de hablante no equivale a cierre. Sólo una instrucción expresa de cierre o de comienzo del análisis permite reanudar esas tareas.

### 1.2 Ejes independientes y estados de adopción

Cada proposición mantiene cinco ejes ortogonales: versión de fuente `V0–V4`, grado de atribución `S0–S4`, estado de adopción personal, clase `P1–P8` y estado de corroboración. La firma, el juramento, la presentación institucional y la corroboración son hechos separados; ninguno se infiere de otro.

Estados de adopción controlados: **capturada**, **transcrita**, **atribuida**, **registrada**, **revisada**, **ratificada**, **firmada**, **jurada o formalizada**, **presentada**, **suplementada** y **supersedida/corregida**. Deben registrarse con alcance, fecha y medio; una etiqueta global no sustituye la adopción proposición por proposición.

## 2. Captura mínima antes de redactar

El registro privado de custodia debe conservar, cuando esté disponible:

- identificador público seguro de la fuente y localizador privado estable;
- aplicación, cuenta/custodio, conversación o hilo de origen;
- fecha, hora y zona horaria de creación, recepción y exportación;
- número, orden y continuidad de los segmentos;
- tipo de archivo, códec, duración, tamaño y nombre nativo;
- método y fecha de exportación;
- SHA-256 del archivo nativo y de cada derivado;
- identidad de quien entregó, recibió, exportó o transcribió;
- indicación de pausas, cortes, solapamientos, ediciones o segmentos ausentes; y
- vínculo entre audio, transcripción literal, versión editada y declaración resultante.

El repositorio público conserva sólo referencias seguras, estados y hashes cuando no revelen datos personales. No publica el audio bruto, nombres privados de archivos, números de teléfono, direcciones privadas, identificadores de cuenta, mensajes completos ni metadatos sensibles.

## 3. Capas de transcripción y control de versiones

Cada fuente de voz debe distinguir, sin sustitución silenciosa:

| Capa | Contenido | Uso |
|---|---|---|
| `V0 — fuente nativa` | archivo original sin modificación | autenticación y custodia privada |
| `V1 — transcripción literal` | palabras audibles, dudas, pausas y segmentos ininteligibles | control de fidelidad |
| `V2 — versión de trabajo corregida` | puntuación, nombres y ordenación editorial identificados | análisis; no adopción automática |
| `V3 — versión revisada por el declarante` | correcciones aceptadas o formuladas por la persona | adopción documentada, con alcance exacto |
| `V4 — versión formal controlada` | texto firmado, jurado o presentado, registrando por separado cada acto y justificante | versión controlante para tenor dentro del alcance adoptado, sin borrar V0–V3 ni convertir presentación en corroboración |

Las correcciones de nombre, fecha o cifra deben quedar en una tabla de cambios. Si una versión posterior modifica una proposición material, la anterior se marca **SUPLEMENTADA**, **SUPERSEDIDA** o **CONTRADICHA/CORREGIDA**, pero no se elimina.

La revisión de transcripción debe marcar ininteligibles, solapamientos, autocorrecciones y dudas; comprobar especialmente nombres, negaciones, fechas, cifras, porcentajes y unidades; y separar puntuación editorial de palabras audibles. Un documento localizado después puede corroborar o corregir una proposición, pero no se inserta retrospectivamente dentro de las palabras del hablante.

## 4. Grado de atribución del hablante

La atribución se registra por segmento, no sólo por archivo:

| Grado | Base disponible | Formulación permitida |
|---|---|---|
| `S0` | hablante desconocido o fuente no recuperada | voz no identificada |
| `S1` | atribución de un participante o transmisor | participante atribuye la voz a X |
| `S2` | cuenta, dispositivo, contexto o continuidad corroboran la atribución | atribución contextual corroborada |
| `S3` | la persona confirma separadamente que es su voz o adopta el segmento | voz/contenido confirmado por el declarante, con alcance indicado |
| `S4` | autenticación técnica o pericial independiente | atribución técnicamente autenticada dentro del alcance del informe |

No se eleva el grado por repetición, familiaridad narrativa, coincidencia con otro relato o instrucción de un tercero. La atribución de Gil sobre una voz atribuida a otra persona es `S1` salvo corroboración adicional; no convierte sus palabras en declaración conjunta.

## 5. Clasificación obligatoria de cada proposición

Toda proposición material se etiqueta como una de estas clases:

- `P1 — percepción o participación directa`;
- `P2 — recuerdo sujeto a precisión`;
- `P3 — palabras o conducta atribuidas a un tercero`;
- `P4 — conocimiento obtenido de documentos`;
- `P5 — inferencia, sospecha u opinión`;
- `P6 — alegación jurídica o posición de parte`;
- `P7 — hecho oficial verificado dentro del alcance de una fuente`; o
- `P8 — cuestión abierta / REQUIERE ACLARACIÓN`.

Por separado se registra el estado de contraste: **corroborada**, **parcial**, **contradicha/corregida**, **no localizada**, **no probada** o **pendiente**. «No localizada» nunca significa «inexistente».

## 6. Separación de declarantes

Gil Marer, la Testigo del perímetro de Gil Marer — identidad reservada y cualquier otra persona son voces probatorias separadas.

**No se mezclan voces.** Cada segmento, proposición, corrección y adopción conserva su hablante propio.

- Una persona no adopta las palabras de otra por relación personal, profesional, societaria o procesal.
- Una instrucción para archivar el relato de otra persona acredita la instrucción, no la verdad material ni la adopción de cada frase.
- Una declaración conjunta sólo existe si cada participante revisa y adopta por separado la versión exacta y se documenta el alcance de cada adopción.
- Si dos relatos convergen, se registra la convergencia como dos fuentes; si divergen, se preservan ambos sin fusionarlos.
- Las entrevistas posteriores se realizan por separado antes de mostrar a una persona el relato de otra, para reducir contaminación, sugestión o armonización retrospectiva.

## 7. Protocolo de aclaración y contradicción

Antes de citar públicamente una declaración de voz o convertirla en declaración de veracidad:

1. separar hechos observados, documentos, palabras de terceros e inferencias;
2. comparar cronología, cifras, capacidades, personas presentes y objeto de cada reunión o acto;
3. buscar documentos y testimonios que apoyen **y** debiliten el relato;
4. conservar resoluciones adversas, negaciones y explicaciones inocentes al lado de la acusación;
5. formular preguntas finitas, neutrales y contestables;
6. pedir a cada declarante que corrija o adopte sin sugerirle la respuesta de otro; y
7. registrar la respuesta, la falta de respuesta o la imposibilidad de aclarar sin inventar cierre.

Una contradicción puede deberse a memoria, fecha, vocabulario, distinta perspectiva, información posterior o desacuerdo material. No demuestra por sí sola falsedad deliberada ni falta general de fiabilidad.

## 8. Presión, capacidad y condiciones de declaración

Cuando se alegue presión, dependencia, enfermedad, miedo, conflicto o interferencia:

- registrar persona, acto, fecha, contexto, palabras o conducta, efecto alegado y fuente contemporánea;
- no convertir una presión limitada en incapacidad general;
- no usar la capacidad profesional de una persona para descartar automáticamente presión concreta;
- preguntar si la persona desea corregir, retirar, limitar o mantener cada proposición; y
- preservar las versiones anteriores y la explicación del cambio.

## 9. Acusaciones graves y derecho de respuesta

Las afirmaciones sobre fraude, concierto, falsedad, prevaricación, corrupción, conflicto profesional, conocimiento, intención o beneficio se conservan como alegaciones atribuidas mientras no exista prueba o decisión suficiente. La redacción pública debe:

- identificar el acto y la capacidad concretos;
- enlazar la fuente y su fecha;
- mostrar el límite probatorio y la prueba adversa;
- evitar transferir conocimiento, intención o responsabilidad por asociación;
- ofrecer una vía visible de corrección o respuesta documentada; y
- actualizar el registro sin borrar la procedencia anterior.

## 10. Privacidad, privilegio y publicación

El corpus privado puede contener audio, transcripción completa, identidad legal, correos, asesoramiento privilegiado y localizadores nativos. La capa pública se limita a derivados necesarios y redactados. Antes de publicar se revisan:

- identidad reservada y riesgo de identificación indirecta;
- datos de contacto, direcciones, firmas, documentos de identidad y datos bancarios o fiscales;
- comunicaciones abogado–cliente y estrategia procesal;
- datos de terceros no necesarios; y
- proporcionalidad entre interés probatorio y exposición pública.

La regla pública es **excluir audio bruto**, transcripciones de trabajo completas, localizadores nativos y metadatos sensibles salvo autorización específica, revisión de privacidad/privilegio y necesidad proporcionada. Codificar o comprimir un archivo no lo vuelve privado.

## 11. Criterio de cierre

Una declaración de voz está preparada para uso público controlado sólo cuando consten:

- fuente y límites de adquisición;
- hablante y grado de atribución por segmento material;
- versión de transcripción utilizada;
- estado de adopción exacto;
- clasificación de cada proposición material;
- matriz de corroboración, contradicción y aclaración;
- revisión de privacidad/privilegio; y
- enlace a correcciones, declaraciones relacionadas y evidencia primaria.

El entregable mínimo incluye: ficha privada de fuente y custodia; mapa de segmentos y hablantes; transcripción/versiones; matriz de proposiciones con los cinco ejes; tabla de correcciones y contradicciones; decisión de privacidad/privilegio; y derivado público autorizado, si procede. Sin esos controles el material puede preservarse como intake, pero no se presenta como declaración personal de veracidad adoptada.

La [cola de aclaraciones de 25 de agosto de 2026](./GIL_RESERVED_DECLARANT_VOICE_STATEMENT_CLARIFICATION_QUEUE_25AUG2026.md) aplica este protocolo al material actualmente conocido de Gil y de la declarante reservada.
