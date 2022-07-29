# SMEAR API Tools

This project contains functions that help interacting with the SmartSMEAR API.

## Installation

```python
pip install smear-api-tools
```

## [Documentation](https://jlpl.github.io/smear-api-tools/)

## Usage

### Example 1
Download DMPS data from Hyytiälä field station for each day in May, 2018

```python
import pandas as pd
from smear_api_tools import getDmpsData

may2018 = pd.date_range(start='2018-05-01',end='2018-05-31')
v = getDmpsData(station='HYY',dates=may2018)
```

### Example 2
List all variables that contain the term "SO2" in the database and write them to a file.

```python
import pandas as pd
from smear_api_tools import listAllData

listAllData("SO2").to_csv("all_so2_data.csv")
```

### Example 3
Download number concentration between 3 nm and 200 nm from the urban measurement station in Kumpula for the year 2021.

```python
import pandas as pd
from smear_api_tools import getConcData

c = getConcData(station='KUM',dp1=3e-9,dp2=200e-9,start='2021-01-31',end='2021-12-31')
```

### Example 4
Download condensation sink from Värriö research station between `2013-07-01` and
`2013-07-05`

```python
import pandas as pd
from smear_api_tools import getCS

cs = getCS(station='VAR',start="2013-07-01",end="2013-07-05")
```

## Resources

Junninen, H., Lauri, A., Keronen, P., Aalto, P., Hiltunen, V., Hari, P., Kulmala, M. 2009. Smart-SMEAR: on-line data exploration and visualization tool for SMEAR stations. Boreal Environment Research 14, 447–457.

https://smear.avaa.csc.fi/
