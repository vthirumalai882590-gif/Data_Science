# FIREGUARD X — Machine Learning Methodology & Data Science Documentation

## 1. Problem Formulation & Academic Objectives
Forest wildfires represent complex, catastrophic ecological and socio-economic hazards driven by non-linear interactions among meteorological factors, atmospheric vapor deficits, and vegetation fuel desiccation. 

The primary objective of **FIREGUARD X** is to construct an explainable, reliable, and mathematically grounded decision-support system that answers:
1. **Where** is wildfire vulnerability elevated? (Spatial Risk Engine)
2. **Why** is the risk elevated? (Explainable AI via localized Shapley Attributions)
3. **How** might risk vary under prospective climatic shifts? (Counterfactual What-If Simulator)
4. **How** could conditions evolve diurnally? (Thermodynamic Trajectory Forecasting)
5. **Are** current microclimate combinations unprecedented? (Isolation Forest Environmental Anomaly Detection)
6. **What** are the educational physics of fire propagation? (Directional Cellular Automaton Simulator)

---

## 2. Dataset Provenance & Inspection
- **Source**: UCI Machine Learning Repository — *Algerian Forest Fires Dataset* (Faroudja ABID et al.).
- **Observation Period**: June 2012 to September 2012 (summer fire season).
- **Regions**:
  - *Bejaia Region*: North-eastern Algeria (Mediterranean maritime climate, dense mountain cork oak and pine forests).
  - *Sidi Bel-abbes Region*: North-western Algeria (semi-arid steppe transition with hot continental winds).
- **Dataset Scale**: 243 validated observations across 15 initial attributes.
- **Target Distribution**:
  - `fire` (Class 1): 137 records (56.4%)
  - `not fire` (Class 0): 106 records (43.6%)
  - Well-balanced distribution avoiding severe class collapse; stratified sampling utilized throughout.

---

## 3. Preprocessing Pipeline & Data Cleaning
1. **Header Normalization**: Stripped anomalous leading/trailing whitespace across column names and class categories.
2. **Numeric Type Enforcement**: Coerced string fields (`Temperature`, `RH`, `Ws`, `Rain`, `FFMC`, `DMC`, `DC`, `ISI`, `BUI`, `FWI`) into rigorous floating-point representations.
3. **Missing Value Imputation**: Continuous attributes audited; verified complete integrity with median imputation fallback for external inference.
4. **Stratified Splitting**: 80% Training partition (194 instances), 20% Holdout Testing partition (49 instances), stratified by target class with fixed random state ($seed = 42$) for strict reproducibility.
5. **Standardization**: `StandardScaler` applied across numerical and engineered features to prevent gradient dominance in linear and distance models.

---

## 4. Domain Feature Engineering
In addition to baseline meteorological inputs and Canadian Fire Weather Index components, the following domain features were engineered:

1. **Temperature-to-Relative-Humidity Ratio (`temp_rh_ratio`)**:
   $$\text{temp\_rh\_ratio} = \frac{\text{Temperature}}{\text{RH} + 10^{-4}}$$
   *Rationale*: Hot dry air rapidly desiccates dead surface litter. Ratios exceeding 0.8 signal critical atmospheric thirst.

2. **Atmospheric Dryness Index (`dryness_index`)**:
   $$\text{dryness\_index} = \frac{(100 - \text{RH}) \times \text{Temperature}}{100.0}$$
   *Rationale*: Directly captures evapotranspiration pressure on fine living and dead fuels.

3. **Wind-Temperature Interaction (`wind_temp_interaction`)**:
   $$\text{wind\_temp\_interaction} = \text{Ws} \times \text{Temperature}$$
   *Rationale*: Convective heat advection enhances combustion rate and supplies oxygen to incipient flame fronts.

4. **Rain Deficit Indicator (`rain_deficit`)**:
   $$\text{rain\_deficit} = \frac{1}{\text{Rain} + 0.1}$$
   *Rationale*: Rain exerts an exponential suppression effect; prolonged zero-rain episodes produce steep risk spikes.

5. **FFMC-to-ISI Propagation Dynamics (`ffmc_isi_ratio`)**:
   $$\text{ffmc\_isi\_ratio} = \frac{\text{ISI}}{\text{FFMC} + 10^{-4}}$$
   *Rationale*: Ratio of rate of spread to fine fuel moisture code.

---

## 5. Machine Learning Architectures & Comparison
Four candidate architectures were trained and evaluated on identical stratified partitions:

| Model Architecture | Test Accuracy | Precision | Recall (Sensitivity) | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression (L2)** | 95.92% | 96.43% | 96.43% | 0.9643 | 0.9932 |
| **Decision Tree (max_depth=5)** | 93.88% | 90.32% | 100.00% | 0.9492 | 0.9949 |
| **Random Forest (150 trees)** | 93.88% | 90.32% | 100.00% | 0.9492 | 1.0000 |
| **XGBoost (Champion)** | **95.92%** | **93.33%** | **100.00%** | **0.9655** | **0.9983** |

### Evaluation Criteria & Trade-off Analysis:
In operational wildfire surveillance, **False Negatives** (failing to predict an active fire) carry catastrophic risk including loss of life, wildlife, and forest canopy. Conversely, **False Positives** merely trigger precautionary observation. 
- **XGBoost** achieved a **100.00% Recall** on holdout testing (0 False Negatives) combined with the highest **F1-Score (0.9655)** and **ROC-AUC (0.9983)**, making it the champion model for primary production serving.

---

## 6. Composite Risk Index Formulation
The platform distinguishes raw statistical class probability from the calibrated **Fire Risk Score (0–100)**:
$$\text{Base Score} = P(\text{Fire} \mid X) \times 100$$
$$\text{Atmospheric Vulnerability} = \left(\frac{\text{Temp}}{45}\right) \times \left(1 - \frac{\text{RH}}{100}\right) \times \min\left(1.25, 1 + \frac{\text{Ws}}{100}\right) \times \text{RainFactor}$$
$$\text{Risk Score} = 0.80 \times \text{Base Score} + 0.20 \times (\text{Atmospheric Vulnerability} \times 100)$$

### Standardized 5-Tier Classification:
- **0–20**: `LOW` (Green)
- **21–40**: `MODERATE` (Yellow)
- **41–60**: `ELEVATED` (Amber)
- **61–80**: `HIGH` (Orange)
- **81–100**: `CRITICAL` (Dark Red / Purple)

---

## 7. Explainable AI (SHAP)
FIREGUARD X utilizes **SHAP (SHapley Additive exPlanations)** grounded in cooperative game theory to quantify the exact marginal contribution of each environmental parameter for every individual prediction:
$$f(x) = \phi_0 + \sum_{i=1}^{M} \phi_i(x)$$
Each feature attribution includes:
- **Feature Name & Value**: (e.g. `Temperature: 38°C`)
- **Contribution Value**: (e.g. `+0.21`)
- **Directional Impact**: (`Increased risk` vs `Decreased risk`)
- **Plain Language Narrative**: Contextual synthesis explaining the combined effect.

---

## 8. Environmental Anomaly Detection
An unsupervised **Isolation Forest** (contamination = 8%) is fitted on historical multi-variate environmental distributions. Coupled with empirical Z-score tracking, it identifies compound climate anomalies (e.g., extreme heatwaves accompanied by record humidity deficits and high wind shear) that deviate significantly from historical norms.

---

## 9. Academic Limitations & Responsible AI
1. **Probabilistic Nature**: Risk scores represent statistical likelihood under observed weather regimes, not deterministic certainty.
2. **Geographic Specificity**: Models were trained on Mediterranean and North African forest ecosystems; transferability to boreal or tropical rainforests requires local fine-tuning.
3. **Educational Fire Spread Simulator**: The 2D cellular automaton is intended exclusively for pedagogical demonstration of wind/dryness vectors and must **never** be used for tactical life-safety evacuation routing.
