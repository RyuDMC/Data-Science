# Fuentes que justifican los pesos del scoring

Justificación documental de los pesos de `codes/analisis.py`
(precio 0.40 · autonomía 0.25 · carga 0.20 · legalidad 0.10 · repuestos 0.05).

**Nota de honestidad:** ningún estudio publica exactamente estos valores para
triciclos en La Habana. Los pesos son una **decisión de juicio experto del
proyecto**; la literatura respalda el **orden de importancia y las magnitudes**,
y la normativa cubana respalda la inclusión del criterio de legalidad.
Presentarlos en el reporte como "juicio experto calibrado con literatura".

Links verificados con HTTP 200 el 2026-10-15 (⚠️ marcados: solo navegador).

---

## 1. Precio = 0.40 (peso dominante)

- **Niu, X.; Song, Y.; Zhu, H. (2024).** *Data-Driven Decision Aids for
  Purchasing Battery Electric Vehicles Based on PROMETHEE-II Methodology.*
  **IEEE Access, vol. 12, pp. 27931–27946.**
  Asigna al criterio **precio un peso de 0.417** y varía ese peso ±25% en su
  análisis de sensibilidad (muy cercano a nuestro 0.40).
  - https://ieeexplore.ieee.org/document/10440069 ⚠️ (IEEE anti-bot; abre en navegador)

- **ISAHP 2022 (Indonesia).** *Developing an AHP-based model for the
  Problem-Solution Fit of Battery Electric Vehicles (BEV): a case of the most
  affordable BEV in Indonesian Market.*
  Modelo AHP: el dolor dominante es el **alza de precios de combustible
  (local priority 0.40)**; la ganancia dominante es *Affordability* (0.45).
  - http://www.isahp.org/uploads/051_003.pdf

- **Contexto Cuba (magnitud del gasto):** los triciclos cuestan
  US$2.000–4.500 y reemplazan al transporte público en la crisis energética.
  - https://apnews.com/article/cuba-fuel-crisis-electric-tricycles-fa75dc2aca5b78dac90b1e86c7c762b1 ⚠️ (403 a bots; abre en navegador)

## 2. Autonomía = 0.25 (segundo)

- **Hidrue, M.K.; Parsons, G.R.; Kempton, W.; Gardner, M.P. (2011).**
  *Willingness to pay for electric vehicles and their attributes.*
  **Resource and Energy Economics, 33(3), 686–705** (n=3.029; encuesta +
  experimento de elección). Conclusión textual: *"Driving range, fuel cost
  savings, and charging time led in importance to respondents."*
  - Ficha: https://ideas.repec.org/a/eee/resene/v33y2011i3p686-705.html
  - PDF: https://www1.udel.edu/V2G/resources/HidrueEtAl-Pay-EV-Attributes-correctedProof.pdf

- **Hong, X. et al. (2024).** *Consumer Preferences and Willingness to Pay for
  Electric Vehicles and Their Attributes* (Shandong, China; experimento de
  elección). Recopila WTP por autonomía: **US$14,5–151/km** adicional
  (Hackbarth & Madlener), CNY587/km (Qian et al.); el precio tiene el
  coeficiente negativo esperado y la autonomía, la mayor WTP tras la garantía.
  - https://www.pjoes.com/pdf-184151-112590

## 3. Carga = 0.20 (tercero)

- **Trung, D.D.; Ersoy, N.; Mai, N.T.; Thinh, H.X. (2025).** *Applying MCDM
  methods for electric vehicle selection: a comparative study between CRADIS
  and PIV methods.* **Journal of Applied Engineering Science, 23(2), 345–358.**
  Tabla 1 (20 estudios MCDM de selección de VE): *price, range, battery life,
  charging time* son los criterios más usados; *cargo/storage space* aparece
  en los estudios de uso comercial. También documenta que el método de
  ponderación cambia rankings → justifica nuestro análisis de sensibilidad.
  - https://doi.org/10.5937/jaes0-56793
  - Texto completo: https://www.engineeringscience.rs/articles/applying-mcdm-methods-for-electric-vehicle-selection-a-comparative-study-between-cradis-and-piv-methods

- **Contexto de uso (Cuba):** el triciclo es vehículo de trabajo — la carga
  útil equivale a capacidad de ingreso del comprador.
  - https://apnews.com/article/cuba-fuel-crisis-electric-tricycles-fa75dc2aca5b78dac90b1e86c7c762b1 ⚠️

## 4. Legalidad = 0.10 (marco legal cubano)

- **Resolución 47 de 2026 del Ministerio del Transporte** (Gaceta Oficial,
  4-ago-2026): homologación/inscripción de ciclomotores, motocicletas y
  **triciclos** armados por partes y piezas; exige acreditar origen legal de
  componentes y adquisición.
  - https://cubatramite.com/homologacion-inscripcion-o-reinscripcion-de-forma-excepcional-de-vehiculos-de-motor-ensamblados-por-partes-y-piezas/

- **Régimen excepcional de licencias temporales** (MINTRAN) para vehículos
  eléctricos **sin matrícula**: 1 año de vigencia, hasta diciembre de 2026;
  en La Habana alcance provincial; requiere acreditar legalidad + licencia
  categoría A.
  - http://agendaeconomica.cubadebate.cu/establecen-regimen-excepcional-para-otorgar-licencias-de-transporte-a-duenos-de-vehiculos-electricos-sin-matricula/
  - https://www.canaleducativo.icrt.cu/cuba-habilita-licencias-temporales-para-motos-y-triciclos-electricos-sin-matricula-hasta-diciembre-de-2026/
  - https://www.cubanet.org/regimen-autoriza-licencias-temporales-para-motos-y-triciclos-electricos-sin-matricula/ ⚠️ (no respondió desde la terminal)

- **Lectura del peso (0.10):** criterio *condicionante* (sin legalidad el
  vehículo puede quedar fuera de servicio), no decisivo del ranking.

## 5. Repuestos = 0.05 (peso menor)

- Evidencia externa débil — declarar como **juicio del equipo**, ya expuesto en
  Limitaciones (`repuestos_proxy` activo en 1 de ~35 modelos).
- Apoyo indirecto: **ISAHP 2022** (mismo PDF del punto 1): dentro de los
  "pains" del AHP, *Frequent repairs* = **0.05** y *Service and maintenance
  costs* = 0.23 — las reparaciones tienen peso bajo frente al costo en la
  decisión de compra.

---

## Justificación metodológica (página Método del reporte)

| Decisión del proyecto | Referencia |
|---|---|
| Pesos normalizados que suman 1.0 + normalización intra-propulsión | Práctica estándar MCDM; Saaty (1990), *The Analytic Hierarchy Process*, McGraw-Hill; Trung & Ersoy (2025) |
| Análisis de sensibilidad de pesos (±25%) | Niu et al. (2024), IEEE Access 12:27931–27946 |
| Orden precio > autonomía > carga | Hidrue et al. (2011); Hong et al. (2024) |
| Declarar cobertura (`n_criterios`) y datos ausentes | Transparencia de criterios MCDM (Trung & Ersoy, 2025) |

**Pendiente sugerido:** ejecutar en `analisis.py` el análisis de sensibilidad
(pesos ±25%) para demostrar que los podios no cambian.
