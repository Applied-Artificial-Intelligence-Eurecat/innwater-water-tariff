# 1. Initialization

## Generate chart of population

- **Endpoint: api/v1/initial/population/plot**
- Description: Generate the scatter plot chart to validate the population
- Method: POST
- Input Schema: PopulationModel

```python
from pydantic import BaseModel

class PopulationModel(BaseModel):
    bd: str
    eps: int
    std: float
```
- Output: PNG image in base64

## Launch simulation

- **Endpoint: /simulation/presimulation**
- Description: Create and save the simulation
- Method: POST
- Input Schema: SimulationPayload

```python
from pydantic import BaseModel
from typing import Dict, List, Optional, Union

# Water service models
class PrimitivesCoitDuService(BaseModel):
    couts_fixes: float
    couts_variables: float
    nombre_abonnes: int


# Environmental costs model
class EnvironnementModel(BaseModel):
    couts_fixes_par_an: float
    couts_variable_moyen: float


# Tax model for water
class FiscaliteModel(BaseModel):
    tva: float
    redevances: float

class FiscaliteSectionModel(BaseModel):
    eau_potable: FiscaliteModel
    assainissement: FiscaliteModel

# TODO: ALERT! This is copied from the endpoint from above! 
class PopulationModel(BaseModel):
    bd: str
    eps: int
    std: float

# Social data model
class DonneesSocialesModel(BaseModel):
    seuil_par: int
    seuil_car: int
    pauvrete: float
    grande_pauvrete: float


# Combined primitives model
class PrimitivesModel(BaseModel):
    ep: PrimitivesCoitDuService
    assainissement: PrimitivesCoitDuService
    environnement: EnvironnementModel
    fiscalite: FiscaliteSectionModel
    donnees_sociales: DonneesSocialesModel

class ConsumptionThresholds(BaseModel):
    seuil: float
    prix: float # (€/m3)

class TarificationSectionModel(BaseModel):
    abonnement: float
    usage_tiers: List[ConsumptionThresholds]


class TarificationModel(BaseModel):
    ep: TarificationSectionModel
    assainissement: TarificationSectionModel


class CoefficientModel(BaseModel):
    a0: float
    a1: float
    a2: float
    a3: float
    a4: float
    a5: float
    a6: float

class DemandeModel(BaseModel):
    coefficients: CoefficientModel
    k: int
    piscine: bool
    jardin: bool

class LaunchModel(BaseModel):
    periodes: int
    nom_simulation: str

# Main simulation payload model
class SimulationPayload(BaseModel):
    userid: str
    primitives: PrimitivesModel
    population: PopulationModel
    tarification: TarificationModel
    demande: DemandeModel
    launch: LaunchModel
```

- Output: primary key of the simulation id created

```python
from pydantic import BaseModel


# TODO: I do not know the simulation id, is it a uuid?
class SimulationInformation(BaseModel):
    uuid: str
```

## Get pre-simulation data

- **Endpoint: /simulation/:simulation_id:/presimulation**
- Description: Get the presimulation data
- Method: GET
- Input Schema: simulation_id
- Output: SimulationPayload

## Get simulations from a user

- **Endpoint: /simulation/**
- Description: Get the presimulation data
- Method: POST
- Input Schema: 

```python
from pydantic import BaseModel

class SimulationInput(BaseModel):
    user_id: str
```

- Output: SimulationList

```python
from pydantic import BaseModel
from datetime import datetime

class SimulationList(BaseModel):
    simulation_name: str
    simulation_id: str
    date: datetime
```



# 2. TBSE Infographics and results

## TBSE Par Affordability and Standard of living

- **Endpoint: /infographics/:simulation_id:/tbse_affordability**
- Description: Generate the scatter plot chart to validate TBSE Par Affordability
- Method: GET
- Input Schema: SimulationInformation
- Output: png in base64

## Pen's Parade of basic and captive consumptions

- **Endpoint: /infographics/:simulation_id:/pens_parade**
- Description: Generate the line plot chart to validate Pen's Parade of basic and captive consumptions
- Method: Get
- Input Schema: simulation_id
- Output: png in base64

## TBSE Consumption and living standards

- **Endpoint: /infographics/:simulation_id:/tbse_consumption**
- Description: Generate the scatter plot chart to validate TBSE Consumption and living standards
- Method: Get
- Input Schema: simulation_id
- Output: png in base64

## Consumption deviations, Weifare losses and environmental cost recovery

- **Endpoint: /infographics/:simulation_id:/pens_parade**
- Description: Generate the bar plot chart to validate Consumption deviations, etc.
- Method: GET
- Input Schema: simulation_id
- Output: png in base64


# Get IBT parameters from a simulation

- **Endpoint: /simulation/:simulation_id:/ibt**
- Description: Get the IBT parameters
- Method: GET
- Input Schema: simulation_id
- Output: TarificationModel


## Change IBT

- **Endpoint: /simulation/:simulation_id:/ibt**
- Description: Change the blocking tariff regulations
- Method: PUT
- Input Schema: simulation_id in uri but TarificationModel in the payload
- Output: true or false (if it could be done or not) 200 OK 500 BAD


# 3. Small Assessment

## Apply Small Assessment

- **Endpoint: /simulation/small_assessment**
- Description: Create the small assessment, the backend must store this data to then show the results.
- Method: POST
- Input Schema: Simulation Information
- Output: true if started false if not (?) 200 OK 500 BAD

## Small Assessment status

- **Endpoint: /simulation/:simulation_id:/small_assessment/status**
- Description: Check if the small_assessment has finished
- Method: GET
- Input Schema: simulation_id
- Output: SmallAssessmentStatus

```python
from pydantic import BaseModel
from typing import Literal

class SmallAssessmentStatus(BaseModel):
    status: Literal['ongoing', 'finished', 'error']
```

## SmallAffordabilityResults

- **Endpoint: /simulation/:simulation_id:/small_assessment/affordability**
- Description: Get Affordability Data
- Method: GET
- Input Schema: simulation_id
- Output: If all ok, it must return AffordabilitySmallAssessment

```python
from pydantic import BaseModel

class AffordabilitySmallColumn(BaseModel):
    headcount_ratio: float
    app_afford_deft: float
    effec_afford_deft: float
    gini_app: float
    gini_eff: float

class AffordabilitySmallAssessment(BaseModel):
    ibt: AffordabilitySmallColumn
    tbse: AffordabilitySmallColumn
```

## SmallRexResult

- **Endpoint: /simulation/:simulation_id:/small_assessment/rex**
- Description: Get rex result
- Method: GET
- Input Schema: simulation_id
- Output: If all ok, it must return the value of rex (float)


