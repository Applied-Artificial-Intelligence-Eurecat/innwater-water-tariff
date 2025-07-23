# 1. Descriptive Statistics

## Generate chart of population

- **Endpoint: /api/affordability/general/stats/:simulation_id:**
- Description: Generate the descriptive statistics of PAR and CAR data for IBT and TBSE, related to Affordability for
  the population as a whole (all the population)
- Method: GET
- Input Schema: -
- Output Schema: GeneralStatistics

```python
from pydantic import BaseModel

class GeneralColumn(BaseModel):
    mean: float
    ...

class DifferenceColumn(BaseModel):
    mean: float
    median: float

class GeneralStatistics(BaseModel):
    par_ibt: GeneralColumn
    par_tbse: GeneralColumn
    par_delta: DifferenceColumn
    car_ibt: GeneralColumn
    car_tbse: GeneralColumn
    car_delta: DifferenceColumn
```
