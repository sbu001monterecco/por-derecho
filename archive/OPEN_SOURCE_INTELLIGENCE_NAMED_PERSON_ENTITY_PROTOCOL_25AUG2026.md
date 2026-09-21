# Protocolo OSINT para personas y entidades nombradas

**Fecha:** 25 de agosto de 2026

**Ámbito:** toda investigación, mapa, ficha, declaración o publicación Por Derecho que nombre a una persona, sociedad, despacho, órgano, comunidad o relación entre ellos

**Estado:** regla de verificación, minimización, contradicción, enlace, actualización y derecho de respuesta

## 1. Objeto y límite

OSINT organiza fuentes abiertas verificables; no autoriza intrusión, suplantación, acceso a cuentas privadas, compra encubierta de datos, contacto engañoso, seguimiento físico ni publicación desproporcionada de datos personales. La inclusión en un mapa no prueba conducta ilícita.

## 2. Ficha mínima de identidad

Antes de vincular un nombre, registrar:

- nombre legal exacto y variantes controladas;
- riesgo de homónimos y criterio de desambiguación;
- persona física/jurídica u órgano;
- capacidad concreta, fecha de inicio/fin y jurisdicción;
- identificador público legítimo cuando sea necesario, sin publicar DNI/NIF, domicilios privados, teléfonos o correos personales;
- fuente directa, fecha de la fuente, fecha de acceso, página/línea/asiento; y
- si la fuente acredita un hecho histórico, un estado actual o sólo una alegación.

Una identidad no se cierra por nombre y región solamente. Salvo identificador oficial inequívoco, requiere al menos dos atributos independientes compatibles —por ejemplo nombre completo más fecha/capacidad, hoja registral, colegio, órgano, domicilio profesional o documento del expediente— y ausencia de una contradicción material. Si no se alcanza ese umbral, el estado es **`IDENTIDAD_ABIERTA`** y el literal se conserva sólo como alias de búsqueda.

Las relaciones familiares o íntimas no se infieren por apellidos, domicilio, trabajo o entorno. Sólo se registran si son materialmente necesarias y están acreditadas por una fuente legítima.

## 3. Jerarquía de fuentes

Preferir, en este orden, y registrar el nivel:

1. `O1` — resolución, expediente, escritura, asiento o publicación oficial;
2. `O2` — registro profesional, regulador o colegio oficial;
3. `O3` — documento corporativo o institucional primario;
4. `O4` — comunicación contemporánea autenticada y lícitamente utilizable;
5. `O5` — fuente periodística o académica identificable y contrastada; y
6. `O6` — web corporativa, biografía interesada, agregador, red social u otra fuente abierta no verificada.

Una fuente secundaria puede abrir una línea de búsqueda, pero no desplaza una fuente primaria contraria. Una captura o copia se enlaza a su origen y se preserva con fecha; no se presenta como certificación.

## 4. Tipos de relación

Cada arista debe etiquetarse y fecharse por **naturaleza**:

- `R1 — societaria/registral`;
- `R2 — profesional o de mandato`;
- `R3 — procesal o institucional`;
- `R4 — comunitaria/propiedad/representación`;
- `R5 — comunicación o reunión documentada`.

Por separado se asigna un **estado probatorio**: `OFICIAL_FECHADO`, `DOCUMENTAL_PROYECTO`, `AUTO_DESCRITO`, `ATRIBUIDO`, `INFERIDO`, `NO_LOCALIZADO`, `CONTRADICHO/CORREGIDO` o `IDENTIDAD_ABIERTA`. Naturaleza y estado no se mezclan: una relación profesional puede estar oficialmente fechada, sólo atribuida o no localizada.

Una relación histórica no se describe como actual sin certificado o fuente vigente. Un cargo en una sociedad no prueba intervención en cada asunto de la sociedad. Una relación entre A y B, y otra entre B y C, no prueba relación, comunicación o coordinación entre A y C.

Registrar separadamente persona, entidad, cargo, fecha de inicio/fin, fuente y vigencia. Una firma creada en una fecha posterior no recibe retrospectivamente los mandatos personales anteriores de sus futuros socios sin hoja de encargo, poder, factura, escrito u otro puente contemporáneo.

## 5. Regla contra la transferencia de responsabilidad

No transferir por asociación:

- conocimiento;
- intención;
- control;
- autoría;
- beneficio;
- conflicto profesional;
- responsabilidad civil, penal, concursal o deontológica; ni
- pertenencia a un supuesto grupo coordinado.

Para cada acusación se exige actor, capacidad, fecha, acto/omisión, fuente, conocimiento, intención cuando proceda, efecto, causalidad, beneficio/daño, prueba contraria y estado procesal.

## 6. Búsqueda reproducible y negativa

Registrar para cada escaneo:

- consultas exactas y variantes nominales;
- dominios y registros revisados;
- rango temporal y fecha de acceso;
- resultados incluidos y excluidos, con razón;
- homónimos descartados;
- búsquedas de prueba contraria o explicación inocente; y
- límite del universo revisado.

**`NO LOCALIZADO` no significa inexistencia.** Significa sólo que el extremo no apareció en ese conjunto, consulta y fecha. Las búsquedas alrededor de un año deben indicar la ventana revisada y no convertir un índice finito en certificado universal de ausencia.

## 7. Publicación y derecho de respuesta

Toda ficha pública de una persona o entidad debe mostrar:

- identidad controlada y capacidad por fecha;
- hechos verificados con enlace directo a la fuente;
- alegaciones atribuidas con su fuente;
- inferencias expresamente marcadas;
- relaciones buscadas pero no probadas;
- resoluciones adversas, negaciones y explicaciones alternativas;
- preguntas/documentos capaces de confirmar o refutar; y
- vía visible de corrección o respuesta.

Las versiones española e inglesa deben conservar el mismo nombre, capacidad, fuente, estado y límite. No se añaden acusaciones en una lengua que falten en la otra.

## 8. Privacidad y proporcionalidad

No publicar direcciones residenciales, correos privados, teléfonos, firmas, identificadores personales, cuentas, datos bancarios/fiscales, nombres de hijos u otros datos no necesarios. Si un dato privado es material, conservarlo en la capa restringida y publicar sólo la proposición y procedencia mínimas.

## 9. Actualización, corrección y enlaces muertos

- Registrar fecha de acceso y alcance temporal de cada fuente.
- Volver a comprobar cargos actuales antes de describirlos en presente.
- Preservar referencia oficial, identificador de publicación y página/asiento para recuperar un enlace roto.
- Incorporar correcciones documentadas sin borrar la versión anterior.
- Revisar periódicamente fichas de personas vivas o sociedades activas si la actualidad es material.

## 10. Primera aplicación controlada

El [escaneo unitario Campanario–Prieto Puente–López Noriega–Comunidad](./CAMPANARIO_PRIETO_NORIEGA_COMMUNITY_CORPORATE_UNITARY_SCAN_25AUG2026.md) constituye la primera aplicación fechada de este protocolo. Sus resultados controlantes incluyen:

- corrección de nombres y sociedades;
- rastro oficial de Álvaro Campanario Hernández en 1995 y 2004, y ausencia limitada en el índice de 2000 revisado;
- vínculo oficial Prieto Puente–López Noriega mediante Millan and Miners, S.L.P.;
- vínculo oficial Prieto Puente–Antonio Cogolludo mediante Santa Lucia Real Estate, S.L.;
- capacidades oficiales de Antonio Cogolludo en Pamalexsha y Explotaciones Noalpa; y
- ausencia, dentro del escaneo finito, de varias relaciones societarias alegadas.

Ninguno de esos vínculos demuestra por sí solo conocimiento, coordinación, conflicto o responsabilidad.
