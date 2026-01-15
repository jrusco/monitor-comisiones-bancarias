# **Informe Integral de Estructuras de Costos, Comisiones y Arquitectura Técnica de Procesamiento de Pagos en Argentina (2025-2026)**

## **1\. Inteligencia Ejecutiva y Contexto Macro-Regulatorio**

El ecosistema de medios de pago en la República Argentina ha experimentado una transformación estructural sin precedentes durante el último lustro, consolidándose hacia el ciclo 2025-2026 como uno de los mercados más dinámicos y complejos de América Latina. Este informe técnico, diseñado para directores financieros, desarrolladores de integraciones y decisores corporativos, ofrece un análisis exhaustivo de las comisiones, costos ocultos y capacidades tecnológicas de las cinco entidades dominantes solicitadas: **Banco de la Nación Argentina (BNA)**, **Banco de la Provincia de Buenos Aires (Banco Provincia)**, **Mercado Pago**, **Ualá** y **Fiserv**.  
La dinámica actual del mercado no puede entenderse simplemente a través de una lista de precios, sino que requiere una comprensión profunda de la bifurcación regulatoria entre **Adquirentes Tradicionales** y **Agregadores de Pagos (PSPs)**. Mientras que los primeros operan bajo los topes arancelarios estrictos impuestos por la Ley de Tarjetas de Crédito (Ley 25.065), los segundos han construido modelos de negocio basados en la velocidad de la liquidez, cobrando primas significativas por la disponibilidad inmediata de fondos en un entorno de alta inflación.

### **1.1 El Marco Normativo de los Aranceles Máximos**

La base de costos para todo el sistema se encuentra dictada por el Banco Central de la República Argentina (BCRA). A través de sucesivas comunicaciones, y reafirmado en la Comunicación “B” 13096/2025, se han establecido techos claros para las tasas de intercambio y los aranceles que los adquirentes pueden cobrar a los comercios.1  
En el esquema vigente para el periodo 2025-2026, los topes máximos que rigen para las operaciones directas con adquirentes (como Fiserv o las terminales bancarias directas) son:

* **1,80%** para transacciones con **Tarjeta de Crédito**.  
* **0,80%** para transacciones con **Tarjeta de Débito**.

Este marco regulatorio es crucial porque define el "piso" del mercado. Cualquier comisión superior a estos valores, como las observadas en Mercado Pago (6,29%) o Ualá (4,9%), no corresponde estrictamente a un "arancel de tarjeta", sino a una **comisión por servicio de agregación**, que incluye la gestión de liquidez, la provisión de tecnología sin costo de mantenimiento mensual y la simplificación fiscal.2

### **1.2 La Dicotomía: Liquidez vs. Rentabilidad**

El hallazgo central de esta investigación es la existencia de una "Prima de Liquidez" masiva. Los comercios argentinos se enfrentan a una elección binaria:

1. **Modelo Bancario (BNA / Provincia / Fiserv):** Maximizar el margen bruto pagando las comisiones reguladas más bajas (1,8%), a cambio de esperar los plazos de acreditación estándar (8 a 18 días hábiles para crédito) y asumir costos fijos de alquiler de terminales.  
2. **Modelo Fintech (Mercado Pago / Ualá):** Maximizar la velocidad del flujo de caja pagando comisiones entre 2 y 3 veces superiores (4,9% \- 6,3%), eliminando costos fijos y barreras de entrada burocráticas.

A continuación, se desglosa la oferta de cada entidad con el nivel de detalle técnico y financiero requerido.

## ---

**2\. Análisis Estructural del Sector Bancario Público**

La banca pública ha adoptado una estrategia híbrida para competir con las fintechs. Mantienen su rol como adquirentes de bajo costo para el segmento corporativo y PYME tradicional, mientras despliegan "sub-marcas" digitales (+Pagos, Cuenta DNI) que emulan la usabilidad de los agregadores pero con subsidios estatales o provinciales agresivos.

### **2.1 Banco de la Nación Argentina (BNA)**

El Banco Nación, siendo la mayor entidad financiera del país, opera con una doble lógica: la de fomento y la comercial. Su propuesta de valor se centra en ofrecer los costos transaccionales más bajos del mercado, apalancándose en su capacidad para bonificar los costos de infraestructura física.

#### **2.1.1 Estructura de Aranceles y Comisiones**

Para los comercios que operan bajo el paraguas de "Cuenta Comercios BNA" o la solución "+Pagos Nación", las comisiones se alinean estrictamente con los topes regulatorios, ofreciendo una ventaja competitiva directa en volumen.  
**Tabla 1: Esquema de Costos de Adquirencia BNA (2025)**

| Tipo de Operación | Tasa / Comisión | Detalle Técnico | Referencia |
| :---- | :---- | :---- | :---- |
| **Tarjeta de Débito** | **0,80%** \+ IVA | Acreditación en 24 horas hábiles. | 4 |
| **Tarjeta de Crédito** | **1,80%** \+ IVA | Acreditación estándar (8-10 días hábiles). | 5 |
| **Tarjeta Internacional** | **7,50%** \+ IVA | Tasa diferenciada para plásticos emitidos en el exterior. | 5 |
| **Pagos B2B** | **0,70%** \+ IVA | Para transferencias entre empresas (Esquema Tradicional). | 7 |
| **Acreditación de Valores** | **0,60%** | Comisión por gestión de valores fuera de canje (Mínimo $3.733). | 7 |

Análisis de Costos Ocultos y Administrativos:  
Es vital notar que el BNA aplica cargos adicionales por la gestión administrativa que no suelen estar presentes en las fintechs simplificadas. Por ejemplo, la "Gestión de aceptación y/o cobro" puede tener un cargo único de $50, y existen comisiones específicas para la operatoria de canje de valores (0,50% \+ IVA).7 Sin embargo, para los comercios adheridos a la plataforma BNA Conecta, existen membresías mensuales que van desde $17.500 (Microempresas) hasta $175.000 (Grandes Empresas), aunque estas suelen estar bonificadas en porcentajes que varían del 20% al 90% según el segmento.7

#### **2.1.2 Infraestructura y Bonificaciones**

El BNA no desarrolla su propio hardware, sino que distribuye terminales de **Fiserv** y **Payway**. Su estrategia comercial agresiva se basa en la **bonificación del 100%** del costo de mantenimiento de estas terminales por periodos de 12 meses para nuevos clientes. Esto elimina una de las principales barreras de entrada del modelo tradicional (el costo de alquiler mensual de \~$40.000), haciendo que la propuesta del BNA sea financieramente superior a Mercado Pago para comercios con facturación estable.8

#### **2.1.3 Recursos Técnicos y Solución Digital (+Pagos)**

La solución **\+Pagos Nación** permite a los comercios cobrar mediante QR y Link de Pago.

* **Recurso Web:** La información oficial y el acceso al portal de comercios se encuentra en: https://www.bna.com.ar/Empresas/Novedades/AdheriTuComercio.8  
* **Integración:** A diferencia de los agregadores puros que ofrecen APIs abiertas, la integración con BNA suele requerir la adhesión formal a través de su portal de "Alta Comercio Web", donde se valida la identidad fiscal (CUIT/CUIL) y se realizan chequeos de cumplimiento (UIF/PEP) antes de otorgar credenciales productivas.8

### **2.2 Banco de la Provincia de Buenos Aires (Banco Provincia)**

El Banco Provincia ha logrado una disrupción masiva con **Cuenta DNI**, una billetera digital que actúa como un sistema de "circuito cerrado" incentivado por reintegros provinciales. Para el comercio, aceptar Cuenta DNI no es solo una opción de cobro, sino una herramienta de atracción de clientes subsidiada.

#### **2.2.1 Tarifario y Estrategia de "Clave DNI"**

El Banco Provincia ha establecido una estructura de precios que desafía los estándares del mercado, perforando el piso del 0,8% para pagos con débito a través de su sistema propietario.  
**Tabla 2: Tarifario de Adquirencia Banco Provincia (2025)**

| Método de Cobro | Comisión (Arancel) | Plazo de Acreditación | Fuente |
| :---- | :---- | :---- | :---- |
| **Clave DNI (Token)** | **0,60%** | **Inmediata** | 9 |
| **QR (Saldo en Cuenta)** | **0,80%** \+ IVA | **Inmediata** | 9 |
| **Débito (POS/QR)** | **0,80%** \+ IVA | 24 Horas Hábiles | 9 |
| **Crédito (POS/QR)** | **1,80%** \+ IVA | 8 a 18 Días Hábiles\* | 9 |
| **American Express** | **2,80%** | Según plan de cuotas | 9 |

**Insight Estratégico:** La tasa del **0,60%** con acreditación inmediata para cobros vía "Clave DNI" representa el costo transaccional más bajo disponible en el mercado argentino para operaciones digitales. Esto posiciona al Banco Provincia como la opción fiscalmente más eficiente para comercios minoristas dentro de la Provincia de Buenos Aires, superando incluso a las transferencias 3.0 estándar en ciertos escenarios de fidelización.11

#### **2.2.2 Costos de Terminales y "Multas" por Inactividad**

A diferencia de las fintechs, el Banco Provincia transparenta el costo de alquiler de los dispositivos POS, el cual se traslada al comercio si no se cumplen las condiciones de bonificación.

* **Fiserv Posnet:** Costo mensual aproximado de **$37.979 \+ IVA**.9  
* **Clover (Mini/Flex):** Costo mensual aproximado de **$46.389 \+ IVA**.9  
* **Payway:** Implementa un esquema de precios penalizados para terminales "Inactivas" ($50.399) versus "Activas" ($41.999), incentivando el uso continuo del dispositivo para evitar el costo ocioso.9

#### **2.2.3 Recursos y Accesos**

* **Portal de Adhesión:** https://www.bancoprovincia.com.ar/web/adhesion\_comercios  
* **Simulador de Costos:** El banco ofrece herramientas para calcular el "Precio de Venta Financiado" utilizando los coeficientes vigentes (ej. Coeficiente de 1.1723 para 3 cuotas), permitiendo al comercio trasladar el Costo Financiero Total (CFT) de manera precisa.9

## ---

**3\. El Sector Fintech: Agregadores y la Prima de Liquidez**

El sector fintech, liderado por Mercado Pago y Ualá, opera bajo una lógica de "Agregación". Jurídicamente, el agregador es el comercio ante la tarjeta, y sus usuarios son "sub-comercios". Esto les permite ofrecer onboarding instantáneo y, crucialmente, **liquidez inmediata**, cobrando por ello una prima sustancial sobre los aranceles bancarios.

### **3.1 Mercado Pago (MercadoLibre S.R.L.)**

Mercado Pago es el estándar de facto para la adquirencia no bancaria. Su modelo de ingresos se basa en la flexibilidad: el comercio decide cuánto pagar en función de cuándo desea recibir el dinero.

#### **3.1.1 Matriz de Costos Point y QR**

La estructura de comisiones de Mercado Pago es dinámica y varía según el dispositivo (Point) o el método (QR). Los valores presentados a continuación incluyen el IVA y representan el costo total directo para el comercio.  
**Tabla 3: Costos de Procesamiento Mercado Pago Point (2025)**

| Medio de Pago | Plazo de Liberación | Comisión \+ IVA | Análisis vs. Bancos |
| :---- | :---- | :---- | :---- |
| **Débito** | **En el momento** | **3,25%** \+ IVA | \~4x más caro que el 0,8% bancario. |
| **Débito** | 24 horas | **2,99%** \+ IVA | Sigue siendo 3.7x más caro. |
| **Crédito** | **En el momento** | **6,29%** \+ IVA | **Prima de Liquidez Extrema.** |
| **Crédito** | 5 días | **5,39%** \+ IVA | Costo alto por velocidad media. |
| **Crédito** | 10 días | **4,39%** \+ IVA | Más del doble del arancel bancario. |
| **Crédito** | 18 días | **3,39%** \+ IVA | Aún no competitivo con bancos. |
| **Crédito** | 35 días | **1,49%** \+ IVA | Única tasa competitiva (menor al 1,8%). |

**Fuente de Datos:**.14
**Consideración Regional (Buenos Aires):** Los valores de comisión presentados en la Tabla 3 corresponden específicamente a comercios registrados en la **Provincia de Buenos Aires**, según lo establecido en la política de aranceles vigente desde el 1 de agosto de 2025. Mercado Pago aplica tarifas diferenciadas por provincia; comercios en otras jurisdicciones pueden experimentar variaciones. Se recomienda consultar el simulador oficial para la provincia específica.14
**Insight de Segundo Orden:** La tasa del **6,29% \+ IVA** para crédito inmediato implica que el comercio está pagando una tasa efectiva anualizada (TEA) implícita astronómica por adelantar esos fondos 10-18 días. Sin embargo, en un contexto de alta volatilidad cambiaria o necesidad de reposición de stock urgente, muchos comercios validan este costo como un "seguro de liquidez".

#### **3.1.2 Arquitectura Técnica y API**

Mercado Pago ofrece la documentación más robusta para desarrolladores, permitiendo integraciones profundas.

* **Portal de Desarrolladores:** https://www.mercadopago.com.ar/developers.17  
* **Endpoint Principal de Pagos:**  
  HTTP  
  POST https://api.mercadopago.com/v1/payments

* Estructura del Payload:  
  Para procesar un pago y obtener el desglose de comisiones en tiempo real, el cuerpo de la solicitud (JSON) debe incluir:  
  JSON  
  {  
    "transaction\_amount": 1000,  
    "description": "Venta Articulo X",  
    "payment\_method\_id": "visa",  
    "payer": { "email": "cliente@email.com" },  
    "installments": 1  
  }

* **Respuesta de Costos (Fee Details):** La API retorna un objeto transaction\_details que desglosa el net\_received\_amount (monto neto) y el total\_paid\_amount. Esto es crítico para sistemas ERP que necesitan conciliar automáticamente la comisión de MP antes de que el dinero entre en cuenta.5  
* **Webhooks:** Se recomienda configurar notificaciones para los eventos payment.created y payment.updated para manejar la asincronía de los pagos con tarjeta de crédito.19

### **3.2 Ualá (Ualá Bis)**

Ualá Bis se posiciona como el retador "simplificado", atacando el mercado con una propuesta de tarifas planas y acreditación inmediata por defecto, eliminando la matriz de plazos complejos de Mercado Pago.

#### **3.2.1 Estructura de Comisiones "Low Cost"**

Ualá Bis promociona sus comisiones como "bajas", aunque esto es relativo al competidor (Mercado Pago) y no a la banca tradicional. Su gran diferenciador es la **Inmediatez**.

* **Tarjeta de Débito (mPOS):** **2,90%** \+ IVA.  
  * *Comparativa:* Más barato que el 3,25% instantáneo de MP, pero mucho más caro que el 0,8% de BNA/Provincia.  
* **Tarjeta de Crédito (mPOS):** **4,40%** a **4,90%** \+ IVA.  
  * *Comparativa:* Significativamente inferior al 6,29% de MP para liquidez inmediata. Aquí reside su ventaja competitiva para micro-comercios.20  
* **Link de Pago / E-commerce:** **4,90%** \+ IVA. Mantiene la coherencia con la tasa presencial de crédito.  
* **QR (Transferencias):** **0,60%**. Iguala la agresividad del Banco Provincia y cumple con la normativa de Transferencias 3.0 para pagos con saldo en cuenta.21

#### **3.2.2 Hardware y Modelo de Negocio**

Ualá subsidia fuertemente el hardware. El dispositivo **POS Pro** (terminal autónoma con impresora) se vende a precios nominales y, crucialmente, **no tiene costo de mantenimiento mensual**. Esto contrasta con los \~$40.000 mensuales de una terminal Clover o Posnet bancaria (cuando no está bonificada), haciendo que Ualá sea la opción matemática preferente para comercios con facturación baja o estacional.22

#### **3.2.3 Recursos para Desarrolladores (API Checkout)**

Ualá ha madurado su oferta técnica con una API de Checkout para integraciones personalizadas.

* **Portal de Desarrolladores:** https://developers.ualabis.com.ar/.23  
* **Endpoint de Creación de Orden:**  
  HTTP  
  POST https://checkout.developers.ar.ua.la/v2/api/orders

* **Autenticación:** Utiliza un flujo de OAuth2 (client\_credentials) para obtener un access\_token.25  
* **SDKs Oficiales:** Ualá mantiene librerías oficiales en GitHub para **Node.js** (ualabis-nodejs), **PHP** (ualabis-php) y plugins para Magento, facilitando la integración en plataformas de e-commerce populares.26

## ---

**4\. Infraestructura de Procesamiento: Fiserv (La Columna Vertebral)**

Fiserv (anteriormente First Data) no es un agregador, sino la infraestructura de adquirencia sobre la que corre gran parte del sistema financiero argentino. Su relación comercial suele ser intermediada por bancos, pero define la tecnología en el punto de venta.

### **4.1 Modelo de Adquirencia Directa**

Cuando un comercio opera con Fiserv (a través de una alta bancaria), accede a los **Aranceles Regulados** puros.

* **Web de Aranceles:** https://aranceles.fiservargentina.com/.3  
* **Tarifas Vigentes:**  
  * **Débito:** 0,80% \+ IVA (Acreditación en 24hs).  
  * **Crédito:** 1,80% \+ IVA (Acreditación en 8-18 días hábiles según tamaño del contribuyente).3  
* **Planes de Cuotas:** Fiserv administra los coeficientes financieros para los planes "Ahora" (Cuota Simple) y "Cuota a Cuota". Por ejemplo, para un plan de 12 cuotas, el coeficiente (a Noviembre 2025\) ronda el **1.5441**, lo que implica un costo financiero directo considerable que debe ser trasladado al precio o absorbido.13

### **4.2 Ecosistema Clover**

Fiserv está migrando activamente su base instalada de las terminales "Posnet" tradicionales a la plataforma **Clover**.

* **Costo de Hardware:** Como se detalló en la sección de Banco Provincia, el alquiler de una Clover Mini ronda los **$46.389** mensuales.  
* **App Market y Monetización:** Clover no es solo una terminal de pagos; es una plataforma Android gestionada. Fiserv opera un "App Market" donde desarrolladores terceros pueden publicar aplicaciones (gestión de stock, fidelización, RRHH). El modelo de ingresos es un **Revenue Share 70/30** (70% para el desarrollador, 30% para Fiserv), lo que abre una vía de negocio para integradores de software.27

### **4.3 API Clover para Argentina**

La integración con Clover es diferente a la de las fintechs web. Se basa en SDKs para Android (para apps que corren en el dispositivo) y una REST API para gestión remota.

* **Sandbox:** https://sandbox.dev.clover.com.29  
* **Limitaciones Regionales:** La documentación de Fiserv advierte explícitamente sobre "Features & Limitations" para la región LATAM (Argentina), donde ciertas funciones de recargos (surcharging) o manejo de impuestos difieren de la versión estadounidense debido a la complejidad fiscal local.30

## ---

**5\. Análisis Comparativo de Costos Totales (TCA)**

Para sintetizar la información y facilitar la toma de decisiones, presentamos una simulación de costos para una venta de **$100.000 ARS** con Tarjeta de Crédito, asumiendo la necesidad de liquidez inmediata vs. la espera estándar.  
**Tabla 4: Simulación de Costo Neto por Venta de $100.000 (Crédito)**

| Proveedor | Modelo | Comisión \+ IVA | Costo Fijo Mensual | Neto a Recibir | Disponibilidad |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Fiserv (Vía BNA)** | Adquirente | $2.178 (1,8% \+ IVA) | $0 (Bonificado 12 meses) | **$97.822** | 10 Días |
| **Fiserv (Sin Bonificación)** | Adquirente | $2.178 (1,8% \+ IVA) | \~$46.000 (Alquiler) | **$97.822** (\*) | 10 Días |
| **Ualá Bis** | Agregador | $5.929 (4,9% \+ IVA) | $0 | **$94.071** | **Inmediata** |
| **Mercado Pago** | Agregador | $7.610 (6,29% \+ IVA) | $0 | **$92.390** | **Inmediata** |
| **Mercado Pago** | Agregador | $1.802 (1,49% \+ IVA) | $0 | **$98.198** | **35 Días** |

(\*) *Nota:* En el caso de Fiserv sin bonificación, el costo fijo de $46.000 debe diluirse en el volumen total de ventas. Para un comercio pequeño, este costo fijo puede ser devastador, haciendo que el modelo de porcentaje variable de las fintechs sea más económico a pesar de las tasas altas.  
Insight Fiscal (Retenciones):  
A estos costos de comisión se deben sumar las Retenciones Impositivas (IVA, Ganancias, Ingresos Brutos).

* **Adquirentes (Bancos):** Actúan como agentes de retención estrictos al momento de la liquidación (día 10).  
* **Agregadores (Fintech):** También retienen, pero la inmediatez del cobro a veces genera la percepción errónea de menor carga impositiva. Sin embargo, sistemas como el **SIRCREB** aplican igualmente sobre las billeteras virtuales. Mercado Pago y Ualá desglosan estas retenciones en sus reportes de API (tax\_details), permitiendo al comercio usar esos saldos como crédito fiscal.31

## ---

**6\. Guía Técnica de Integración y Recursos**

Para los equipos de desarrollo e integración, consolidamos aquí los puntos de acceso críticos identificados en la investigación.

### **6.1 Mercado Pago**

* **Documentación:** https://www.mercadopago.com.ar/developers  
* **Autenticación:** Authorization: Bearer YOUR\_ACCESS\_TOKEN  
* **Idempotencia:** Se requiere el header X-Idempotency-Key en las llamadas POST para evitar cobros duplicados en redes inestables.33  
* **Recurso Clave:** Simulador de Costos en la web para validar cálculos de API: https://www.mercadopago.com.ar/ayuda/costos-financiacion-point\_2548.34

### **6.2 Ualá Bis**

* **Documentación:** https://developers.ualabis.com.ar/  
* **Repositorios SDK:** https://github.com/Uala-Developers (Node.js, PHP, Magento).26  
* **Manejo de Errores:** La API retorna códigos de error estándar (400, 401, 500\) con mensajes descriptivos en JSON (ej. "Invalid amount value") que facilitan el debugging.24

### **6.3 Fiserv / Clover**

* **Documentación:** https://docs.clover.com/  
* **Estrategia:** La integración es más compleja y orientada a "Semi-Integration" donde el POS controla el flujo de pago y la PC/Tablet solo envía el monto. Esto reduce el alcance PCI-DSS para el comercio.35

## ---

**7\. Conclusiones Estratégicas**

El mercado de procesamiento de pagos argentino para el ciclo 2025-2026 presenta una clara segmentación estratégica:

1. **Para el Comercio Corporativo / PYME Estable:** La ruta óptima sigue siendo la bancaria (**BNA** o **Banco Provincia**). Al adherirse a través de estas entidades, se accede a la red **Fiserv** con los aranceles mínimos de ley (1,8%/0,8%) y se neutraliza el costo de hardware mediante las bonificaciones anuales. El costo de esperar 10 días por los fondos es financieramente menor que pagar el 6% de comisión, salvo en escenarios de hiperinflación aguda.  
2. **Para el Micro-Comercio y la Economía Gig:** **Ualá Bis** ha logrado posicionarse como la alternativa superior en costos para quienes necesitan inmediatez, con una tasa de crédito (4,9%) significativamente menor a la de Mercado Pago (6,29%). La ausencia de costo de mantenimiento de terminal refuerza esta posición.  
3. **Para Desarrolladores y Experiencia de Usuario:** **Mercado Pago** mantiene el liderazgo en calidad de API y documentación. Si el modelo de negocio depende de una integración digital compleja (split payments, suscripciones, marketplace), el sobrecosto de Mercado Pago se justifica por la robustez de su stack tecnológico.  
4. **La Oportunidad Fiscal:** El uso de **Cuenta DNI** (Banco Provincia) con su tasa del **0,6%** representa una anomalía de mercado que debe ser explotada por cualquier comercio con presencia en Buenos Aires, funcionando efectivamente como un subsidio a la transacción.

Este panorama exige que la decisión de proveedor no sea estática; los comercios deben auditar sus costos semestralmente, aprovechando la portabilidad y la interoperabilidad (QR Transferencias 3.0) para arbitrar entre las tasas de los diferentes proveedores.

#### **Works cited**

1. El BCRA fijó un nuevo tope a la tasa de interés de tarjetas no ..., accessed January 6, 2026, [https://radiorafaela.com.ar/interes-general/el-bcra-fijo-un-nuevo-tope-a-la-tasa-de-interes-de-tarjetas-no-bancarias](https://radiorafaela.com.ar/interes-general/el-bcra-fijo-un-nuevo-tope-a-la-tasa-de-interes-de-tarjetas-no-bancarias)  
2. Tarjeta de débito \- BCRA, accessed January 6, 2026, [https://www2.bcra.gob.ar/MediosPago/Tarjeta-de-debito.asp](https://www2.bcra.gob.ar/MediosPago/Tarjeta-de-debito.asp)  
3. Fiserv | Pagos con QR, accessed January 6, 2026, [https://aranceles.fiservargentina.com/](https://aranceles.fiservargentina.com/)  
4. Simulador de Ventas - +Pagos Nación (BNA), accessed January 15, 2026, [https://maspagos.com.ar/simulador-de-ventas](https://maspagos.com.ar/simulador-de-ventas)  
5. Aranceles Regulados BCRA - Tasas de Débito y Crédito, accessed January 15, 2026, [https://maspagos.com.ar/simulador-de-ventas](https://maspagos.com.ar/simulador-de-ventas)  
6. En enero bajaron los aranceles que pagan los comercios a las tarjetas, accessed January 6, 2026, [https://www.argentina.gob.ar/noticias/en-enero-bajaron-los-aranceles-que-pagan-los-comercios-las-tarjetas](https://www.argentina.gob.ar/noticias/en-enero-bajaron-los-aranceles-que-pagan-los-comercios-las-tarjetas)  
7. COMISIONES Y CARGOS \- CARTERA COMERCIAL \- Banco Nación, accessed January 6, 2026, [https://www.bna.com.ar/Downloads/ComisionesYCargosComercial.pdf](https://www.bna.com.ar/Downloads/ComisionesYCargosComercial.pdf)  
8. Cuenta Comercios BNA \- Banco de la Nación Argentina, accessed January 6, 2026, [https://www.bna.com.ar/Empresas/Novedades/AdheriTuComercio](https://www.bna.com.ar/Empresas/Novedades/AdheriTuComercio)  
9. Potenciá los ingresos de tu comercio \- Banco de la Provincia de ..., accessed January 6, 2026, [https://www.bancoprovincia.com.ar/web/adhesion\_comercios](https://www.bancoprovincia.com.ar/web/adhesion_comercios)  
10. BP0507 \- COMISIONES Y CARGOS \- OTROS SERVICIOS, accessed January 6, 2026, [https://www.bancoprovincia.com.ar/CDN/Get/BP0507\_WEB](https://www.bancoprovincia.com.ar/CDN/Get/BP0507_WEB)  
11. Sumate a Cuenta DNI Comercios \- Provincia Microcréditos, accessed January 6, 2026, [https://www.provinciamicrocreditos.com.ar/comunidad/cdnicomercios2024/](https://www.provinciamicrocreditos.com.ar/comunidad/cdnicomercios2024/)  
12. Cómo adherir un comercio a Cuenta DNI: requisitos, comisiones y ..., accessed January 6, 2026, [https://www.ambito.com/informacion-general/como-adherir-un-comercio-cuenta-dni-requisitos-comisiones-y-paso-paso-n5867618](https://www.ambito.com/informacion-general/como-adherir-un-comercio-cuenta-dni-requisitos-comisiones-y-paso-paso-n5867618)  
13. Fiserv Argentina. Novedades en Procesamiento de Pagos., accessed January 6, 2026, [https://www.fiserv.com.ar/novedades/todas-las-novedades/](https://www.fiserv.com.ar/novedades/todas-las-novedades/)  
14. ¿Cuánto cuesta recibir pagos con Point? - Mercado Pago (Buenos Aires), accessed January 15, 2026, [https://www.mercadopago.com.ar/ayuda/2779#tabla1](https://www.mercadopago.com.ar/ayuda/2779#tabla1)  
15. ¿Cuánto cuesta recibir pagos con QR? - Mercado Pago (Buenos Aires), accessed January 15, 2026, [https://www.mercadopago.com.ar/ayuda/3605#tabla1](https://www.mercadopago.com.ar/ayuda/3605#tabla1)  
16. Comisiones y cargos para individuos y vendedores \- Mercado Pago, accessed January 6, 2026, [https://www.mercadopago.com.ar/ayuda/26748](https://www.mercadopago.com.ar/ayuda/26748)  
17. Overview \- Checkout API (via Orders) \- Mercado Pago Developers, accessed January 6, 2026, [https://www.mercadopago.com.ar/developers/en/docs/checkout-api-orders/overview](https://www.mercadopago.com.ar/developers/en/docs/checkout-api-orders/overview)  
18. Other payment methods \- Integration configuration \- Mercado Pago ..., accessed January 6, 2026, [https://www.mercadopago.com.ar/developers/en/docs/checkout-api-payments/integration-configuration/other-payment-methods](https://www.mercadopago.com.ar/developers/en/docs/checkout-api-payments/integration-configuration/other-payment-methods)  
19. Create payment \- Payments \- Mercado Pago Developers, accessed January 6, 2026, [https://www.mercadopago.com.co/developers/en/reference/payments/\_payments/post](https://www.mercadopago.com.co/developers/en/reference/payments/_payments/post)  
20. POS Pro - Aranceles y Comisiones - Ualá Bis, accessed January 15, 2026, [https://www.ualabis.com.ar/pos-pro](https://www.ualabis.com.ar/pos-pro)  
21. POS Pro - Solución de Cobros - Ualá Bis, accessed January 15, 2026, [https://www.ualabis.com.ar/pos-pro](https://www.ualabis.com.ar/pos-pro)  
22. Comprá tu mPOS en la web \- Las mejores comisiones \- Ualá Bis, accessed January 6, 2026, [https://mpos.ualabis.com.ar/productos/mpos/](https://mpos.ualabis.com.ar/productos/mpos/)  
23. Ualá Bis \- API Cobros Online, accessed January 6, 2026, [https://developers.ualabis.com.ar/v2/orders/get/snippets/js](https://developers.ualabis.com.ar/v2/orders/get/snippets/js)  
24. Crear Orden \- API Cobros Online \- Ualá Bis, accessed January 6, 2026, [https://developers.ualabis.com.ar/v2/orders/create](https://developers.ualabis.com.ar/v2/orders/create)  
25. API Cobros Online \- Ualá Bis, accessed January 6, 2026, [https://developers.ualabis.com.ar/v2/authentication/create/snippets/js](https://developers.ualabis.com.ar/v2/authentication/create/snippets/js)  
26. Uala-Developers \- GitHub, accessed January 6, 2026, [https://github.com/Uala-Developers](https://github.com/Uala-Developers)  
27. Monetize your apps \- Clover Developer, accessed January 6, 2026, [https://docs.clover.com/dev/docs/monetizing-your-apps](https://docs.clover.com/dev/docs/monetizing-your-apps)  
28. Fintech \- Fiserv AppMarket, accessed January 6, 2026, [https://appmarket.fiservapps.com/fintech](https://appmarket.fiservapps.com/fintech)  
29. Transaction data: Charges and fees \- Clover Developer, accessed January 6, 2026, [https://docs.clover.com/dev/docs/transaction-data](https://docs.clover.com/dev/docs/transaction-data)  
30. Region Specific Features and Limitations \- FISERV, accessed January 6, 2026, [https://docs.apis-fiserv.com/latam/docs/card-present-clover-region-features-limitations](https://docs.apis-fiserv.com/latam/docs/card-present-clover-region-features-limitations)  
31. ¿Cuánto cuesta recibir pagos con Point? - Mercado Pago, accessed January 15, 2026, [https://www.mercadopago.com.ar/ayuda/2779](https://www.mercadopago.com.ar/ayuda/2779)  
32. Modificación a la Ley de Tarjetas de Crédito \- Allende & Brea, accessed January 6, 2026, [https://allende.com/reforma-argentina-2024-25/modificacion-a-la-ley-de-tarjetas-de-credito-12-21-2023/](https://allende.com/reforma-argentina-2024-25/modificacion-a-la-ley-de-tarjetas-de-credito-12-21-2023/)  
33. Other payment methods \- Integration configuration \- Mercado Pago, accessed January 6, 2026, [https://www.mercadopago.com.co/developers/en/docs/checkout-api-payments/integration-configuration/other-payment-methods](https://www.mercadopago.com.co/developers/en/docs/checkout-api-payments/integration-configuration/other-payment-methods)  
34. Cómo calcular tus comisiones en Mercado Pago de modo facil, accessed January 6, 2026, [https://www.youtube.com/watch?v=P0htygBh8-I](https://www.youtube.com/watch?v=P0htygBh8-I)  
35. Clover Developer Docs Home, accessed January 6, 2026, [https://docs.clover.com/dev/docs/home](https://docs.clover.com/dev/docs/home)