# Resumen de los pesos del scoring

Pesos aprobados para el scoring de "Mejor Opción" (suman 1.0), aplicados en `codes/analisis.py` y mostrados en `reporte/pages/2\_Metodo.py`. A continuación se explica cada campo por separado e indicando en qué documento del repositorio y en qué parte específica de ese documento está justificado. Los enlaces externos citados se listan al final con su número de referencia.

## Precio — peso 0.40 (Menor = mejor)

El criterio de mayor peso: el triciclo es una inversión grande (US$2.000–4.500) que reemplaza al transporte público en la crisis energética cubana.

- `Data/fuentes\_justificacion.md`, sección "1. Precio = 0.40 (peso dominante)": Niu, X.; Song, Y.; Zhu, H. (2024), *Data-Driven Decision Aids for Purchasing* *Battery Electric Vehicles Based on PROMETHEE-II Methodology*, IEEE Access, vol. 12, pp. 27931–27946, asigna al criterio precio un peso de 0.417 y varía ese peso ±25% en su análisis de sensibilidad (muy cercano a nuestro 0.40) \[1\]. Además, el modelo AHP de ISAHP 2022 (Indonesia) sitúa el dolor dominante en el alza de precios de combustible con local priority 0.40, y la ganancia dominante en *Affordability* (0.45) \[2\]. El contexto cubano (magnitud del gasto) se apoya en AP News sobre la crisis de combustible y los triciclos eléctricos \[3\].

## Autonomía — peso 0.25 (Mayor = mejor)

Segundo criterio: distancia recorrible con una carga, decisiva para un vehículo de trabajo que opera todo el día.

- `Data/fuentes\_justificacion.md`, sección "2. Autonomía = 0.25 (segundo)": Hidrue, M.K.; Parsons, G.R.; Kempton, W.; Gardner, M.P. (2011), *Willingness to pay for electric vehicles and their attributes*, Resource and Energy Economics, 33(3), 686–705 (n=3.029), concluye textualmente que "Driving range, fuel cost savings, and charging time led in importance to respondents" \[4\]\[5\]. Hong, X. et al. (2024), en un experimento de elección en Shandong (China), recopila disposición a pagar por autonomía de US$14,5–151/km adicional (Hackbarth & Madlener) y CNY587/km (Qian et al.); la autonomía tiene la mayor disposición a pagar tras la garantía \[6\].

## Carga — peso 0.20 (Mayor = mejor)

Tercer criterio: capacidad de carga útil, que en el contexto cubano equivale a capacidad de ingreso del comprador (el triciclo es vehículo de trabajo).

- `Data/fuentes\_justificacion.md`, sección "3. Carga = 0.20 (tercero)": Trung, D.D.; Ersoy, N.; Mai, N.T.; Thinh, H.X. (2025), *Applying MCDM* *methods for electric vehicle selection: a comparative study between CRADIS* *and PIV methods*, Journal of Applied Engineering Science, 23(2), 345–358, tabla 1 con 20 estudios MCDM de selección de vehículos eléctricos: precio, autonomía, vida de batería y tiempo de carga son los criterios más usados, y espacio de carga/almacenamiento aparece en los estudios de uso comercial \[7\]\[8\]. También documenta que el método de ponderación cambia los rankings, lo que justifica el análisis de sensibilidad. El contexto de uso en Cuba se apoya en AP News \[3\].

## Legalidad — peso 0.10 (1 = menciona legalidad)

Criterio condicionante: sin legalidad el vehículo puede quedar fuera de servicio, pero no es decisivo del ranking.

- `Data/fuentes\_justificacion.md`, sección "4. Legalidad = 0.10 (marco legal cubano)": Resolución 47 de 2026 del Ministerio del Transporte (Gaceta Oficial, 4-ago-2026) sobre homologación/inscripción de ciclomotores, motocicletas y triciclos armados por partes y piezas, que exige acreditar origen legal de componentes y adquisición \[9\]; régimen excepcional de licencias temporales (MINTRAN) para vehículos eléctricos sin matrícula, de 1 año de vigencia hasta diciembre de 2026, con alcance provincial en La Habana, verificado en cubadebate \[10\], canaleducativo.icrt.cu \[11\] y cubanet.org \[12\]. La lectura del peso (0.10) como criterio condicionante y no decisivo está en la misma sección.

## Repuestos — peso 0.05 (1 = \>1 fuente)

Criterio de menor peso: evidencia externa débil, declarado como juicio del equipo.

- `Data/fuentes\_justificacion.md`, sección "5. Repuestos = 0.05 (peso menor)": la evidencia externa es débil; apoyo indirecto en ISAHP 2022 (mismo PDF del punto 1) \[2\], donde dentro de los "pains" del AHP, *Frequent repairs* = 0.05 y *Service and maintenance costs* = 0.23, es decir, las reparaciones tienen peso bajo frente al costo en la decisión de compra. También se anota que el proxy está activo en 1 de ~35 modelos.

## Enlaces referenciados

\[1\] -\> [https://ieeexplore.ieee.org/document/10440069](https://ieeexplore.ieee.org/document/10440069) 

\[2\] -\> [http://www.isahp.org/uploads/051\_003.pdf](http://www.isahp.org/uploads/051_003.pdf) 

\[3\] -\> [https://apnews.com/article/cuba-fuel-crisis-electric-tricycles-fa75dc2aca5b78dac90b1e86c7c762b1](https://apnews.com/article/cuba-fuel-crisis-electric-tricycles-fa75dc2aca5b78dac90b1e86c7c762b1) 

\[4\] -\> [https://ideas.repec.org/a/eee/resene/v33y2011i3p686-705.html](https://ideas.repec.org/a/eee/resene/v33y2011i3p686-705.html) 

\[5\] -\> [https://www1.udel.edu/V2G/resources/HidrueEtAl-Pay-EV-Attributes-correctedProof.pdf](https://www1.udel.edu/V2G/resources/HidrueEtAl-Pay-EV-Attributes-correctedProof.pdf) 

\[6\] -\> [https://www.pjoes.com/pdf-184151-112590](https://www.pjoes.com/pdf-184151-112590) 

\[7\] -\> [https://doi.org/10.5937/jaes0-56793](https://doi.org/10.5937/jaes0-56793) 

\[8\] -\> [https://www.engineeringscience.rs/articles/applying-mcdm-methods-for-electric-vehicle-selection-a-comparative-study-between-cradis-and-piv-methods](https://www.engineeringscience.rs/articles/applying-mcdm-methods-for-electric-vehicle-selection-a-comparative-study-between-cradis-and-piv-methods) 

\[9\] -\> [https://cubatramite.com/homologacion-inscripcion-o-reinscripcion-de-forma-excepcional-de-vehiculos-de-motor-ensamblados-por-partes-y-piezas/](https://cubatramite.com/homologacion-inscripcion-o-reinscripcion-de-forma-excepcional-de-vehiculos-de-motor-ensamblados-por-partes-y-piezas/) 

\[10\] -\> [http://agendaeconomica.cubadebate.cu/establecen-regimen-excepcional-para-otorgar-licencias-de-transporte-a-duenos-de-vehiculos-electricos-sin-matricula/](http://agendaeconomica.cubadebate.cu/establecen-regimen-excepcional-para-otorgar-licencias-de-transporte-a-duenos-de-vehiculos-electricos-sin-matricula/) 

\[11\] -\> [https://www.canaleducativo.icrt.cu/cuba-habilita-licencias-temporales-para-motos-y-triciclos-electricos-sin-matricula-hasta-diciembre-de-2026/](https://www.canaleducativo.icrt.cu/cuba-habilita-licencias-temporales-para-motos-y-triciclos-electricos-sin-matricula-hasta-diciembre-de-2026/) 

\[12\] -\> [https://www.cubanet.org/regimen-autoriza-licencias-temporales-para-motos-y-triciclos-electricos-sin-matricula/](https://www.cubanet.org/regimen-autoriza-licencias-temporales-para-motos-y-triciclos-electricos-sin-matricula/)

