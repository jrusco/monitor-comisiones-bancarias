# Merchant Interview Guide
*For: Hidden Costs Research — Argentine Small Business Payment Providers*
*Version: 1.0 — February 2026*

---

## Logistics

| Item | Detail |
|------|--------|
| **Target** | 5–8 interviews with Argentine small business owners who accept card payments |
| **Duration** | 30–45 minutes per session |
| **Format** | In-person or phone; conversational, not structured |
| **Note-taking** | Capture quotes verbatim where possible; note what surprised you |
| **Recording** | Not required — mention the tool will be free and public; record only if the merchant explicitly agrees |
| **Consent** | Mention that the conversation will inform a free public tool; no personal data is collected |

**Ideal merchant profile:**
- Runs a small or medium business (retail, gastronomy, services)
- Accepts debit and/or credit card via terminal or mobile reader
- GBA/PBA-based for v1, though any Argentine merchant is useful
- Mix of providers is valuable (Mercado Pago, Ualá, Banco Nación, Banco Provincia, etc.)

---

## Intro Script

> *"Hola, gracias por tomarte el tiempo. Estamos construyendo una herramienta gratuita para comercios, y queremos entender cómo tomás decisiones sobre tus medios de cobro — no para venderte nada, sino para entender qué información te sería útil. No hay respuestas correctas o incorrectas. Si en algún momento no querés responder algo, no hay problema. ¿Arrancamos?"*

---

## Part 1 — Current Setup
**Goal:** Establish facts about what the merchant uses today, without influencing later answers about costs or switching.
**Time:** ~5 minutes

**Questions:**
1. "¿Con qué terminales o aplicaciones cobrás con tarjeta hoy?"
2. "¿Hace cuánto tenés esa solución?"
3. "¿Cómo llegaste a usar ese proveedor — fue una búsqueda activa o llegó por algún otro motivo?"
4. "¿Tenés más de un proveedor, o usás uno solo?"

**Probe if they use multiple providers:** "¿Por qué dos? ¿Hay algo que uno hace mejor que el otro?"

**Interviewer note:** Don't ask about costs yet. Let the merchant settle into the conversation. Note the provider(s) — this will inform how you interpret cost questions later.

---

## Part 2 — Cost Awareness
**Goal:** Answer unknown #1 — do merchants actually know what they pay in fees?
**Time:** ~10 minutes

**Questions:**
1. "¿Sabés más o menos cuánto pagás por mes en comisiones de tarjeta?"
2. "¿Cómo calculás ese número — lo ves en un resumen, lo estimás, o no lo tenés muy claro?"
3. "¿Revisás los resúmenes de liquidación que te manda tu proveedor?"
4. "¿Cómo te enterás cuando cambian las tarifas?"
5. "¿Alguna vez te sorprendió un cobro que no esperabas?"

**Probe if they say they don't review:** "¿Quién se encarga de eso en tu negocio, o nadie en particular?"

**Probe if they cite an exact number:** "¿De dónde sacás ese número — lo calculás vos o viene de algún lado?"

**Interviewer note:** This section answers the core question: rational optimizer vs. passive payer. If they can't estimate their monthly fee, the product thesis of "show them the real cost" may need to be reframed.

---

## Part 3 — Bonification & the "Month 13" Problem
**Goal:** Answer unknown #2 — is the bonification expiry visible or invisible to merchants?
**Time:** ~10 minutes

> **Critical:** Do NOT use the word "bonificación" first. Let the merchant introduce it. If they never use the word, probe gently with neutral terms.

**Questions:**
1. "¿Tu terminal o lector tiene algún costo mensual, o es gratis?"
2. "¿Ese costo siempre fue igual, o cambió en algún momento desde que arrancaste?"
3. *(If they mention a promotional period or free period):* "¿Sabés hasta cuándo dura eso?"
4. *(If they didn't mention a promo period):* "¿Te ofrecieron algún período de prueba o descuento cuando arrancaste con ese proveedor?"
5. "¿Recibís algún aviso antes de que cambie tu tarifa, o te enterás cuando ves el débito?"

**Probe if they mention bonification spontaneously:** "¿Cuándo arrancó eso? ¿Sabés cuándo termina?"

**Probe if they seem unaware:** "¿Cómo sabés cuánto vas a pagar el mes que viene?"

**Interviewer note:** The "month 13 trap" is the highest-leverage product insight from the research. If 4+ of 8 merchants are unaware their bonification expires, that validates a proactive alert feature. If merchants are fully aware, the alert is less valuable than assumed.

---

## Part 4 — Switching Behavior
**Goal:** Answer unknown #3 — what actually triggers a provider change? Is it rational comparison or something else?
**Time:** ~10 minutes

**Questions:**
1. "¿Alguna vez cambiaste de proveedor de cobro con tarjeta?"
   - *(If yes):* "¿Qué te hizo decidirte a cambiar?"
   - *(If yes):* "¿Fue fácil el proceso de cambio, o fue un trámite?"
   - *(If no):* "¿Qué haría falta para que te cambiaras — qué tendría que pasar?"
2. "¿Comparaste opciones antes de elegir el que tenés ahora, o fue más directo?"
3. "¿Sabés si hay algún proveedor que cobre menos que el tuyo en este momento?"

**Hypothetical for non-switchers:** "Si te enteraras de que podrías ahorrar $30.000 por mes cambiando de proveedor, ¿qué harías primero — buscar más info, hablar con tu contador, o directamente lo harías?"

**Probe on friction:** "¿Hay algo que te frene de cambiar aunque supieras que podrías pagar menos?"

**Interviewer note:** This section separates rational optimizers from inertia-driven merchants. "I'd ask my accountant" or "I'd need my accountant to tell me it's safe" is a critical signal — it means the product's real user may be the accountant, not the merchant directly.

---

## Part 5 — Information-Seeking Behavior
**Goal:** Answer unknown #4 — where do merchants go for information? Do they seek it independently or rely on intermediaries?
**Time:** ~5 minutes

**Questions:**
1. "Cuando tenés una duda sobre los costos de cobrar con tarjeta, ¿a quién le preguntás primero?"
2. "¿Buscás información online sobre esto, o preferís preguntarle a alguien de confianza?"
3. "¿Tu banco o proveedor te explica bien cómo funcionan las tarifas, o es difícil de entender?"
4. "¿Usarías una herramienta web gratuita que compare los costos reales de cada proveedor, con datos actualizados?"

**Probe if they say yes to tool:** "¿La buscarías vos, o esperarías que te la recomiende alguien?"

**Probe if they cite their accountant:** "¿Cuántas veces por año hablás con tu contador sobre estos temas?"

**Interviewer note:** If the dominant answer is "my accountant" or "my bank rep," the distribution strategy changes (target accountants as intermediaries, not merchants directly). This is a product-market fit question as much as a UX question.

---

## Closing Script

> *"Perfecto, eso es todo lo que necesitaba. Muchas gracias — esto es exactamente el tipo de información que hace que la herramienta sea útil para comercios reales. Cuando tengamos algo listo, te voy a avisar. ¿Te puedo contactar si surge alguna duda puntual?"*

---

## Post-Interview Synthesis Notes Template

*Complete within 30 minutes of ending the interview, while memory is fresh.*

```
Interview #: ___
Date: ___
Duration: ___
Merchant type (retail / gastronomy / services / other): ___
Estimated monthly card volume (their estimate or your impression): ___
Current provider(s): ___

--- UNKNOWNS ANSWERED ---

Unknown #1 — Cost awareness:
[ ] Knows exact monthly fee
[ ] Has rough estimate
[ ] No idea
[ ] Delegates to accountant/employee
Quote: "___"

Unknown #2 — Bonification awareness:
[ ] Fully aware (knows when it expires)
[ ] Partially aware (knows it exists, not when it ends)
[ ] Unaware (didn't know about it)
[ ] Not applicable (no bonification)
Quote: "___"

Unknown #3 — Switching behavior:
[ ] Has switched (trigger: ___)
[ ] Considered switching but didn't (reason: ___)
[ ] Never considered switching
[ ] Would switch if given data
Key insight: ___

Unknown #4 — Information source:
[ ] Accountant first
[ ] Bank/provider rep
[ ] Independent online search
[ ] Peer merchants
[ ] Doesn't seek info proactively
Quote: "___"

--- IMPRESSIONS ---

Biggest surprise from this interview: ___

Signal: rational optimizer vs. inertia-driven?
(circle one): RATIONAL   INERTIA   MIXED

Would use the tool?  YES / MAYBE / NO
Would they recommend it to others?  YES / MAYBE / NO

--- PRODUCT IMPLICATIONS ---

One thing this interview changes about the product (if anything): ___
```

---

## Synthesis Plan

*After all interviews are complete:*

Run a tally across all interviews to answer the four unknowns:

| Unknown | Question | Tally |
|---------|----------|-------|
| #1 | Cost awareness | _/8 merchants knew their monthly fee |
| #2 | Bonification visibility | _/8 merchants knew their bonification expires |
| #3 | Switching trigger | _/8 have ever switched providers |
| #4 | Info source | _/8 cited accountant as first reference |

**Decision rules based on findings:**

| If... | Then... |
|-------|---------|
| <3/8 know their monthly cost | Lead with cost transparency feature, not savings optimization |
| <3/8 are aware of bonification expiry | Proactive expiry alert is highest-priority v1 feature |
| >5/8 rely on accountant for info | Design for accountants as primary distribution channel |
| >5/8 cite inertia as switching blocker | Focus on reducing friction to act, not just information |

**Output:** Condense findings into a 1-page summary answering each unknown with tally data and 2–3 representative quotes. This summary becomes an appendix of the PRD.

---

*Guide created for sprint research phase — February 2026.*
*Linked to: `docs/research-hidden-costs-for-business-owners.md`, `docs/things-to-improve.md`*
