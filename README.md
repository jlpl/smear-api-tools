# SMEAR API Tools

This project contains functions that help interacting with the SmartSMEAR API.

Latest version: 0.4.0

## Installation

```shell
pip install git+https://github.com/jlpl/smear-api-tools.git
```

## Documentation 
See [here](https://jlpl.github.io/smear-api-tools/)

## Usage

### Example 1
Download DMPS data from Hyytiälä field station for each day in May, 2018

```python
import pandas as pd
from smear_api.tools import getDmpsData

may2018 = pd.date_range(start='2018-05-01',end='2018-05-31')
v = getDmpsData(station='HYY',dates=may2018)
```

### Example 2
List all variables that contain the term "SO2" in the database and write them to a file.

```python
import pandas as pd
from smear_api.tools import listAllData

listAllData("SO2").to_csv("all_so2_data.csv")
```

## Resources

Junninen, H., Lauri, A., Keronen, P., Aalto, P., Hiltunen, V., Hari, P., Kulmala, M. 2009. Smart-SMEAR: on-line data exploration and visualization tool for SMEAR stations. Boreal Environment Research 14, 447–457.

https://smear.avaa.csc.fi/
