# FIREGUARD X — Data Dictionary

| Column Name | Type | Unit | Range in Dataset | Description |
| :--- | :--- | :--- | :--- | :--- |
| `day` | Integer | Day of month | 1 – 31 | Calendar day of observation |
| `month` | Integer | Month (6–9) | 6 – 9 | Month of observation (June to September) |
| `year` | Integer | Year | 2012 | Observation year |
| `Temperature` | Float | °C | 22.0 – 42.0 | Max ambient daily air temperature |
| `RH` | Float | % | 21.0 – 90.0 | Relative humidity percentage |
| `Ws` | Float | km/h | 6.0 – 29.0 | Surface wind velocity |
| `Rain` | Float | mm | 0.0 – 16.8 | Daily accumulated precipitation |
| `FFMC` | Float | Unitless | 28.6 – 96.0 | Fine Fuel Moisture Code (litter dryness) |
| `DMC` | Float | Unitless | 1.1 – 65.9 | Duff Moisture Code (moderately deep organic layers) |
| `DC` | Float | Unitless | 7.0 – 220.4 | Drought Code (deep organic layers and heavy logs) |
| `ISI` | Float | Unitless | 0.0 – 18.5 | Initial Spread Index (wind + surface fuel ignition) |
| `BUI` | Float | Unitless | 1.1 – 68.0 | Buildup Index (total fuel available for burning) |
| `FWI` | Float | Unitless | 0.0 – 31.1 | Fire Weather Index (numerical fire intensity rating) |
| `Region` | Integer | Binary | 0 or 1 | 0: Bejaia Region, 1: Sidi Bel-abbes Region |
| `Classes` | String | Categorical | `fire`, `not fire` | Ground-truth wildfire occurrence |
| `temp_rh_ratio` | Float | Derived | 0.24 – 2.00 | Engineered: Temperature / Relative Humidity |
| `dryness_index` | Float | Derived | 2.5 – 33.1 | Engineered: Atmospheric evapotranspiration drying index |
| `wind_temp_interaction` | Float | Derived | 132.0 – 975.0 | Engineered: Ws * Temperature advective thermal indicator |
| `rain_deficit` | Float | Derived | 0.059 – 10.0 | Engineered: Inverse precipitation index |
| `ffmc_isi_ratio` | Float | Derived | 0.0 – 0.21 | Engineered: Rate of spread relative to fine fuel moisture |
