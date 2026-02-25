# Guía de Costos Reales para Comercios Minoristas: Más Allá del Arancel Visible

**Audiencia:** Comercios minoristas argentinos (kioscos, almacenes, ferreterías, pequeños negocios)
**Fecha de elaboración:** Febrero 2026
**Fuente base:** Investigación oficial + adaptación de informe técnico interno (enero–febrero 2026)
**Versión:** 1.5

---

## Índice

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Taxonomía de Costos](#2-taxonomía-de-costos)
3. [Análisis por Entidad](#3-análisis-por-entidad)
4. [Comparación Transversal](#4-comparación-transversal)
5. [Escenarios de Impacto](#5-escenarios-de-impacto)
6. [Notas de Confianza y Calidad de Fuentes](#6-notas-de-confianza-y-calidad-de-fuentes)
7. [Preguntas Abiertas e Investigación Pendiente](#7-preguntas-abiertas-e-investigación-pendiente)
8. [Notas para el Desarrollo de Producto](#8-notas-para-el-desarrollo-de-producto)
9. [Desarrollo Futuro (Nice-to-Haves)](#9-desarrollo-futuro-nice-to-haves)

---

## 1. Resumen Ejecutivo

### 1.1 El problema: el precio que ves no es el precio que pagás

Cuando un banco o fintech te dice "cobramos el 1,8% en crédito", eso es solo el comienzo. El **costo real mensual** de aceptar pagos con tarjeta incluye:

- El arancel transaccional (lo que todos comunican)
- El alquiler o mantenimiento de la terminal
- La pérdida de poder adquisitivo por esperar días o semanas a que el dinero llegue a tu cuenta
- Impuestos sobre comisiones (IVA)
- Penalizaciones por inactividad o incumplimiento de condiciones
- Membresías o abonos mensuales de plataforma
- Impuestos sobre acreditaciones (SIRCREB, IIBB, Impuesto al Débito y Crédito Bancario)

Un comercio que cobra $1,5 millones por mes puede estar pagando entre **$21.780 y $81.087 en costos de cobro**, dependiendo del proveedor que elija — una diferencia de casi 4 veces.

### 1.2 Hallazgos clave

**Patrón central del mercado argentino:**
> **Bancos = costo fijo alto + tasa baja.**
> **Fintechs = sin costo fijo + tasa alta.**

El punto de inflexión es aproximadamente **$850.000 ARS/mes en ventas con tarjeta de crédito** (ver cálculo de punto de equilibrio en §4). Por encima de ese volumen, los bancos son más convenientes. Por debajo, las fintechs.

**Seis hallazgos que cambian la lógica de decisión:**

1. **La bonificación de 12 meses lo cambia todo.** BNA, BAPRO, Getnet/Santander y BBVA bonifican el alquiler de la terminal durante 12 meses. Esto elimina el principal argumento a favor de las fintechs para comercios medianos. El problema: ¿qué pasa en el mes 13?

2. **La inflación cobra un "arancel invisible".** Esperar 10 días hábiles para cobrar ventas de crédito, con una inflación mensual del 2,5%, equivale a pagar un 1,2% adicional por esas ventas. Esto hace que la ventaja nominal de los bancos sea menor de lo que parece.

3. **Cuenta DNI (BAPRO) es la anomalía del mercado.** Para comercios en Provincia de Buenos Aires con clientes del Banco Provincia, la tasa del 0,6% con acreditación inmediata vía Clave DNI no tiene precedente en el mercado. Es efectivamente un subsidio provincial a la transacción.

4. **Ualá gana en el segmento de volumen bajo-medio con liquidez inmediata.** Para un kiosco o almacén que no califica para bonificación bancaria y necesita el dinero hoy, Ualá (4,9% crédito inmediato, sin cargo fijo) supera a Mercado Pago (6,29%) por un margen significativo.

5. **Los costos de cuotas son una categoría aparte.** Los coeficientes de los planes "Ahora" y "Cuota a Cuota" representan un costo financiero que muchos comercios absorben en silencio. Un plan de 12 cuotas puede tener un coeficiente de 1.54 (noviembre 2025), lo que implica que el comercio efectivamente financia al cliente al 54%.

6. **El costo fiscal es el impuesto invisible.** Para un monotributista, el costo real de aceptar tarjeta supera en ~1,5%–2% lo que muestra cualquier tabla de tasas, por el efecto acumulado de IVA no recuperable, SIRCREB, IIBB y el Impuesto al Débito y Crédito Bancario. Ver §2.5 para el análisis completo.

---

## 2. Taxonomía de Costos

Para entender el costo real, hay que separar los costos en cuatro categorías.

### 2.1 Costos Fijos Mensuales

Son los que pagás aunque no vendas nada.

| Tipo de costo | Quién lo cobra | Rango aproximado (ARS/mes) |
|---------------|---------------|---------------------------|
| Alquiler terminal Fiserv Posnet | Bancos (vía BAPRO, BNA, Macro) | $37.979 – $46.000 + IVA |
| Alquiler terminal Clover | Bancos (vía BAPRO) | $46.389 + IVA (~$56.130 c/IVA) |
| Terminal PayWay activa | Bancos, PayWay directo | $41.999 + IVA (~$50.819) |
| Terminal PayWay inactiva | PayWay | $50.399 + IVA (~$60.983) |
| Terminal Getnet Smart/Classic | Getnet/Santander | $37.000 + IVA (~$44.770) |
| mPOS Ualá | Sin costo mensual | $0 |
| Point Mercado Pago | Sin costo mensual | $0 |
| Membresía BNA Conecta (no bonificada) | BNA | $17.500 – $175.000 |

> ⚠️ **Nota clave:** Los valores de alquiler de terminal corresponden al costo **sin bonificación**. La mayoría de los bancos bonifican el 100% durante los primeros 12 meses. Pasado ese período, el costo recae sobre el comercio a menos que renegocie.

### 2.2 Costos Variables (por transacción)

Son los que pagás proporcionalmente a tus ventas.

| Tipo de pago | Tope regulatorio BCRA | Bancos (precio real) | Ualá | Mercado Pago |
|--------------|-----------------------|---------------------|------|--------------|
| Débito       | 0,80% + IVA           | 0,80% + IVA         | 2,90% + IVA | 2,99%–3,25% + IVA |
| Crédito      | 1,80% + IVA           | 1,80% + IVA         | 4,40%–4,90% + IVA | 1,49%–6,29% + IVA |
| Crédito internacional | N/A (sin tope) | 7,50% + IVA (BNA) | No confirmado | No confirmado |
| QR Transferencia | 0,60%–0,80%       | Variable            | 0,60% | Variable |

**El IVA sobre comisiones** (21%) es un costo real para la mayoría de los monotributistas y responsables inscriptos de menor escala, aunque en algunos casos puede recuperarse como crédito fiscal. Para simplificar los cálculos, esta guía lo incluye como costo neto.

### 2.3 Costos de Acreditación (impacto de la inflación)

Este es el costo más invisible. En Argentina, con inflación mensual activa, esperar días para cobrar tiene un costo financiero real.

**Fórmula de referencia:**

```
Costo inflación = Monto de ventas a crédito × (Inflación_mensual / 30) × Días_calendario_de_espera
```

**Tabla de referencia (inflación mensual 2,5% — verificar con INDEC actualizado):**

| Plazo de acreditación | Días calendario aprox. | Costo inflación por cada $100.000 vendidos |
|-----------------------|------------------------|------------------------------------------|
| En el momento         | 0                      | $0                                       |
| 24 horas hábiles      | ~1–2 días              | ~$83                                     |
| 8 días hábiles        | ~11 días               | ~$917                                    |
| 10 días hábiles       | ~14 días               | ~$1.167                                  |
| 18 días hábiles       | ~25 días               | ~$2.083                                  |
| 35 días               | 35 días                | ~$2.917                                  |

> 📌 **Referencia de inflación:** Los cálculos de esta guía usan 2,5% mensual como valor conservador de referencia. La inflación real en Argentina varía; al momento de leer este documento, verificar el dato actualizado en **INDEC.gob.ar**. Si la inflación real es mayor, el costo de esperar es proporcionalmente mayor.

### 2.4 Costos Operativos y Penalizaciones

| Tipo                          | Quién aplica      | Descripción |
|-------------------------------|-------------------|-------------|
| Penalización por inactividad  | PayWay            | $50.399/mes (vs. $41.999 activa) — castigo por no usar la terminal |
| Cargo por contracargo (chargeback) | Todos      | Variable según entidad; puede incluir tasa administrativa más el monto disputado |
| Gestión de cobranza           | BNA               | $50 cargo único por "gestión de aceptación/cobro" (operatoria tradicional) |
| Retención IIBB PBA sobre billeteras | ARBA (PBA) | Desde oct. 2025: retención automática de 0,01%–5% sobre acreditaciones, según actividad |
| Retención SIRCREB             | ARCA/Provincias   | Aplica sobre liquidaciones de todas las redes, incluidas billeteras |
| Coeficiente de cuotas         | Todos los bancos  | Ej.: coeficiente 1.5441 para 12 cuotas (nov. 2025 — verificar actualización) |

> 📌 Las retenciones de IIBB y SIRCREB se listan aquí como costo operativo. Para el análisis fiscal completo (incluyendo Impuesto al Cheque e impacto por categoría fiscal), ver **§2.5**. Para el proceso de contracargos, ver **§2.6**. Para el análisis de coeficientes de cuotas, ver **§2.7**.

---

### 2.5 Costos Fiscales

Este es el capítulo más frecuentemente ignorado. Los impuestos sobre acreditaciones no aparecen en las tablas de tasas de ningún proveedor, pero impactan directamente el dinero que llega a la cuenta del comercio.

#### 2.5.1 IVA sobre comisiones: monotributista vs. responsable inscripto

El IVA del 21% sobre comisiones bancarias y fintech no tiene el mismo impacto para todos los comercios:

| Categoría fiscal | Tratamiento del IVA pagado en comisiones |
|-----------------|------------------------------------------|
| Monotributista | 100% costo — no lo puede acreditar ni recuperar. Los $378 de IVA en una comisión de $1.800 son pérdida neta. |
| Responsable Inscripto | Crédito fiscal IVA — lo acredita contra el IVA cobrado a sus propios clientes. Reduce el costo neto de comisión. |

**Ejemplo concreto:**
- Venta de $100.000 en crédito → comisión del 1,80% = $1.800 → IVA sobre comisión = $378
- **Monotributista:** costo real = $1.800 + $378 = **$2.178** (no $1.800)
- **Responsable Inscripto:** costo real = $1.800 (el IVA se recupera como crédito fiscal)

#### 2.5.2 SIRCREB (Sistema de Recaudación sobre Acreditaciones Bancarias)

El SIRCREB es una retención automática aplicada por ARCA (ex-AFIP) y las provincias adheridas. Opera silenciosamente: el banco o procesador descuenta el importe **antes** de acreditar el neto al comercio.

- **Cómo funciona:** La retención se aplica sobre el monto bruto acreditado, no sobre la comisión.
- **Tasas:** Varían según el código de actividad AFIP del comercio. Rango típico: **0,5%–3%** sobre el bruto acreditado.
- **Recupero:** El SIRCREB es técnicamente un **adelanto del Impuesto a los Ingresos Brutos** — no un impuesto adicional. Lo que el banco retiene ya lo tendrías que pagar como IIBB; el sistema lo recauda anticipadamente antes de que llegue la declaración mensual. Esto significa que no pagás doble, pero sí adelantás el dinero antes de necesitarlo. Se computa como crédito en tu liquidación de IIBB. Si el monto retenido supera tu obligación de IIBB del período, generás saldo a favor — recuperarlo requiere declaración ante la agencia provincial y puede demorar meses.
- **Fintechs:** Mercado Pago y Ualá exponen `tax_details` en sus reportes de liquidación, lo que facilita el uso de lo retenido como crédito fiscal.

🟡 **Confianza:** Tasas generales verificadas. Tasas específicas por actividad requieren consulta a ARCA o contador impositivo.

#### 2.5.3 IIBB (Ingresos Brutos) — Retención sobre acreditaciones

El Impuesto a los Ingresos Brutos tiene regímenes de retención diferentes por provincia:

- **PBA (ARBA):** Desde octubre 2025, retención automática de **0,01%–5%** sobre acreditaciones en billeteras digitales y procesadores, según actividad. Comercio minorista: rango típico ~0,5%–1%.
- **CABA (AGIP):** Régimen propio, aplicable a comercios radicados en Ciudad de Buenos Aires. Tasa diferente a PBA.
- **Otras provincias:** Córdoba, Santa Fe, Mendoza tienen sus propios regímenes; no están centralizados ni son comparables.

> ~~🔔 **Impuesto de Sellos CABA (derogado en marzo 2023):**~~ FECOBA y CAME rechazaron en su momento la aplicación de un Impuesto de Sellos del **1,2% sobre operaciones con tarjeta de crédito** en CABA. El impuesto fue sancionado y luego **derogado por la Legislatura CABA en marzo de 2023** — no está vigente. No representa un costo adicional para comercios en CABA.

⚠️ **Limitación importante:** Los valores en las tablas de comparación de esta guía **NO incluyen IIBB**. El costo real para comercios inscriptos es mayor.

🟡 **Confianza:** Dato verificado para PBA. 🔴 Para otras provincias requiere investigación provincial específica.

#### 2.5.4 Impuesto al Débito y Crédito Bancario ("Impuesto al Cheque" — Ley 25.413)

- **Qué es:** 0,6% sobre cada acreditación en cuenta bancaria (cuentas corrientes y cajas de ahorro).
- **A quién aplica:** Comercios con cuenta bancaria donde reciben liquidaciones de adquirentes.
- **Recupero parcial:** Monotributistas y RI pueden acreditar el 34% contra su impuesto a las ganancias. El **66% restante es costo puro**.
- **Mecanismo adicional para microempresas (RG ARCA 5632/2024):** Las microempresas pueden imputar el **30% del Impuesto al Débito y Crédito Bancario** como pago a cuenta del **15% de las contribuciones patronales al SIPA** (aportes de empleadores). El 70% restante sigue siendo computable contra Ganancias (mecanismo tradicional del 34%). Este canal de recupero adicional es relevante para negocios con empleados en relación de dependencia. Prorrogado hasta diciembre 2026 vía **RG ARCA 5817/2026** (enero 2026).
- **Asimetría fintech vs. banco:** Este impuesto **no aplica** si el dinero queda en una billetera fintech (Mercado Pago, Ualá) sin transferir a banco. Esto crea un incentivo fiscal para mantener saldos en fintechs, aparentemente contradictorio con el análisis de tasas — pero que puede ser relevante para comercios con baja demanda de liquidez bancaria.

🟢 **Confianza:** Regulado por Ley 25.413, permanece vigente.

#### 2.5.5 Tabla de Costo Fiscal Acumulado (por escenario)

Costo efectivo total sobre una venta de $100.000 en crédito, incluyendo todos los impuestos:

| Escenario | Comisión base | + IVA (21%) | + SIRCREB est. | + IIBB PBA est. | + Imp. Cheque (rec. 34%) | **Costo total efectivo** |
|-----------|--------------|-------------|----------------|-----------------|--------------------------|--------------------------|
| Monotributista, banco bonificado, 10 días hábiles | 1,80% | +0,378% (no rec.) | +0,5% (parcial rec.) | +0,5% (no rec.) | +0,40% (0,6% × 66%) | **~3,58%** |
| Resp. Inscripto, banco bonificado, 10 días hábiles | 1,80% | recupera | +0,5% (rec.) | variable | +0,40% (0,6% × 66%) | **~2,6%–2,9%** |
| Monotributista, Ualá inmediato (sin banco) | 4,90% | +1,029% (no rec.) | +0,5% (parcial) | +0,5% | 0% (no sale a banco) | **~6,93%** |
| Monotributista, Mercado Pago 18 días (sin banco) | 3,39% | +0,712% (no rec.) | +0,5% | +0,5% | 0% | **~5,10%** |

> ⚠️ Nota: estos valores son aproximaciones de orden de magnitud. Las tasas exactas de SIRCREB e IIBB varían por actividad y provincia. El punto clave es que el costo fiscal puede representar **1%–2% adicional** no visible en las tablas de comisiones.

#### 2.5.6 Programas de Incentivo para la Adopción de Pagos Electrónicos

El Estado Nacional implementó programas de incentivo fiscal para comercios que adoptan terminales POS. Estos beneficios reducen el costo neto efectivo de aceptar pagos electrónicos y son frecuentemente ignorados al calcular el costo total real.

**Para Monotributistas:**
- Sin comisión en débito: los monotributistas adheridos al programa reciben acreditación de operaciones con tarjeta de débito **sin cargo de comisión** (0% de comisión sobre débito)
- **Terminal gratuita** durante **2 años** (sin costo de alquiler mensual)

**Para Responsables Inscriptos:**
- **Terminal subsidiada o gratuita:** descuento del 50% en el costo de terminal por 6 meses, o terminal gratuita por 2 años (según el programa vigente)
- **Reducción en retenciones sobre débito:** rebaja del 50% en las retenciones de IVA e Impuesto a las Ganancias sobre operaciones con tarjeta de débito

> ⚠️ **Cómo acceder:** Estos beneficios se gestionan a través del banco adquirente o Fiserv/Prisma. Las condiciones exactas varían por programa y período fiscal. Consultar directamente con el banco o en ARCA (arca.gob.ar) para verificar la vigencia actual.

> 📌 Fuente: Guía de Pagos Electrónicos FECOBA. Para comercios CABA, FECOBA (fecoba.com.ar) ofrece asistencia en la gestión de estos beneficios.

🟡 **Confianza:** Documentado por FECOBA como beneficio vigente. Montos y condiciones exactas requieren verificación con contador o banco adquirente, ya que pueden variar por período fiscal.

#### 2.5.7 SIRTAC (Sistema de Recaudación sobre Tarjetas de Crédito y Compra)

El SIRTAC es un **tercer nivel de retención provincial** sobre operaciones con tarjeta, distinto del SIRCREB y del IIBB. Fue implementado por varias provincias y representa un costo adicional que no aparece en las tablas de comisiones de ningún proveedor.

**Cómo se diferencia del SIRCREB:**

| Característica | SIRCREB | SIRTAC |
|---------------|---------|--------|
| Qué grava | Acreditaciones bancarias en general | Específicamente operaciones con tarjetas de crédito y compra |
| Quién lo recauda | ARCA + provincias adheridas al SIRCREB | Provincias que crearon su propio sistema |
| Marco legal | Sistema nacional coordinado | Regímenes provinciales independientes |

**Impacto reportado:** CAME calificó el SIRTAC como "un nuevo golpe para las pymes", señalando que se suma a la ya alta carga de retenciones sobre operaciones con tarjeta.

**Qué hacer:** Consultar con contador impositivo o con ARCA si la provincia donde opera el comercio tiene SIRTAC vigente y cuál es la tasa aplicable a su actividad.

🔴 **Confianza:** Existencia del mecanismo confirmada (CAME vía Ámbito Financiero). Tasas específicas por provincia y actividad requieren verificación provincial.

---

### 2.6 Costos de Disputas y Contracargos

Un contracargo (chargeback) ocurre cuando el titular de una tarjeta disputa una transacción ante su banco emisor. Para el comercio, el impacto va más allá del monto disputado.

#### 2.6.1 Cómo funciona el proceso

1. El cliente disputa la transacción ante su banco emisor (el banco que emitió la tarjeta, no el del comercio)
2. El banco emisor notifica a Visa/Mastercard
3. Visa/Mastercard notifica al adquirente o agregador del comercio
4. El adquirente/agregador **retiene o debita el monto disputado** de la cuenta del comercio
5. El comercio tiene un plazo para presentar evidencia (comprobante de venta, firma, entrega, etc.)
6. Si no la presenta en tiempo, pierde el monto automáticamente

#### 2.6.2 La diferencia crítica: agregador vs. adquirente directo

Esta distinción impacta fuertemente al comercio:

| Aspecto | Banco adquirente (BNA, BAPRO, Getnet) | Agregador fintech (Ualá, Mercado Pago) |
|---------|--------------------------------------|----------------------------------------|
| Quién retiene el dinero | El banco, dentro del sistema Visa/MC | El agregador, directamente de tu saldo en la plataforma |
| Cuándo se retiene | Generalmente al inicio del proceso formal | **Inmediatamente al recibir la disputa** — antes de resolución |
| A quién le reclamás | Al banco + proceso formal Visa/MC | Al agregador (no tenés acceso directo a Visa/MC) |
| Plazo para presentar evidencia | Regulado por Visa/MC (tipicamente 7–30 días hábiles) | Definido por el agregador en sus propios términos de servicio |
| Resolución si perdés el chargeback | Débito en cuenta bancaria | Débito de tu saldo en la plataforma |

> ⚠️ En fintechs agregadoras, un chargeback puede congelar fondos de tu saldo operativo sin previo aviso, afectando tu liquidez diaria.

🔴 **Confianza:** El proceso general es estándar de la industria (Visa/MC Operating Regulations). Los plazos y mecanismos específicos de Ualá y Mercado Pago no están publicados en sus portales de ayuda para comercios en términos claros. Verificar en los Términos y Condiciones de cada plataforma.

#### 2.6.3 Exposición estimada por volumen

Tasa de chargeback típica para comercio minorista: **0,1%–0,5% de las transacciones** (referencia industria; varía por rubro).

| Volumen mensual | Tasa 0,1% | Tasa 0,5% | Riesgo anual (0,3% promedio) |
|----------------|-----------|-----------|------------------------------|
| $500.000 | $500/mes | $2.500/mes | ~$18.000 |
| $1.500.000 | $1.500/mes | $7.500/mes | ~$54.000 |
| $4.000.000 | $4.000/mes | $20.000/mes | ~$144.000 |

> 📌 Para ferreterías y negocios que venden a crédito en cuotas, la tasa de chargeback tiende a ser mayor. Un cliente que no reconoce una cuota específica puede disputarla individualmente.

#### 2.6.4 Cómo mitigar el riesgo

- **Siempre imprimir o conservar el comprobante firmado** — es la principal defensa ante un chargeback
- **Verificar la descripción del comercio** que aparece en el resumen de tarjeta del cliente (el "descriptor") — nombres confusos generan disputas evitables
- **Para fintechs:** revisar el saldo disponible antes de disponer de fondos si tenés transacciones de alto valor recientes — pueden estar bajo revisión
- **Preguntar al proveedor por el proceso de disputa antes de adherirse** — no todos lo publican claramente

---

### 2.7 Coeficientes de Cuotas — El Financiamiento Silencioso

Cuando un comercio ofrece "cuotas sin interés", alguien paga el interés. Ese alguien es el comercio — a través del coeficiente que aplica el adquirente.

#### 2.7.1 Cómo funciona el coeficiente

- El cliente paga $100.000 en 12 cuotas "sin interés"
- El adquirente (Fiserv/Prisma) liquida al comercio: $100.000 ÷ 1.5441 = **$64.766**
- El comercio absorbió **$35.234 de costo financiero** (~35%) por ofrecer cuotas

La única fuente oficial actualizada para coeficientes vigentes es: **aranceles.fiservargentina.com** (requiere acceso periódico — se actualiza cada 1–2 meses).

#### 2.7.2 Programas de cuotas activos en Argentina

| Programa | Quién financia | Quién decide el coeficiente | Actualización |
|----------|---------------|-----------------------------|---------------|
| ~~Ahora 12 / Ahora 18~~ → **Cuotas MiPyME** (desde jul. 2025) | Estado + mercado (tasa negociada) | BCRA + Fiserv/Payway | Frecuente |
| Cuota a Cuota | El comercio absorbe todo | Fiserv/Prisma | Frecuente |
| MiPyME | Estado + banco | BCRA + banco | Frecuente |
| Cencosud | Cencosud (tarjeta propia) | Cencosud | Independiente |

> ⚠️ Los coeficientes cambiaron en agosto 2025 (ver §3.10). No hay obligación legal de notificar al comercio — el comercio debe revisar el portal antes de cada período promocional.

#### 2.7.3 Referencia de coeficientes (noviembre 2025 — verificar actualización)

El único valor confirmado en el momento de elaboración de esta guía:

| Plan | Cuotas | Coeficiente | Costo implícito para el comercio |
|------|--------|-------------|----------------------------------|
| Cuota a Cuota / Ahora | 12 cuotas | **1,5441** | El comercio recibe $64,77 por cada $100 vendidos |

> 📌 La tabla completa (3, 6, 9, 12, 18, 24 cuotas × todos los programas) requiere acceso a aranceles.fiservargentina.com. Se recomienda consultarla antes de lanzar cualquier promoción de cuotas. Ver §9.2 para la descripción completa de lo que debería contener un análisis exhaustivo.

🟡 **Confianza:** Coeficiente de 12 cuotas confirmado (aranceles.fiservargentina.com, noviembre 2025). Valores para otras cantidades de cuotas y programas requieren verificación actualizada.

#### 2.7.4 Programa de Cuotas con Subsidio — Historial y Estado Actual

**Programa vigente (desde julio 2025): Cuotas MiPyME**

El Estado reemplazó los programas "Ahora" (discontinuados en enero 2024) con "Cuota Simple" (feb. 2024 – jun. 2025) y finalmente con **Cuotas MiPyME** (julio 2025–presente). Requisito: certificado MiPyME vigente (Sepyme).

| Programa | Cuotas | Tasa al comercio | El comercio recibe (por c/ $100 vendidos) |
|----------|--------|------------------|------------------------------------------|
| **Cuotas MiPyME** (vigente) | 3 cuotas | 5,93% + IVA | ~$94,07 |
| **Cuotas MiPyME** (vigente) | 6 cuotas | 11,24% + IVA | ~$88,76 |

> 📌 **Diferencia clave con §2.7.3:** El coeficiente 1.5441 (→ comercio recibe $64,77 por $100) aplica al "Cuota a Cuota" **sin subsidio estatal**. Cuotas MiPyME tiene tasa negociada con subsidio parcial del Estado — significativamente más favorable para el comercio. Verificar condiciones en **redcame.org.ar/novedades/12205**.

> 📌 **Herramienta gratuita:** CAME ofrece una calculadora que incorpora IIBB, impuestos municipales e IVA al precio de venta en cuotas: **redcame.org.ar/novedades/13344**

---

**Datos históricos de referencia (programas discontinuados)**

Los programas "Ahora 12 / 18 / 24" rigieron hasta enero 2024 con las siguientes tasas de descuento (CAME, ene. 2024 — ya no vigentes):

| Programa | Cuotas | Descuento histórico | El comercio recibía (por c/ $100) |
|----------|--------|---------------------|----------------------------------|
| ~~Ahora 12~~ | 12 cuotas | 18,18% | $81,82 |
| ~~Ahora 18~~ | 18 cuotas | 28,84% | $71,16 |
| ~~Ahora 24~~ | 24 cuotas | 35,83% | $64,17 |

🟡 **Confianza:** Tasas históricas documentadas por CAME para programas Ahora (redcame.org.ar). Tasas de Cuotas MiPyME requieren verificación actualizada en redcame.org.ar/novedades/12205.

---

### 2.8 Opacidad en la Estructura de Tasas: Lo que no Dice la Tarifa Publicada

Este es uno de los aspectos menos documentados del sistema de pagos argentino. Las tasas que publica cualquier proveedor ("0,80% + IVA", "1,80% + IVA") son **tasas compuestas** — suman internamente al menos dos centros de costo distintos, pero el comercio solo ve un número.

#### 2.8.1 La anatomía real de una tasa de comisión

Toda transacción procesada involucra al menos dos actores:

| Componente | Quién lo cobra | ¿Aparece en el contrato? | ¿Es negociable? |
|------------|---------------|--------------------------|-----------------|
| **Margen propio del banco/fintech** | El banco/fintech directamente | Solo el total | Parcialmente |
| **Fee de red / infraestructura** | Tercero (Red Link, Fiserv, red Visa/MC) | No | No |

El banco o fintech cobra la tasa total, retiene su margen, y **remite el resto al operador de red** que procesó la transacción. Este desglose no figura en ninguna tabla de tarifas publicada.

#### 2.8.2 "Comisión Cuenta y Orden de Terceros": el cargo invisible

En el sistema argentino, cuando un banco cobra una comisión "por cuenta y orden de terceros" (abreviado en los recibos como "CTA Y ORD TERCE"), está actuando como agente recaudador de otro operador. El banco **no retiene ese dinero** — lo recauda y lo transfiere.

**Para pagos QR / Transferencias 3.0:** el tercero típico es **Red Link**, la red interbancaria que opera la infraestructura de QR interoperable en Argentina (de la que son co-propietarios los propios bancos). Red Link cobra un fee de red por cada transacción enrutada; el banco lo pasa al comercio como línea separada en el comprobante.

**Para pagos con tarjeta (débito/crédito):** el tercero equivalente son las redes Fiserv/Prisma o Visa/MC. El mecanismo es el mismo — el adquirente retiene su margen y transfiere el resto a la red — pero en los comprobantes de tarjeta esta separación no siempre se presenta con igual claridad.

#### 2.8.3 Implicancias concretas para el comercio

**1. Solo el margen del banco es negociable.**
El fee de red es un costo fijo de infraestructura que el banco no puede negociar en nombre del comercio. Cuando intentás conseguir una tasa mejor, el banco tiene margen de maniobra únicamente sobre su propio componente. Si la tasa publicada es 0,80% y el fee de red es 0,20%, el banco solo puede trabajar el 0,60% restante.

**2. El IVA aplica a ambos componentes por separado.**
Matemáticamente el resultado total es el mismo (21% sobre 0,80% = 21% sobre 0,60% + 21% sobre 0,20%), pero el Responsable Inscripto que quiera usar el IVA como crédito fiscal debe asegurarse de que ambas líneas figuren en el comprobante de forma legible para la declaración.

**3. La tarifa publicada es un techo, no un margen íntegro.**
Un banco que publica "0,80% + IVA" no está diciendo que su rentabilidad es 0,80%. Parte de ese porcentaje son costos de red que el banco también paga. Esto es relevante al evaluar el poder real de negociación y al comparar proveedores cuya infraestructura es propia vs. arrendada.

**4. Las fintechs puras operan de forma distinta.**
Mercado Pago y Ualá tienen infraestructura de red propia (CVU, wallets, procesamiento interno). Sus tasas publicadas pueden ser genuinamente "todo incluido" sin un tercero de red separado, o pueden tener pass-throughs absorbidos internamente. Esta distinción requiere verificación por recibo — pendiente para futura sesión.

> 🔍 **Fuente de esta sección:** Comprobante real de POS BNA (Venta 2 - POS 26432, 23/02/2026). Ver §3.1 para el análisis completo del comprobante.

🟡 **Confianza:** Estructura verificada para BNA QR/Transferencia (feb. 2026). El principio general aplica al sector pero la distribución exacta entre componentes varía por procesador y tipo de transacción. Verificación por recibo pendiente para otros proveedores.

---

## 3. Análisis por Entidad

> **Niveles de confianza usados en esta sección:**
> - 🟢 **Verde**: Dato oficial y reciente (menos de 6 meses)
> - 🟡 **Amarillo**: Oficial pero con más de 6 meses, o sujeto a variación por inflación
> - 🔴 **Rojo**: Reportado por comunidad/prensa, no confirmado oficialmente

---

### 3.1 Banco de la Nación Argentina (BNA)

#### Costos visibles
| Transacción | Tasa | Acreditación |
|-------------|------|-------------|
| Débito | 0,80% + IVA | 24 horas hábiles |
| Crédito | 1,80% + IVA | 8–10 días hábiles |
| Tarjeta internacional | 7,50% + IVA | 10 días hábiles |
| Pagos B2B (Esquema Tradicional) | 0,70% + IVA | Variable |

#### Costos fijos
- **Terminal:** Distribuye terminales Fiserv y PayWay. **Bonificación del 100% durante 12 meses** para nuevos clientes. Luego: costo de mercado (~$37.979–$46.389 + IVA/mes).
- **Membresía BNA Conecta:** Desde $17.500 hasta $175.000/mes (segmentada por tamaño de empresa). En la práctica, **bonificada entre 20% y 90% según segmento**, quedando efectivamente en $0 para microempresas en muchos casos.
- **Cargo de gestión:** $50 por "gestión de aceptación/cobro" en operatoria tradicional (cobro de valores).

#### Condiciones y letra chica
- La bonificación de terminal requiere adhesión formal a través del portal BNA Conecta (validación CUIT/UIF/PEP).
- La solución **+Pagos Nación** permite cobrar con QR y Link de Pago sin terminal física — opción sin costo fijo, viable para kioscos y comercios pequeños.
- Los aranceles se alinean estrictamente con los topes regulatorios del BCRA.

#### Desglose real de tarifas (comprobante POS, 23/02/2026)

El comprobante de movimiento de un POS BNA real (QR dinámico / Transferencia) revela la estructura interna de la comisión del 0,80% publicada:

| Línea en el comprobante | Monto | % sobre venta | Quién recibe |
|------------------------|-------|---------------|-------------|
| Cobro (venta bruta) | $17.577,50 | 100% | — |
| COMISION | $105,46 | **0,60%** | BNA (margen propio) |
| COMISION IVA GENE 21,00% | $22,15 | 21% s/ $105,46 | ARCA |
| COMISION CTA Y ORD TERCE | $35,16 | **0,20%** | Tercero de red (Red Link) |
| COMISION CTA Y ORD TERCE IVA GENE 21,00% | $7,38 | 21% s/ $35,16 | ARCA |
| **Total acreditado** | **$17.407,35** | neto: 98,98% | Comercio |

**Lectura del comprobante:**
- La tarifa publicada es **0,80% + IVA** — pero BNA solo retiene **0,60%**. El **0,20% restante es un fee de red** que BNA recauda y transfiere a Red Link (la red interbancaria que procesa los QR de Transferencias 3.0).
- El descriptor "COMISION CTA Y ORD TERCE" significa "comisión cobrada por cuenta y orden de terceros" — BNA actúa como agente intermediario, no como beneficiario final de esa porción.
- **La tabla de tarifas de BNA no desglosa este componente.** Solo es visible en el comprobante real de cada transacción.

**Implicancias para el comercio:**
- Al negociar con BNA, el margen de reducción real está sobre el **0,60%** (margen BNA), no sobre el 0,80% total.
- El cargo de Red Link (0,20%) es un costo de infraestructura fijo — no negociable a nivel del comercio individual.
- Ver §2.8 para el análisis del patrón general en todos los procesadores.

🟢 **Confianza:** Datos obtenidos de comprobante de POS real (BNA +Pagos, 23/02/2026).

#### Evaluación por perfil de volumen
| Perfil | Recomendación |
|--------|--------------|
| Bajo ($300K–$800K) | ✅ Viable con bonificación. Sin bonif., terminal hace inviable el modelo. Evaluar +Pagos (QR, sin terminal). |
| Medio ($800K–$2,5M) | ✅ Muy conveniente con terminal bonificada. Ahorros de $30K–$60K/mes vs. fintechs. |
| Medio-alto ($2,5M–$6M) | ✅ Claramente el más económico. Prioridad absoluta. |

🟢 **Confianza:** Datos obtenidos de tabla oficial de comisiones y cargos BNA (bna.com.ar/Downloads/ComisionesYCargosComercial.pdf) y portal +Pagos Nación.

---

### 3.2 Banco de la Provincia de Buenos Aires (BAPRO / Cuenta DNI)

#### Costos visibles
| Transacción | Tasa | Acreditación |
|-------------|------|-------------|
| Clave DNI (Token) | **0,60%** | Inmediata |
| QR (Saldo en Cuenta) | 0,80% + IVA | Inmediata |
| Débito (POS/QR) | 0,80% + IVA | 24 horas hábiles |
| Crédito (POS/QR) | 1,80% + IVA | 8–18 días hábiles |
| American Express | 2,80% | Según plan de cuotas |

**⭐ La tasa de 0,60% con acreditación inmediata vía Clave DNI es la más baja del mercado argentino para transacciones digitales.**

#### Costos fijos (cuando se usa terminal POS física)
| Terminal | Costo mensual + IVA | Costo total |
|----------|--------------------|----|
| Fiserv Posnet | $37.979 + IVA | ~$45.955/mes |
| Clover (Mini/Flex) | $46.389 + IVA | ~$56.130/mes |
| PayWay (activa) | $41.999 + IVA | ~$50.819/mes |
| PayWay (inactiva) | $50.399 + IVA | ~$60.983/mes |

> ⚠️ BAPRO es transparente sobre los costos de terminal. No siempre bonifican; depende del segmento y acuerdo comercial. Verificar condiciones vigentes al momento de adhesión.

#### Condiciones y letra chica
- La tasa del 0,60% aplica **exclusivamente a pagos vía Clave DNI**. Solo disponible para clientes con cuenta en Banco Provincia.
- **Coeficientes de cuotas:** Ejemplo para 3 cuotas: coeficiente 1.1723. El comercio que ofrece 3 cuotas financia al cliente al 17,23% por encima del precio de contado.
- La inactividad de terminal PayWay tiene un costo 20% mayor ($50.399 vs. $41.999): es una penalización encubierta que impacta a comercios con demanda estacional.
- **Limitación geográfica:** Cuenta DNI y sus beneficios aplican principalmente en Provincia de Buenos Aires. Fuera de PBA, el modelo es menos diferenciado.

#### Evaluación por perfil de volumen
| Perfil | Recomendación |
|--------|--------------|
| Bajo ($300K–$800K) | ✅ Excelente si clientes usan Cuenta DNI. Sin terminal, usar QR Transferencia. |
| Medio ($800K–$2,5M) | ✅ La mejor opción en PBA. Clave DNI más crédito regular es la combinación óptima. |
| Medio-alto ($2,5M–$6M) | ✅ Altamente conveniente. El costo de terminal se diluye sobre el volumen. |

🟢 **Confianza:** Portal oficial bancoprovincia.com.ar/web/adhesion_comercios, verificado en enero 2026.

---

### 3.3 Mercado Pago

#### Costos visibles (Provincia de Buenos Aires, vigente desde ago. 2025)
| Transacción | Plazo | Comisión + IVA | Costo efectivo |
|-------------|-------|----------------|----------------|
| Débito | En el momento | 3,25% + IVA | 3,93% aprox. |
| Débito | 24 horas | 2,99% + IVA | 3,62% aprox. |
| Crédito | En el momento | 6,29% + IVA | 7,61% aprox. |
| Crédito | 5 días | 5,39% + IVA | 6,52% aprox. |
| Crédito | 10 días | 4,39% + IVA | 5,31% aprox. |
| Crédito | 18 días | 3,39% + IVA | 4,10% aprox. |
| Crédito | 35 días | 1,49% + IVA | 1,80% aprox. |

> 📌 **Nota provincial:** Las tasas aplican a comercios registrados en Provincia de Buenos Aires. Pueden variar en otras provincias. Verificar en mercadopago.com.ar/ayuda/2779.

#### Costos fijos
- **Sin abono mensual ni alquiler de terminal.** El dispositivo Point Mini y Point Pro se venden por única vez o en cuotas.
- La ausencia de costo fijo es la ventaja estructural frente a bancos para volúmenes bajos.

#### Análisis de la "Prima de Liquidez"
El comercio que elige cobrar crédito "en el momento" a 6,29%+IVA está pagando implícitamente una Tasa Efectiva Anualizada (TEA) muy elevada por adelantar 10–18 días de crédito. En cambio, esperar 35 días da una tasa del 1,49% (más baja incluso que el tope bancario del 1,8%), pero con pérdida por inflación que puede equivaler a un 2,9% adicional a ese plazo — resultando en un costo real mayor que el de 18 días.

**La opción óptima en MP, considerando inflación (2,5% mensual):**

| Plazo crédito | Comisión | Costo inflación* | Costo total efectivo |
|---------------|----------|-----------------|---------------------|
| En el momento | 6,29% + IVA | 0% | 7,61% |
| 18 días | 3,39% + IVA | 1,50% | 5,60% |
| 35 días | 1,49% + IVA | 2,92% | 4,72% |

*Por $100K vendidos con inflación mensual 2,5%

**Conclusión:** Para la mayoría de los comercios minoristas, **el plazo de 18 días es el mejor equilibrio** dentro de Mercado Pago.

#### Evaluación por perfil de volumen
| Perfil | Recomendación |
|--------|--------------|
| Bajo ($300K–$800K) | 🟡 Conveniente por ausencia de costos fijos, pero la tasa es 3–4x mayor que bancos. |
| Medio ($800K–$2,5M) | 🔴 Desventajoso vs. banco con terminal bonificada. Solo si no califica para bonificación bancaria. |
| Medio-alto ($2,5M–$6M) | 🔴 Muy costoso. Diferencia de $80K–$150K/mes vs. banco. |

🟢 **Confianza:** Datos de mercadopago.com.ar/ayuda/2779 y /ayuda/3605, actualizados agosto 2025.

---

### 3.4 Ualá (Ualá Bis)

#### Costos visibles
| Transacción | Comisión + IVA | Acreditación |
|-------------|----------------|-------------|
| Débito (mPOS) | 2,90% + IVA (~3,51%) | Inmediata |
| Crédito (mPOS) | 4,40%–4,90% + IVA (~5,32%–5,93%) | Inmediata |
| Link de Pago / E-commerce | 4,90% + IVA | Inmediata |
| QR (Transferencias 3.0) | 0,60% | Inmediata |

#### Costos fijos
- **Sin abono mensual ni alquiler de terminal.** El POS Pro se vende a precios subsidiados por única vez.
- **El mPOS tampoco tiene costo mensual.** Esto es crítico para la comparación con bancos.

#### Ventaja competitiva
Frente a Mercado Pago, Ualá Bis ofrece acreditación inmediata de crédito a **4,9% vs. 6,29%**, un ahorro de 1,39 puntos porcentuales. Para un comercio que vende $500K/mes en crédito, eso representa ~$6.950/mes de ahorro.

#### Condiciones y letra chica
- La tasa del 0,60% para QR aplica a pagos con saldo en cuenta (Transferencias 3.0), no a pagos con tarjeta. Es la misma lógica que BAPRO y otros.
- Ualá opera como **agregador**, no como adquirente directo. Esto implica que frente a disputas de cargo (chargebacks), el comercio trata con Ualá, no directamente con Visa/Mastercard.

#### Evaluación por perfil de volumen
| Perfil | Recomendación |
|--------|--------------|
| Bajo ($300K–$800K) | ✅ La mejor fintech para este perfil. Sin costo fijo, menor tasa que MP. |
| Medio ($800K–$2,5M) | 🟡 Competitivo si no hay acceso a terminal bancaria bonificada. |
| Medio-alto ($2,5M–$6M) | 🔴 La diferencia vs. banco supera $100K/mes. Evaluar migración bancaria. |

🟢 **Confianza:** ualabis.com.ar/pos-pro, verificado enero 2026.

---

### 3.5 Fiserv / Prisma (Infraestructura Adquirente)

Fiserv no es un proveedor al que un comercio accede directamente; es la **infraestructura de adquirencia** sobre la que operan BNA, BAPRO, BBVA, Macro, y PayWay. Se incluye aquí porque los costos de su ecosistema impactan directamente a los comercios.

#### Costos visibles (adquirencia directa vía banco)
| Transacción | Tasa | Acreditación |
|-------------|------|-------------|
| Débito | 0,80% + IVA | 24 horas hábiles |
| Crédito | 1,80% + IVA | 8–18 días hábiles (según categoría comercio) |

#### Costos del ecosistema Clover
- Terminal Clover Mini: ~$46.389/mes (precio publicado por BAPRO, fecha: enero 2026)
- Coeficientes cuotas plan "Ahora" / "Cuota a Cuota": coeficiente de 1.5441 para 12 cuotas (noviembre 2025) — sujeto a actualización frecuente.

#### Condiciones relevantes
- La plataforma Clover permite instalar apps de gestión (stock, fidelización), pero el comercio paga por cada app del Clover App Market.
- Los coeficientes de cuotas son actualizados periódicamente por Fiserv, sin aviso previo garantizado al comercio. El comercio debe revisar el portal antes de promocionar planes de cuotas.
- Fuente oficial de aranceles: aranceles.fiservargentina.com

🟢 **Confianza:** aranceles.fiservargentina.com y portal BAPRO, verificados enero 2026.

---

### 3.6 Getnet / Santander Argentina

Getnet es la plataforma de adquirencia del Grupo Santander para Argentina. Opera como la puerta de entrada a Fiserv para clientes del Banco Santander.

#### Costos visibles
| Transacción | Tasa | Notas |
|-------------|------|-------|
| Débito | 0,80% + IVA | Tope regulatorio BCRA |
| Crédito | 1,80% + IVA | Tope regulatorio BCRA |
| Tarjetas internacionales Visa/MC | +0,70% adicional | Sobre la tasa base; aplica a crédito y prepago |

#### Costos fijos
- Terminal GetPOS (Smart/Classic): **$37.000 + IVA/mes** (precio base post-bonificación)
- **Bonificación: 12 meses gratis** para nuevos clientes (vigente febrero 2026). Luego aplica el costo mensual.
- Servicio "Pago Inmediato": disponible; tasa subsidiada para nuevos clientes hasta marzo 2026 (hasta $2.000.000 ARS en ventas brutas/mes). Luego aplica tasa estándar.

#### Condiciones y letra chica
- Los aranceles exactos por tarifa dinámica (para cada comercio según negociación) se consultan únicamente a través del **Portal Getnet** — no están publicados de forma genérica.
- La promoción de "Pago Inmediato" tiene **tope mensual de $2.000.000 en ventas brutas**. Superado ese monto, aplica la tasa estándar para el resto del mes.
- Getnet opera como adquirente dentro del ecosistema Santander. Comercios fuera del banco Santander pueden adherirse, pero las condiciones más favorables las obtienen clientes del banco.

#### Evaluación por perfil de volumen
| Perfil | Recomendación |
|--------|--------------|
| Bajo ($300K–$800K) | ✅ Viable con bonificación. Tasa competitiva. |
| Medio ($800K–$2,5M) | ✅ Muy conveniente durante bonificación; evaluar renovación o alternativa al mes 13. |
| Medio-alto ($2,5M–$6M) | ✅ Económicamente eficiente. |

🟡 **Confianza:** Datos parciales de getnet.com.ar y santander.com.ar (febrero 2026). Tarifas exactas requieren portal Getnet. Monto de terminal sujeto a inflación.

---

### 3.7 BBVA Argentina

BBVA opera su adquirencia a través de Prisma (Fiserv) con la plataforma **Central POS** para gestión de ventas.

#### Costos visibles
| Transacción | Tasa | Notas |
|-------------|------|-------|
| Débito | 0,80% + IVA | Fijado por Ley de Tarjetas de Crédito N° 25.065 |
| Crédito | 1,80% + IVA | Fijado por Ley de Tarjetas de Crédito N° 25.065 |

#### Costos fijos
- **Terminal POS:** Bonificación durante **12 meses (Personas)** o **6 meses (Empresas)** para nuevas terminales. Monto post-bonificación: No confirmado oficialmente — estimado similar al mercado (~$37.000–$46.000 + IVA/mes).
- **Central POS:** Plataforma online para control de ventas. No se encontró información sobre costo de la plataforma.

#### Condiciones y letra chica
- Procesamiento a través de Prisma (Fiserv): las condiciones de liquidación y penalizaciones son las del ecosistema Fiserv.
- Para **empresas**, la bonificación de terminal es de solo 6 meses (vs. 12 para personas/comercios individuales). Esto impacta fuerte el análisis de costo total.
- BBVA publica sus comisiones en el marco del **Régimen de Transparencia del BCRA** (bcra.gob.ar), recurso útil para comparación oficial.

#### Evaluación por perfil de volumen
| Perfil | Recomendación |
|--------|--------------|
| Bajo ($300K–$800K) | 🟡 Viable. Confirmar si califica como "persona" (12 meses bonificación) o "empresa" (6 meses). |
| Medio ($800K–$2,5M) | ✅ Conveniente. |
| Medio-alto ($2,5M–$6M) | ✅ Conveniente. |

🟡 **Confianza:** Datos de bbva.com.ar (búsqueda febrero 2026). Monto de terminal post-bonificación no confirmado oficialmente. Verificar en sucursal.

---

### 3.8 Banco Macro

Banco Macro opera sus cobros con tarjeta a través de terminales **PayWay** (bajo la marca "Terminal PayWay Macro").

#### Costos visibles
| Transacción | Tasa | Notas |
|-------------|------|-------|
| Débito | 0,80% + IVA | Regulado BCRA |
| Crédito | 1,80% + IVA | Regulado BCRA |
| Débito en dólares | Igual que débito en pesos | BCRA habilitó pagos en USD desde ene. 2025 |

#### Costos fijos
- **Terminal PayWay Macro:** Costo mensual no confirmado oficialmente. Asumir similar al mercado PayWay: $41.999 (activa) o $50.399 (inactiva) + IVA.
- Macro publica un "Tarifario Completo" en macro.com.ar — se recomienda consultar directamente.

#### Condiciones
- Macro tiene presencia fuerte en el interior del país (NOA, NEA, Cuyo). Para comercios en esas regiones, puede ser el banco más conveniente por proximidad y relación comercial establecida.

🔴 **Confianza:** Tasas de transacción asumidas por regulación BCRA (correcto). Costos de terminal no confirmados en fuente oficial. Datos de búsqueda web febrero 2026. **Verificar en sucursal antes de tomar decisiones.**

---

### 3.9 Naranja X

Naranja X es la evolución digital de Tarjeta Naranja (Grupo Financiero Galicia). Opera como emisor de su propia tarjeta y, a través de alianzas, permite a los comercios recibir pagos.

#### Costos visibles
| Transacción | Tasa | Notas |
|-------------|------|-------|
| Crédito (tarjeta Naranja X) | 1,80% + IVA | Tope regulatorio |
| Débito / otras redes | No confirmado — ver portal | — |

#### Costos fijos
- **Primeros 3 meses: 0% de comisión** (promoción activa, verificar vigencia)
- **Cobro Tap:** solución NFC para cobrar con el celular, sin terminal física. Costo mensual no publicado.
- Detalle completo en: naranjax.com/costos-comisiones-y-limites

#### Condiciones y letra chica
- Naranja X tiene una base de usuarios propia muy importante en el interior del país (especialmente Córdoba y Cuyo). Para comercios en esas zonas, adherirse puede capturar clientes que pagan exclusivamente con Naranja.
- La integración de cobros puede hacerse sin terminal física (Cobro Tap, Link de Pago). Esto elimina el costo fijo de alquiler.

🟡 **Confianza:** Tasa de crédito confirmada (regulatorio). Datos de naranjax.com (búsqueda febrero 2026). Confirmación de tasa débito y costos adicionales requiere consultar el portal oficial.

---

### 3.10 PayWay (Red Prisma / Fiserv)

PayWay es el brazo comercial de la red Prisma (Fiserv) para la venta directa a comercios de terminales y servicios de adquirencia.

#### Costos visibles
| Transacción | Tasa | Acreditación |
|-------------|------|-------------|
| Débito | 0,80% + IVA | 24 horas hábiles |
| Crédito | 1,80% + IVA | 10–18 días hábiles |
| American Express | Hasta 2,90% | Variable |
| Débito en cuenta | 0,80% + IVA | Variable |

#### Plazos de acreditación (por categoría de comercio)
| Categoría | Opciones disponibles |
|-----------|---------------------|
| Micro/Pequeño | 24 horas, 10 días hábiles, 18 días hábiles |
| Mediano/Grande | 1 día hábil, 8 días hábiles, 18 días hábiles |

#### Costos fijos de terminal
| Estado de terminal | Costo mensual + IVA | Total aprox. |
|-------------------|--------------------|----|
| Activa | $41.999 + IVA | ~$50.819/mes |
| Inactiva | $50.399 + IVA | ~$60.983/mes |

> ⚠️ **El castigo por inactividad** ($8.400/mes extra) es una penalización que afecta a comercios con temporada baja o cierre temporal. Es una "trampa" contractual frecuente.

#### Criterio de inactividad — lo que no está publicado

PayWay no publica en su portal público la definición exacta de qué hace que una terminal sea clasificada como "inactiva". Lo que se sabe y lo que no:

| Aspecto | Estado |
|---------|--------|
| Costo de terminal inactiva ($50.399/mes) | 🟢 Confirmado (portal PayWay) |
| Definición de "inactividad" (umbral de transacciones) | 🔴 **No publicado** — requiere consulta directa a PayWay |
| Período de gracia antes de aplicar el cargo mayor | 🔴 **No confirmado** |
| Posibilidad de pausar el contrato temporalmente | 🔴 **No confirmado** |
| Penalización por devolver terminal antes de fin de contrato | 🔴 **No confirmado** — presumiblemente sin penalización, pero verificar |

> ⚠️ **Antes de firmar con PayWay:** Preguntar explícitamente: "¿Cuántas transacciones mínimas necesito por mes para que la terminal se considere activa?" y obtenerlo por escrito. Esto es especialmente crítico para comercios con temporada baja (turismo, kioscos escolares, eventos).

#### Actualización importante (agosto 2025)
A partir del 13 de agosto de 2025, cambiaron las tasas y coeficientes para cuotas MiPyME, Cencosud y Cuotas PayWay. Los comercios que ofrecen planes de cuotas deben **actualizar periódicamente los coeficientes** en sus sistemas de caja.

🟢 **Confianza:** payway.com.ar/planes-precios y ayuda.payway.com.ar/cobros/plazos-acreditacion-y-comisiones, verificados febrero 2026.

---

### 3.11 Modo

Modo es la billetera digital interbancos, operada por un consorcio de los principales bancos argentinos (Santander, BBVA, Macro, Galicia, entre otros).

#### Costos visibles para comercios
- Los pagos con Modo se procesan como transferencias bancarias (Transferencias 3.0). La tasa aplicable al comercio es la de **QR/transferencia inmediata: 0,80% + IVA** (máximo regulatorio para débito/transferencia).
- Algunos bancos aplican tasas menores para pagos Modo de clientes propios.

#### Condiciones
- La adhesión como comercio para aceptar Modo requiere una cuenta bancaria en alguno de los bancos participantes.
- El número de usuarios activos de Modo ha crecido significativamente en 2025, especialmente en segmentos de mayor poder adquisitivo.

🔴 **Confianza:** Tasas inferidas por regulación de Transferencias 3.0. No se encontró página oficial de tarifas para comercios (modo.com.ar). **Se recomienda consultar con el banco de preferencia antes de adhesión.**

---

## 4. Comparación Transversal

### 4.1 Metodología

Los cálculos a continuación usan los siguientes supuestos:
- **Mix de pagos:** 60% débito / 40% crédito (aproximación para comercio minorista general)
- **Inflación mensual de referencia:** 2,5% (verificar en INDEC al momento de consulta)
- **Plazo de crédito:** 10 días hábiles (~14 días calendario) para bancos; inmediato para fintechs
- **IVA sobre comisiones:** 21%
- **Terminal bancaria:** Fiserv Posnet a $45.955/mes (con IVA) — mostrado como costo separado
- Para la versión "con bonificación": costo de terminal = $0 (primeros 12 meses)

### 4.2 Tabla de Costo Estimado Total Mensual

#### Perfil A: Kiosco ($500.000 ARS/mes — 60% débito: $300K / 40% crédito: $200K)

| Proveedor | Comisión débito | Comisión crédito | Costo fijo/mes | Costo inflación crédito | **Total estimado** |
|-----------|----------------|-----------------|----------------|------------------------|-------------------|
| BNA / BAPRO / Getnet / PayWay (bonificado) | $2.904 | $4.356 | $0 | $2.333 | **$9.593** |
| BAPRO Clave DNI (70% Clave DNI, 30% crédito) | $2.100* | $2.178 | $0 | $1.400 | **$5.678** |
| Naranja X / Modo / BBVA (bonificado) | ~$2.904 | ~$4.356 | $0 | $2.333 | **~$9.593** |
| BNA / BAPRO / PayWay (sin bonificación) | $2.904 | $4.356 | $45.955 | $2.333 | **$55.548** |
| Ualá (inmediato) | $10.527 | $11.858 | $0 | $0 | **$22.385** |
| Mercado Pago (18 días crédito, 24h débito) | $10.854 | $8.166 | $0 | $1.400 | **$20.420** |
| Mercado Pago (inmediato) | $13.763 | $15.222 | $0 | $0 | **$28.985** |

*Clave DNI asume 70% de las ventas en débito capturadas por clientes del banco.

> 📌 **Conclusión Perfil A:** Con bonificación bancaria, los bancos son 2,3 veces más baratos que Ualá y 3x más que MP. Sin bonificación, las fintechs ganan por amplio margen. BAPRO Clave DNI es la opción más económica posible para comercios en PBA con base de clientes del banco.

---

#### Perfil B: Almacén ($1.500.000 ARS/mes — 60% débito: $900K / 40% crédito: $600K)

| Proveedor | Comisión débito | Comisión crédito | Costo fijo/mes | Costo inflación crédito | **Total estimado** |
|-----------|----------------|-----------------|----------------|------------------------|-------------------|
| BNA / Getnet / PayWay (bonificado) | $8.712 | $13.068 | $0 | $7.000 | **$28.780** |
| BAPRO Clave DNI | $6.300* | $6.534 | $0 | $4.200 | **$17.034** |
| BNA / PayWay (sin bonificación) | $8.712 | $13.068 | $45.955 | $7.000 | **$74.735** |
| BBVA (sin bonificación, empresa, 6 meses) | $8.712 | $13.068 | $45.955 | $7.000 | **$74.735** |
| Ualá (inmediato) | $31.611 | $35.574 | $0 | $0 | **$67.185** |
| Mercado Pago (18 días crédito) | $32.562 | $24.498 | $0 | $4.200 | **$61.260** |
| Mercado Pago (inmediato) | $41.290 | $45.694 | $0 | $0 | **$86.984** |

> 📌 **Conclusión Perfil B:** BNA/Getnet con bonificación es claramente superior ($28.780 vs. $61.260 mínimo de fintechs). La opción BAPRO Clave DNI es aún más económica pero requiere base de clientes del banco. Sin bonificación bancaria, Mercado Pago a 18 días es marginalmente preferible a Ualá en este perfil.

---

#### Perfil C: Ferretería ($4.000.000 ARS/mes — 50% débito: $2M / 50% crédito: $2M)

| Proveedor | Comisión débito | Comisión crédito | Costo fijo/mes | Costo inflación crédito | **Total estimado** |
|-----------|----------------|-----------------|----------------|------------------------|-------------------|
| BNA / Getnet / PayWay (bonificado) | $19.360 | $43.560 | $0 | $23.333 | **$86.253** |
| BAPRO Clave DNI | $12.000* | $21.780 | $0 | $14.000 | **$47.780** |
| BNA / PayWay (sin bonificación) | $19.360 | $43.560 | $45.955 | $23.333 | **$132.208** |
| Ualá (inmediato) | $70.180 | $118.580 | $0 | $0 | **$188.760** |
| Mercado Pago (18 días) | $87.450 | $82.060 | $0 | $14.000 | **$183.510** |
| Mercado Pago (inmediato) | $78.650 | $152.318 | $0 | $0 | **$230.968** |

> 📌 **Conclusión Perfil C:** La diferencia entre la mejor opción bancaria y las fintechs es **$100.000–$145.000 por mes**. En términos anuales: $1.2M–$1.7M ARS de ahorro. Un comercio de este volumen **no debería usar Mercado Pago o Ualá como solución principal**.

---

### 4.3 Punto de Equilibrio: ¿Cuándo conviene pagar el alquiler de terminal?

La pregunta más práctica: ¿a qué volumen de ventas el ahorro en comisiones bancarias cubre el costo de alquiler mensual de la terminal?

**Comparando banco (1,8% crédito) vs. Ualá (4,9% crédito), para ventas de crédito:**

```
Ahorro por punto porcentual = (4,9% - 1,8%) × 1,21 (IVA) = 3,751% sobre ventas de crédito
Terminal mensual = $45.955
Volumen de crédito para breakeven = $45.955 / 3,751% = $1.225.000 ARS/mes en crédito
```

Si el 40% de tus ventas son con crédito: `$1.225.000 / 40% = $3.062.000 ARS/mes en ventas totales`

**Comparando banco vs. Mercado Pago (inmediato):**

```
Ahorro = (6,29% - 1,8%) × 1,21 = 5,433%
Volumen de crédito para breakeven = $45.955 / 5,433% = $846.000 ARS/mes en crédito
Con 40% de ventas en crédito: $846.000 / 40% = $2.115.000 ARS/mes en ventas totales
```

| Si tus ventas mensuales son... | Respecto a Ualá | Respecto a MP inmediato |
|-------------------------------|-----------------|------------------------|
| Menos de $2,1M | Terminal NO conviene (si la pagás vos) | Terminal NO conviene |
| $2,1M – $3M | Terminal conviene vs. MP; evaluar vs. Ualá | ✅ Terminal conviene |
| Más de $3M | ✅ Terminal conviene en todos los casos | ✅ Claramente conviene |

### 4.4 El Ciclo de Vida de la Bonificación — Qué Pasa en el Mes 13

#### 4.4.1 El problema documentado: nadie avisa

La bonificación de terminal de 12 meses es el hallazgo más impactante de esta guía — pero tiene una trampa documentada:

- Las condiciones de renovación post-bonificación **no están publicadas por ningún banco** (ver §7)
- El costo de terminal reaparece como débito automático en la cuenta del comercio desde el mes 13, sin notificación proactiva garantizada
- Este efecto convierte un negocio conveniente en uno costoso de forma silenciosa

#### 4.4.2 Opciones disponibles en el mes 13

| Opción | Descripción | Costo estimado | Factibilidad |
|--------|-------------|----------------|--------------|
| A) Renegociar con el mismo banco | Solicitar extensión de bonificación antes del mes 12 | $0 si se otorga | 🟡 Posible para clientes con buen historial de uso |
| B) Migrar a otro banco (nueva bonificación) | Cerrar en banco A, abrir en banco B — 12 meses nuevos | Costo de apertura y tiempo (~2–4 semanas) | ✅ Estrategia válida; los bancos la conocen pero no la prohíben formalmente |
| C) Pagar el alquiler sin negociar | Continuar con el costo de mercado | $37.979–$56.130 + IVA/mes | ❌ Solo conveniente si el volumen es >$3M/mes (ver §4.3) |
| D) Devolver terminal y migrar a QR/fintech | Cancelar contrato de POS, usar QR o mPOS | $0 fijo, tasa variable sube | 🟡 Según volumen (ver §4.3 punto de equilibrio) |

#### 4.4.3 Switching costs reales

- **Terminación anticipada de contrato:** Generalmente no hay penalización por devolver la terminal antes del mes 12. Verificar en el contrato individual.
- **Tiempo de adhesión a nuevo banco:** 2–4 semanas entre apertura de cuenta, validación CUIT/UIF, y entrega de terminal.
- **Riesgo operativo:** Período sin terminal durante la transición. Mitigar con mPOS de fintech temporario (Ualá o Mercado Pago).
- **Restricción de re-adhesión:** No confirmado oficialmente que los bancos restrinjan re-adhesión por CUIT, pero es un riesgo reputacional a considerar.

#### 4.4.4 Sistema de gestión recomendado (calendario)

```
Mes 1:    Adhesión. Registrar fecha de fin de bonificación.
Mes 10:   Primera revisión. Consultar con el banco si renuevan.
Mes 11:   Si no hay renovación, iniciar trámite en banco alternativo.
Mes 12:   Nueva adhesión activa. Devolver terminal anterior.
Mes 13+:  Sin costo de terminal (nuevo ciclo de bonificación iniciado).
```

> 📌 **Regla práctica:** Tratar la bonificación como una suscripción con fecha de vencimiento. Programar un recordatorio en el mes 10 es la acción de mayor retorno por unidad de tiempo para un comercio mediano.

---

### 4.5 Sensibilidad del Modelo — Qué Pasa Si Cambian los Supuestos

Los cálculos de §4.2 usan supuestos fijos (2,5% inflación, 60/40 mix débito/crédito). Esta sección explora cómo cambian los resultados cuando esos supuestos varían.

#### 4.5.1 Sensibilidad a la inflación mensual

El "arancel invisible" de esperar días para cobrar depende directamente de la inflación. A mayor inflación, mayor es el costo real de los plazos de acreditación bancaria.

| Inflación mensual | Costo de esperar 10 días hábiles (~14 días) por $1M en crédito | Impacto en la ventaja banco vs. Ualá inmediato |
|------------------|-----------------------------------------------------------------|------------------------------------------------|
| 1,0% | ~$4.667 | Se reduce: banco cuesta ~0,8% real adicional (tasa efectiva total ~2,6%) |
| 2,5% *(referencia)* | ~$11.667 | Banco cuesta ~1,2% real adicional (tasa efectiva total ~3,0%) |
| 4,0% | ~$18.667 | Banco cuesta ~1,9% real adicional (tasa efectiva total ~3,7%) — ventaja sobre fintech se achica significativamente |

> 💡 **Punto de inflexión:** Con inflación menor al 1% mensual, la ventaja de la acreditación inmediata pierde ~70% de su valor — los bancos se vuelven convenientes para comercios de menor volumen. Con inflación mayor al 4%, el arancel invisible de esperar 10 días hábiles supera el 1,7%, elevando el costo real bancario de crédito a ~3,7%–4,0%. En ese escenario, incorporando el costo inflacionario al cálculo de §4.3, el punto de equilibrio con Ualá **sube** de ~$3,5M (a 1% inflación) a ~$6M (a 4% inflación): cuanto mayor es la inflación, más volumen necesita un comercio para justificar pagar el alquiler de terminal.

#### 4.5.2 Sensibilidad al mix de pagos (débito/crédito)

Para un comercio de $1.500.000/mes (Perfil B), el impacto del mix de pagos en el costo total:

| Mix pagos | Bancos (bonificado) | Ualá | MP 18 días | Mejor opción |
|-----------|---------------------|------|------------|--------------|
| 80% débito / 20% crédito | ~$21.650 | ~$59.900 | ~$57.800 | Banco (2,8× mejor) |
| 60% débito / 40% crédito *(referencia)* | ~$28.780 | ~$67.185 | ~$61.260 | Banco (2,3× mejor) |
| 40% débito / 60% crédito | ~$35.910 | ~$74.400 | ~$64.900 | Banco (2,1× mejor) |
| 20% débito / 80% crédito | ~$43.040 | ~$81.675 | ~$68.450 | Banco (1,9× mejor) |

> 💡 **Insight:** La ventaja bancaria se mantiene en todos los mixes posibles, pero es proporcionalmente mayor cuando el negocio es débito-intensivo (kiosco, almacén). Esto se debe a que el diferencial de tasa en débito es más pronunciado en puntos porcentuales: banco 0,80% vs. Ualá 2,90% = 2,10 pp de diferencia.

#### 4.5.3 Sensibilidad al crecimiento de pagos QR

Si los pagos QR (tasa 0,6%) crecen como proporción del total de ventas:

| % ventas vía QR | Costo efectivo ponderado (banco) | Costo efectivo (Ualá, QR también 0,6%) | Diferencia banco vs. Ualá |
|----------------|----------------------------------|----------------------------------------|--------------------------|
| 10% (hoy) | ~1,7% efectivo promedio | ~4,4% efectivo promedio | Banco 2,7pp mejor |
| 30% | ~1,4% efectivo promedio | ~3,3% efectivo promedio | Banco 1,9pp mejor |
| 50% | ~1,2% efectivo promedio | ~2,7% efectivo promedio | Banco 1,5pp mejor |

> 💡 **Insight:** A mayor penetración de QR, el costo promedio ponderado baja para todos los proveedores — porque la tasa QR (0,6%) es la misma para todos. Si QR llega a representar el 50% de las ventas, la diferencia entre banco y fintech se reduce al punto donde el análisis de volumen cambia: el breakeven baja, y los fintechs se vuelven más competitivos incluso a volúmenes medios.

---

## 5. Escenarios de Impacto

### Perfil A: Don Norberto, kiosco de barrio

**Contexto:** Kiosco en zona residencial del conurbano bonaerense. Vende bebidas, snacks, cigarrillos, tarjetas de celular. Factura aproximadamente $500.000 ARS/mes. Transacciones promedio: 80 ventas/mes, ticket promedio $6.250. No tiene empleados. Cliente mayoritario: vecinos con tarjeta de débito (70% débito, 30% crédito).

**Situación actual:** Usa Mercado Pago Point Mini para no complicarse con bancos. Cobra inmediato en todo. Costo estimado: ~$28.985/mes en comisiones.

**Opciones:**

| Opción | Costo est. mensual | Diferencia vs. MP actual | Consideraciones |
|--------|-------------------|--------------------------|-----------------|
| Continuar con MP (inmediato) | $28.985 | — | Ninguna gestión adicional |
| Migrar a Ualá | $22.385 | Ahorra $6.600/mes | Mismo esquema, menor tasa |
| +Pagos BNA (QR, sin terminal) | ~$9.593 | Ahorra $19.392/mes | Requiere apertura cuenta BNA, espera 10d en crédito |
| BAPRO Cuenta DNI | ~$5.678 | Ahorra $23.307/mes | Solo si clientes son usuarios de Banco Provincia |

**Recomendación:** Migrar a **Ualá** es el primer paso sin fricción ($6.600/mes de ahorro). Si Don Norberto puede abrir cuenta en BNA y sus clientes aceptan esperar que él no les cobre "extra" por la demora, **+Pagos BNA** le ahorra casi $20.000/mes — equivalente a 2 cajas de cerveza por semana en rentabilidad adicional.

---

### Perfil B: Almacén "La Esperanza"

**Contexto:** Almacén familiar en ciudad del interior. Atiende familias del barrio. Factura ~$1.500.000 ARS/mes, ~150 transacciones/mes (ticket promedio $10.000). Mix: 60% débito, 40% crédito. Tiene una terminal POS hace 2 años (ya pasó el período de bonificación).

**Situación actual:** Opera con PayWay contratado directamente. Terminal activa a $50.819/mes (con IVA). Comisiones: +$21.780. Total estimado: ~$72.599/mes.

**Opciones:**

| Opción | Costo est. mensual | Diferencia | Consideraciones |
|--------|-------------------|------------|-----------------|
| Situación actual (PayWay sin bonif.) | $72.599 | — | Sin gestión |
| Negociar terminal en BNA (nueva bonificación 12 meses) | $28.780 | Ahorra $43.819/mes | Requiere apertura/migración a BNA; bonificación temporal |
| Getnet/Santander (nuevo cliente, bonificación 12 meses) | ~$28.780 | Ahorra $43.819/mes | Requiere apertura cuenta Santander |
| Ualá (migrar de POS a mPOS) | $67.185 | Ahorra $5.414/mes | Sin terminal fija; puede ser limitante en volumen |

**Recomendación:** La acción de mayor impacto es **gestionar una bonificación nueva en BNA o Santander**. Muchos bancos renuevan bonificaciones si el comercio cierra y reabre la cuenta, o si migra de proveedor. El ahorro de $43.819/mes recupera la inversión de tiempo en 1 día de ventas.

⚠️ **Atención en el mes 13:** Programar una revisión 11 meses después de la nueva adhesión para evitar que el costo de la terminal reaparezca sin avisar.

---

### Perfil C: Ferretería "El Tornillo"

**Contexto:** Ferretería mediana, barrio industrial. Vende materiales de construcción, herramientas. Factura ~$4.000.000 ARS/mes, ~300 transacciones/mes (ticket promedio $13.333). Mix: 50% débito, 50% crédito. Ofrece cuotas en muchas ventas. Tiene 2 terminales.

**Situación actual:** Opera con 2 terminales Clover de BAPRO. Una activa ($56.130/mes), una inactiva ($60.983/mes). Comisiones: ~$62.920. Total: ~$180.033/mes.

**Opciones:**

| Opción | Costo est. mensual | Diferencia | Consideraciones |
|--------|-------------------|------------|-----------------|
| Situación actual (2 Clover BAPRO) | $180.033 | — | |
| BNA: 1 terminal bonificada | $86.253 | Ahorra $93.780/mes | Negociar bonificación |
| BNA: 2 terminales (1 bonif. + 1 $45.955) | $132.208 | Ahorra $47.825/mes | Más operativa |
| BAPRO + Clave DNI agresivo | ~$47.780 + $56.130 = ~$103.910 | Ahorra $76.123/mes | Optimizar mix de pago |
| Devolver terminal inactiva | $180.033 − $60.983 = $119.050 | Ahorra $60.983/mes | Acción inmediata, sin fricción |

**Recomendaciones para Ferretería:**

1. **Acción inmediata:** Devolver o cancelar la terminal inactiva. Ahorro: $60.983/mes sin ningún otro cambio.
2. **Corto plazo:** Solicitar bonificación de terminal nueva en BNA. Ahorro adicional de ~$30.000/mes.
3. **Estrategia de cuotas:** Revisar los coeficientes de los planes "Ahora" frecuentemente. Para una ferretería, las ventas en cuotas son frecuentes — un coeficiente de 1.54 en 12 cuotas significa que el cliente paga 54% más; si el comercio absorbe ese costo, es un enorme drenaje.

---

## 6. Notas de Confianza y Calidad de Fuentes

### 6.1 Datos con alta confianza (🟢 Verde)

| Dato | Fuente | Fecha |
|------|--------|-------|
| Topes arancelarios BCRA: 1,8% crédito / 0,8% débito | BCRA Comunicación B 13096/2025 | 2025 |
| Tarifas BNA: 0,8% / 1,8% / 7,5% internacional | BNA ComisionesYCargosComercial.pdf | Verificado ene. 2026 |
| Membresías BNA Conecta: $17.500–$175.000 | BNA portal oficial | Verificado ene. 2026 |
| Tarifas BAPRO: completa (Clave DNI / QR / crédito) | bancoprovincia.com.ar/web/adhesion_comercios | Verificado ene. 2026 |
| Terminales BAPRO: Posnet $37.979, Clover $46.389 | Portal BAPRO | Verificado ene. 2026 |
| PayWay: activa $41.999 / inactiva $50.399 | Portal BAPRO, investigación interna | Verificado ene. 2026 |
| Mercado Pago: matriz completa de plazos/tasas (PBA) | mercadopago.com.ar/ayuda/2779 | Actualizado ago. 2025 |
| Ualá: débito 2,9%, crédito 4,4%–4,9%, QR 0,6% | ualabis.com.ar/pos-pro | Verificado ene. 2026 |
| Fiserv: 0,8% / 1,8%, coef. cuotas 1.5441 | aranceles.fiservargentina.com | Nov. 2025 |
| PayWay: débito 0,8%, crédito 1,8%, Amex 2,9% | payway.com.ar/planes-precios | Feb. 2026 |
| Getnet: terminal $37.000 + IVA, bonif. 12 meses | getnet.com.ar | Feb. 2026 |
| Getnet: 0,7% adicional tarjetas internacionales Visa/MC | getnet.com.ar/comisiones-por-ventas | Feb. 2026 |

### 6.2 Datos con confianza media (🟡 Amarillo)

| Dato | Observación |
|------|-------------|
| Montos de terminales BNA/BAPRO/Getnet en ARS | Sujetos a inflación. Verificar antes de firmar contrato. |
| Membresías BNA Conecta | Verificar vigencia de bonificaciones por segmento. |
| Coeficientes de cuotas | Se actualizan frecuentemente (último cambio conocido: ago. 2025). |
| BBVA: terminal 12 meses personas / 6 meses empresas | Dato de búsqueda web; confirmar en sucursal. |
| Naranja X: 1,8% crédito | Confirmado por regulación; otros aranceles requieren portal. |

### 6.3 Datos no confirmados (🔴 Rojo)

| Dato | Estado |
|------|--------|
| Banco Macro: costo mensual de terminal | No encontrado en fuente oficial. Asumir similar a PayWay. |
| BBVA: monto exacto del alquiler post-bonificación | No publicado. Consultar en sucursal. |
| Modo: tarifa exacta para comercios | No se encontró página de tarifas oficial. Inferido de regulación Transferencias 3.0. |
| Naranja X: tasa de débito exacta, cargo mensual | Requiere consulta en naranjax.com/costos-comisiones-y-limites |
| Santander: tarifas individualizadas por portal | Opacas; se consultan caso por caso. |

---

## 7. Preguntas Abiertas e Investigación Pendiente

### 7.1 Qué no se pudo confirmar

| Entidad | Dato faltante | Por qué |
|---------|--------------|---------|
| Banco Macro | Costo de terminal y condiciones de bonificación | Sitio web no publica tarifas; requiere contacto directo |
| BBVA | Monto exacto de alquiler de terminal post-bonificación | No publicado públicamente |
| Modo | Tarifas para comercios, condiciones de adhesión | No se encontró sección específica en modo.com.ar |
| Naranja X | Tasa de débito, costos de Cobro Tap, condiciones de cuotas para tarjeta Naranja | Portal requiere registro para ver detalle completo |
| Getnet/Santander | Tarifas dinámicas individualizadas | Disponibles solo vía Portal Getnet (requiere acceso comercial) |
| Todos los bancos | Condiciones de renovación post-bonificación de terminal | No publicadas; son condiciones comerciales individuales |

> 📌 **Actualización:** Los costos fiscales (IVA, SIRCREB, IIBB, Impuesto al Débito y Crédito Bancario) fueron documentados parcialmente en §2.5. Las tasas exactas de SIRCREB por código de actividad y los regímenes de IIBB para provincias fuera de PBA siguen siendo preguntas abiertas — ver §8.3 para la versión priorizada de estas preguntas.

### 7.2 Variables que pueden cambiar el análisis

1. **Inflación:** Si la inflación baja sostenidamente por debajo del 1% mensual, el costo de esperar días para cobrar se vuelve despreciable y las fintechs pierden aún más ventaja sobre los bancos.

2. **Bimonetarismo:** Desde febrero 2025, los comercios pueden cobrar en dólares con tarjeta de débito. Para ferreterías y negocios que venden insumos dolarizados, las tarifas en USD pueden cambiar la lógica del proveedor elegido.

3. **Transferencias 3.0 y QR interoperable:** El ecosistema de pagos con QR sigue expandiéndose. Si los pagos con QR (a tasa del 0,6%–0,8%) capturan una proporción mayor de las ventas, el costo total de cualquier proveedor cae significativamente — favoreciendo a quienes ya operan en este canal (BAPRO, BNA +Pagos, Ualá QR).

4. **IIBB sobre billeteras digitales (PBA):** La retención automática de Ingresos Brutos sobre acreditaciones en billeteras (desde oct. 2025 en PBA) suma un costo para comercios inscriptos que no se refleja en las tablas de tasas de cada proveedor.

5. **Planes "Ahora" y financiamiento de cuotas:** Los coeficientes se actualizan en función de la tasa de política monetaria del BCRA. Cualquier cambio en la política del banco central impacta directamente el costo de ofrecer cuotas.

### 7.3 Cómo mantener esta guía actualizada

- **Revisión recomendada:** Semestral
- **Datos a verificar primero:** Montos de alquiler de terminal (los más sensibles a la inflación), coeficientes de cuotas (los más volátiles), condiciones de bonificación vigentes
- **Fuentes primarias clave:**
  - BCRA Régimen de Transparencia: bcra.gob.ar/BCRAyVos/Financiamiento_personas_fisicas.asp
  - Fiserv aranceles: aranceles.fiservargentina.com
  - PayWay: ayuda.payway.com.ar/cobros/plazos-acreditacion-y-comisiones
  - Mercado Pago: mercadopago.com.ar/ayuda/2779
  - Ualá: ualabis.com.ar/pos-pro

---

## 8. Notas para el Desarrollo de Producto

Esta sección es un insumo directo para el PRD de la herramienta de monitoreo de comisiones.

### 8.1 Clasificación de Volatilidad de Datos

Guía para priorizar qué datos scrapeary con qué frecuencia actualizar:

| Tipo de dato | Volatilidad | Frecuencia de cambio esperada | Prioridad de monitoreo |
|-------------|-------------|------------------------------|----------------------|
| Montos de alquiler de terminal (ARS) | Muy alta | Mensual (indexado a inflación) | 🔴 Crítica — actualizar mensualmente |
| Coeficientes de cuotas (Ahora, MiPyME) | Alta | Cada 1–2 meses | 🔴 Crítica |
| Tasas de comisión (crédito/débito %) | Baja | Cambios regulatorios infrecuentes | 🟡 Trimestral (6 meses = límite de confianza del documento) |
| Condiciones de bonificación | Media-baja | Discrecionales por banco, sin aviso | 🟡 Trimestral |
| Plazos de acreditación | Baja | Muy estables | 🟢 Anual |
| Tasas IIBB por provincia | Media | Cambios presupuestarios anuales | 🟡 Semestral |
| Referencia de inflación (INDEC) | Muy alta | Mensual | 🔴 Mensual |

### 8.2 Árbol de Decisión del Comerciante

```
¿Cuánto facturás por mes con tarjeta?
│
├── Menos de $800.000/mes
│   └── ¿Tenés acceso a bonificación bancaria? (nuevo cliente banco)
│       ├── SÍ → Ir a banco con bonificación (ahorrás $30K–$50K/mes vs. fintech)
│       └── NO → ¿Necesitás el dinero hoy?
│           ├── SÍ → Ualá (mejor tasa inmediata)
│           └── NO → Mercado Pago 18 días (equilibrio tasa-liquidez)
│
├── $800.000 – $3.000.000/mes
│   └── ¿Estás en Provincia de Buenos Aires?
│       ├── SÍ → ¿Tus clientes usan Cuenta DNI?
│       │   ├── SÍ (>30%) → BAPRO Clave DNI es la mejor opción
│       │   └── NO → BNA o Getnet/Santander con bonificación
│       └── NO → BNA o banco con presencia regional + bonificación
│
└── Más de $3.000.000/mes
    └── Banco con terminal (bonificada o no — igual conviene)
        └── Considerar devolver terminal inactiva si hay estacionalidad
```

> ⚠️ Nota: el umbral de $800.000/mes es una referencia de perfil de volumen, no el punto de equilibrio calculado en §4.3 ($2,1M vs. MP / $3,06M vs. Ualá). La variable decisiva en todos los casos es el **acceso a bonificación bancaria**, no el volumen absoluto.

### 8.3 Preguntas Pendientes Priorizadas para el PRD

Preguntas abiertas ordenadas por impacto en el producto:

| Prioridad | Pregunta | Por qué importa para el producto | Cómo responderla |
|-----------|----------|----------------------------------|------------------|
| P1 | ¿Qué % de comercios renueva bonificación al mes 13 con el mismo banco? | Define si el consejo principal del documento es escalable | Entrevistas con comerciantes o contacto directo con bancos |
| P2 | ¿Cuáles son las tasas exactas de SIRCREB por código de actividad? | Permite calcular costo total real por sector | Consulta ARCA, contador impositivo |
| P3 | ¿Cuáles son las tasas de IIBB para comercio minorista en Córdoba, Santa Fe, Mendoza? | Necesario para versión nacional de la herramienta | Consulta AGIP, ARBA, DGR Córdoba |
| P4 | ¿Tiene Naranja X tasa de débito y costo de Cobro Tap publicados? | Completa el análisis de entidades | Consulta naranjax.com con registro |
| P5 | ¿Cuáles son las condiciones contractuales de terminación anticipada de terminal? | Permite modelar switching costs reales | Revisión de contratos tipo de cada banco |

---

## 9. Desarrollo Futuro (Nice-to-Haves)

Temas excluidos del alcance actual de esta guía, pero de alto valor para versiones futuras.

### 9.1 Nuevas entidades a incorporar

| Entidad | Relevancia |
|---------|-----------|
| Banco Galicia / Galicia Más | Uno de los mayores bancos privados del país; tiene oferta activa para comercios (Galicia Más) con tasas no publicadas genéricamente |
| Banco Ciudad de Buenos Aires | Relevante para comercios en CABA; opera a través de Prisma/Fiserv |
| Bind (Bank for Innovation and Development) | Banco digital con propuesta diferenciada para pymes; tasas y condiciones a investigar |
| Personal Pay (Telecom) | Billetera digital con base de usuarios en crecimiento; aún sin tarifa pública para comercios |

### 9.2 Análisis de cuotas en profundidad

El análisis completo de coeficientes fue incorporado en **§2.7**. Pendiente: tabla exhaustiva de todos los programas (3/6/9/12/18/24 cuotas × Ahora/Cuota a Cuota/MiPyME/Cencosud) con valores actualizados desde aranceles.fiservargentina.com.

### 9.3 Contrafactual: efectivo vs. tarjeta

El análisis de esta guía asume que la alternativa al cobro electrónico es no tener ingresos. La realidad es que el efectivo también tiene costos:
- Transporte de valores y seguridad
- Depósito bancario (comisiones)
- Tiempo de conteo y conciliación
- Riesgo de robo y falsificación

Incluir este análisis daría al comercio el cuadro completo para decidir si conviene incentivar el pago en efectivo.

### 9.4 Dimensión geográfica

Esta guía está sesgada hacia GBA/PBA. Para una versión nacional:
- **NOA/NEA:** Banco Macro es el banco de referencia en esas regiones
- **Córdoba:** Naranja X tiene penetración muy alta; los comercios sin adhesión pierden clientes
- **Cuyo:** Presencia de Banco Supervielle y Banco de Mendoza como actores regionales relevantes

### 9.5 Fuentes no oficiales de alto valor

Para complementar la investigación oficial:
- **CAME (Confederación Argentina de la Mediana Empresa):** Publica informes periódicos sobre costos del comercio minorista. Herramientas destacadas: **calculadora de costos en cuotas** (redcame.org.ar/novedades/13344) que incorpora IIBB, tasas municipales e IVA; información sobre **Cuotas MiPyME** (reemplazó a Cuota Simple desde julio 2025) con tasas negociadas para pymes (redcame.org.ar/novedades/12205)
- **FECOBA (Federación de Comercio e Industria de la Ciudad de Buenos Aires):** Guías prácticas para comercios de CABA, incluyendo guía de pagos electrónicos con detalle de beneficios fiscales por categoría (monotributistas y responsables inscriptos) y asistencia en la gestión de programas de incentivo para la adopción de terminales (fecoba.com.ar)
- **BCRA Régimen de Transparencia** (bcra.gob.ar): Herramienta de comparación oficial entre entidades financieras — fuente primaria subutilizada en esta investigación
- **iProfesional / Cronista:** Para verificación secundaria de cambios regulatorios (no usar como fuente primaria)

---

*Documento elaborado para uso interno y como guía de contenido del proyecto monitor-comisiones-bancarias.
Los valores en ARS son válidos a la fecha de elaboración (febrero 2026) y deben actualizarse semestralmente.*
