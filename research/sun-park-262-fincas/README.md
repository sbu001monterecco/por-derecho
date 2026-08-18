# Sun Park — registro maestro de 262 fincas

**Estado:** base de investigación para un hilo/tarea separado y futuro.  
**Objeto:** impedir que el análisis de Sun Park vuelva a colapsar 262 fincas registrales en una sola narrativa de “el hotel”.

## 1. Fuente canónica para las 262 fincas

`sun-park-262-fincas.csv` contiene **262 filas, una por finca**, con `registry_finca` único y `unit` consecutivo 1–262.

La geometría/base histórica procede de la hoja **GESVALT** del archivo de trabajo:

- `Anexo III - Responsabilidad Máxima Hipotecaria - Intereses y Swap 1SEP2022`
- columnas de origen: UNIT, REGISTRY, NAME, NUMBER, APT Nº, AREA m2, OWNER, VALUE, VALUE SQM, CUOTA %, VALOR/CUOTA, VALUE SQM II, VALOR/UNIDAD.

**Cautela esencial:** `owner_as_listed_gesvalt` conserva lo que decía esa fuente histórica. **No se presenta como titularidad registral actual** ni como prueba suficiente de una transmisión.

No se usa como fuente canónica la hoja `AC Proposal`: su propio resumen totaliza 261 unidades y el control de integridad detecta, entre las filas con finca explícita, **8497 duplicada y 8500 ausente**. Esa anomalía se preserva para el futuro análisis, no se corrige silenciosamente.

## 2. Capa Aweswell / Matkator

Se ha cruzado, exclusivamente por número de finca y sin copiar datos personales, la hoja histórica **`Fincas Matkator - Caixa`** en `acquisition-overlay.csv`.

La hoja marca como **“En Propiedad”**:

- **8497**
- **8498**
- **8584**
- **8587**
- **8588**

y registra muchas otras fincas como **“Pdte. Compraventa”** dentro de la estrategia de adquisición, incluyendo **8503–8507 (JSP)** y **8499–8500 (Montelanza)**.

Esto no convierte automáticamente una negociación pendiente en un derecho real. La columna `matkator_acquisition_status` conserva exactamente la categoría de la fuente de trabajo para que el futuro análisis pueda separar: propiedad, contrato, negociación, pago, escritura, presentación registral y adquisición frustrada.

### P0 — cadena Matkator que debe reconstruirse primero

Un escrito judicial de MATKATOR de marzo de 2025 afirma que:

- **8584 y 8588** seguían siendo propiedad de MATKATOR según notas simples de 30/01/2025;
- **8497 y 8498** aparecían registradas a nombre de Hotel New Trend desde diciembre de 2022, transmisión que MATKATOR afirma desconocer y cuya causa cuestiona.

La base por tanto marca estas fincas como **cadena disputada**, no como “fraude probado”. Debe localizarse y comparar para cada una: escritura de adquisición Matkator, asiento de presentación, título que llevó a CAM/HNT, facultades del transmitente, precio/pago, documentos concursales y certificación registral.

**8587** también figura “En Propiedad” en la hoja histórica y queda expresamente abierta para la misma reconstrucción documental.

## 3. P0 — JSP: 8503–8507

Las cinco fincas contiguas **8503, 8504, 8505, 8506 y 8507** forman un bloque excepcional.

La fuente GESVALT las identifica bajo José Sánchez Peñate; las notas simples históricas localizadas sitúan la adquisición JSP en 2009 y las mantenían a nombre de JSP en abril de 2017. La hoja Matkator las incluye posteriormente dentro de la cartera de adquisición pendiente. Otras fuentes de trabajo posteriores las sitúan en el perímetro CAM.

La tarea futura no debe preguntar sólo “¿quién las compró?”. Debe reconstruir **JSP → negociación Matkator/Aweswell → CAM/HNT** y comprobar si la Comunidad de Propietarios, la Comunidad de Explotación o terceros intervinieron mediante deuda, certificación, voto, poder, cobro, ocupación, obra o instrumento de transmisión.

## 4. P0 — Montelanza: 8499–8500

Las fincas **8499 y 8500** se separan del bloque JSP.

Una hoja histórica de junio de 2018 las anotó como **“MONTELANZA !!! sold by CP!!!”**. Debe determinarse exactamente qué significa `CP` en el documento originario y cuál fue el título, órgano, autorización, precio y flujo de fondos.

No se debe extrapolar esta anotación a 8503–8507 sin documento equivalente.

## 5. Montelanza / Molina / CAM: estándar de revisión reforzada

Project Sun Rock considera que **toda adquisición de CAM procedente del perímetro Montelanza/Molina merece revisión finca por finca**, pero la etiqueta `MOLINA_WORKING_PERIMETER_REVIEW` es deliberadamente una **etiqueta de investigación**, no una conclusión mercantil, penal ni de responsabilidad.

Para cada finca debe contestarse:

1. ¿Quién era el titular registral inmediatamente antes?
2. ¿Qué vínculo tenía con Montelanza, JSP/Sun Group, Molina o la Comunidad?
3. ¿Quién negoció por el vendedor y con qué poder?
4. ¿Qué escritura/auto/decreto/certificación sustentó el cambio?
5. ¿Qué precio se pactó y quién lo pagó/cobró?
6. ¿Hubo deuda de Comunidad, compensación, quita, cesión o adjudicación?
7. ¿La finca estaba dentro o fuera del concurso 36/2012?
8. ¿Existía un acuerdo previo de Aweswell/Matkator?
9. ¿Qué sabía CAM antes de adquirir?
10. ¿Cuándo entró CAM en posesión/control material?
11. ¿Fue incluida después en CAM→HNT y con qué título?
12. ¿Qué explicación alternativa/adversa existe y qué documento podría refutar la hipótesis del Proyecto?

## 6. Significado de `working_tags`

- `P0_JSP_EXCEPTIONAL`: bloque 8503–8507.
- `P0_MONTELANZA_CP_CAM`: 8499–8500.
- `P0_MATKATOR_OWNED`: “En Propiedad” según la hoja histórica Matkator.
- `DISPUTED_CHAIN_REVIEW`: requiere reconstrucción reforzada; **no significa fraude judicialmente declarado**.
- `MATKATOR_PIPELINE`: “Pdte. Compraventa” en la hoja histórica.
- `MOLINA_WORKING_PERIMETER_REVIEW`: etiqueta interna de investigación a validar documentalmente.
- `CAM_CHAIN_RECONSTRUCTION`: priorizar el instrumento y el flujo de transmisión hacia CAM/HNT.

## 7. Regla de no borrado / deletion audit

Las contradicciones se conservan. Si una valoración, lista de propietarios, nota simple, acta, escritura, hoja de adquisición o documento concursal da una versión distinta, se añade como **otra capa temporal**. No se reemplaza una fuente incómoda por una versión “limpia”.

El objetivo del futuro hilo es producir, para las 262 fincas, una matriz temporal **hecho → fuente → fecha → nivel de prueba → contradicción → explicación adversa → siguiente documento necesario**.
