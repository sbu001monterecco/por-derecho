# Declaraciones / Statements of Truth

Repositorio permanente de declaraciones personales vinculadas al proyecto Por Derecho y a la reconstrucción documental del Concurso Ordinario 36/2012 y asuntos conexos.

## Finalidad

Este directorio conserva declaraciones fechadas de personas con conocimiento personal o documental de hechos relevantes. No sustituye a los documentos primarios, resoluciones, escrituras, testimonios, registros ni expedientes oficiales. Su función es preservar memoria, identificar fuentes, separar conocimiento personal de inferencia y facilitar la verificación posterior.

## Uso de declaraciones no firmadas

La firma **no es requisito para que una declaración exista en el repositorio ni para que pueda conservarse, citarse, comunicarse o utilizarse** como relato fechado, fuente de investigación, índice de hechos o solicitudes documentales, material de trabajo jurídico o comunicación institucional.

El estado de autenticación debe describirse con exactitud:

- una declaración no firmada no se describirá como **firmada**, **jurada** o **ratificada**;
- cuando derive de audio, correo, notas u otro relato personal, se identificará la fuente y se preservarán, fuera del repositorio público cuando corresponda, los originales y metadatos;
- la ausencia de firma puede afectar el peso, la autenticación o los requisitos formales que aplique un destinatario concreto, pero no vuelve inutilizable la declaración;
- si posteriormente existe una versión firmada o ratificada, ésta prevalecerá para la autenticación y el tenor exacto en caso de diferencia, sin borrar ni invalidar el historial anterior;
- la versión anterior permanece preservada como parte de la cadena de procedencia y del registro de correcciones.

Una versión preparada por terceros a partir de audios o documentos, pero no revisada personalmente por el declarante, debe indicarlo expresamente. Puede usarse como **declaración registrada derivada de fuente**, pero no como prueba de adopción personal de cada palabra del texto.

## Reglas de integridad

1. Cada declaración debe identificar claramente al declarante, fecha y lugar.
2. Debe distinguir entre: conocimiento personal directo; recuerdo; conocimiento derivado de documentos; manifestaciones atribuidas a terceros; inferencia o entendimiento; y extremos que requieren verificación.
3. No se presentarán como hechos probados las alegaciones no corroboradas.
4. La firma no es condición de uso. La versión firmada o ratificada, cuando exista, controla la autenticación y el tenor exacto en caso de diferencia.
5. Cuando exista versión firmada, deberá conservarse su hash SHA-256, nombre exacto de archivo y, si fue presentada institucionalmente, el justificante REG-AGE/RedSARA correspondiente.
6. Cuando la fuente sea audio, correo, mensajería o notas, deberán preservarse, cuando sea posible, el archivo nativo, exportación, metadatos, fechas, hashes y relación entre la fuente y la declaración.
7. Toda corrección posterior se hará mediante una nueva versión o declaración suplementaria, sin borrar silenciosamente la versión anterior.
8. Las declaraciones públicas destinadas al sitio web deberán redactarse con cautela para no atribuir delitos, dolo o responsabilidad como hechos establecidos sin resolución o prueba suficiente.
9. No se publicarán audio bruto, transcripciones íntegras, datos personales innecesarios, material privilegiado o estrategia procesal salvo decisión expresa, revisión de privacidad y base legítima.
10. Si una frase material no puede afirmarse responsablemente en el nivel en que está redactada, debe marcarse **`REQUIERE ACLARACIÓN`** o reformularse como recuerdo, manifestación de tercero, conocimiento documental, inferencia o cuestión pendiente. No se inventará certeza para completar una declaración.
11. La evidencia exculpatoria, las negaciones y las explicaciones alternativas deben preservarse con el mismo rigor que la evidencia adversa.
12. El número secuencial refleja el **orden de incorporación al archivo**, no necesariamente la fecha del hecho ni la fecha de la declaración fuente.

## Hacer una declaración accionable

Cuando la declaración genere cuestiones verificables, debe añadirse, después del relato y separado claramente de los hechos, un **“Apéndice operativo — acciones derivadas”**. Su función es convertir el testimonio en tareas finitas sin fortalecer la acusación. Puede incluir:

- documentos concretos que deben preservarse u obtenerse;
- custodios, sistemas y periodos;
- personas que deben ser entrevistadas por separado;
- metadatos, registros, contabilidad, extractos o expedientes a conciliar;
- explicaciones contradictorias o exculpatorias que deben probarse;
- autoridades, órganos o terceros a los que puede dirigirse una solicitud documental;
- el criterio objetivo que permitiría confirmar o descartar cada hipótesis.

El apéndice **no forma parte de la declaración de hechos** y no convierte una inferencia en hecho probado.

## Convención de nombres

`NNN_APELLIDO_NOMBRE_TEMA_AAAAMMDD.md`

Ejemplos:

- `001_DOMINGUEZ_PATRICIA_TESTIMONIO_2018_20260815.md`
- `002_DOMINGUEZ_PATRICIA_RICPE_MENSAJES_VOZ_20260815.md`
- `003_DOMINGUEZ_PATRICIA_REUNION_CAM_COMPARECENCIA_20260727.md`

## Estado de las declaraciones

- **BORRADOR**: preparada pero no adoptada ni registrada como relato atribuible; puede usarse como material de trabajo, no como declaración personal adoptada.
- **REGISTRADA**: incorporada al repositorio con fecha, fuente y límites; puede utilizarse aunque no esté firmada.
- **REVISADA**: revisada o confirmada por el declarante; puede estar firmada o no.
- **FIRMADA**: firmada por el declarante; versión de autenticación reforzada y controlante para el tenor exacto si difiere.
- **PRESENTADA**: presentada ante una institución; debe vincularse al justificante.
- **SUPLEMENTADA**: existe una declaración posterior que la amplía o corrige.

Los estados pueden combinarse, por ejemplo: `REVISADA Y REGISTRADA — no firmada` o `FIRMADA Y PRESENTADA`.

## Flujo operativo para cualquier hilo

1. Leer `README.md`, `INDEX.md` y `STATEMENT_TEMPLATE.md`.
2. Recuperar la fuente completa antes de redactar si está disponible.
3. Verificar el último número real del archivo y asignar el siguiente.
4. Convertir el relato en primera persona sin añadir hechos.
5. Clasificar las proposiciones materiales por fuente y nivel de conocimiento.
6. Marcar `REQUIERE ACLARACIÓN` cuando corresponda sin bloquear el resto de la declaración.
7. Añadir el apéndice operativo cuando existan verificaciones derivadas.
8. Actualizar `INDEX.md` en la misma rama.
9. Usar rama protegida, pull request y merge cuando proceda.
10. Verificar después del merge que la declaración y el índice existen en `main`.

La instrucción completa y reutilizable está en [`ACTION_PROMPT.md`](./ACTION_PROMPT.md).

## Índice

Véase [`INDEX.md`](./INDEX.md).

## Plantilla

Véase [`STATEMENT_TEMPLATE.md`](./STATEMENT_TEMPLATE.md).
