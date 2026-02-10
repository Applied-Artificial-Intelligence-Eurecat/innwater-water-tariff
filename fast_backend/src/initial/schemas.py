from typing import List, Optional

from pydantic import BaseModel, Field, EmailStr

from src.core.models import StatusEnum


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="User email address", example="user@example.com")
    password: str = Field(..., description="User password", example="strongpassword123")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "strongpassword123"
            }
        }


# Add examples for Population Model
class PopulationModel(BaseModel):
    bd: str = Field(
        ...,
        description="Distribution type for population (e.g., 'lognormal', 'normal', 'uniform')",
        example="lognormal"
    )
    original_datasource: bool = Field(
        ...,
        default_factory=lambda: True,
        description="Use the original datasource for the population",
        example=False
    )
    eps: int = Field(
        ...,
        description="Population size parameter",
        example=10000
    )
    std: float = Field(
        ...,
        description="Standard deviation parameter",
        example=0.5
    )

    class Config:
        json_schema_extra = {
            "example": {
                "bd": "lognormal",
                "eps": 10000,
                "std": 0.5
            }
        }


# Water service models with examples
class WaterServiceCostModel(BaseModel):
    fixed_costs: float = Field(
        ...,
        alias="couts_fixes",
        description="Fixed costs for the water service",
        example=100000.0
    )
    variable_costs: float = Field(
        ...,
        alias="couts_variables",
        description="Variable costs per unit",
        example=1.2
    )
    number_of_subscribers: int = Field(
        ...,
        alias="nombre_abonnes",
        description="Number of subscribers to the service",
        example=5000
    )

    @property
    def tbse_base_prix(self):
        cfm = self.fixed_costs / self.number_of_subscribers
        f_tbse = cfm / 4
        return f_tbse

    class Config:
        populate_by_name = True
        validate_by_name = True
        json_schema_extra = {
            "example": {
                "fixed_costs": 100000.0,
                "variable_costs": 1.2,
                "number_of_subscribers": 5000
            }
        }


# Environmental costs model with examples
class EnvironmentalModel(BaseModel):
    fixed_costs_per_year: float = Field(
        ...,
        alias="couts_fixes_par_an",
        description="Annual fixed environmental costs",
        example=25000.0
    )
    average_variable_cost: float = Field(
        ...,
        alias="couts_variable_moyen",
        description="Average variable environmental cost per unit",
        example=0.3
    )

    class Config:
        populate_by_name = True
        validate_by_name = True
        json_schema_extra = {
            "example": {
                "fixed_costs_per_year": 25000.0,
                "average_variable_cost": 0.3
            }
        }


# Tax model for water with examples
class TaxModel(BaseModel):
    vat: float = Field(
        ...,
        alias="tva",
        description="Value-added tax percentage",
        example=5.5
    )
    fees: float = Field(
        ...,
        alias="redevances",
        description="Additional fees per unit",
        example=0.25
    )

    class Config:
        populate_by_name = True
        validate_by_name = True
        json_schema_extra = {
            "example": {
                "vat": 5.5,
                "fees": 0.25
            }
        }


class TaxSectionModel(BaseModel):
    drinking_water: TaxModel = Field(..., alias="eau_potable")
    sanitation: TaxModel = Field(..., alias="assainissement")

    class Config:
        populate_by_name = True
        validate_by_name = True
        json_schema_extra = {
            "example": {
                "drinking_water": {
                    "vat": 5.5,
                    "fees": 0.35
                },
                "sanitation": {
                    "vat": 10.0,
                    "fees": 0.25
                }
            }
        }


# Social data model with examples
class SocialDataModel(BaseModel):
    threshold_par: int = Field(
        ...,
        alias="seuil_par",
        description="Threshold for basic needs per person",
        example=550
    )
    threshold_car: int = Field(
        ...,
        alias="seuil_car",
        description="Threshold for car-related expenses",
        example=3300
    )
    poverty: float = Field(
        ...,
        alias="pauvrete",
        description="Poverty rate in percentage",
        example=14.0
    )

    class Config:
        populate_by_name = True
        validate_by_name = True
        json_schema_extra = {
            "example": {
                "threshold_par": 550,
                "threshold_car": 3300,
                "poverty": 14.0,
            }
        }


# Combined primitives model
class PrimitivesModel(BaseModel):
    drinking_water: WaterServiceCostModel = Field(..., alias="ep")
    sanitation: WaterServiceCostModel = Field(..., alias="assainissement")
    environment: EnvironmentalModel = Field(..., alias="environnement")
    taxation: TaxSectionModel = Field(..., alias="fiscalite")
    social_data: SocialDataModel = Field(..., alias="donnees_sociales")

    class Config:
        populate_by_name = True
        validate_by_name = True


class ConsumptionThresholds(BaseModel):
    threshold: float = Field(
        ...,
        alias="seuil",
        description="Consumption threshold in cubic meters",
        example=50.0
    )
    price: float = Field(
        ...,
        alias="prix",
        description="Price per cubic meter (€/m3)",
        example=1.2
    )

    class Config:
        populate_by_name = True
        validate_by_name = True
        json_schema_extra = {
            "example": {
                "threshold": 50.0,
                "price": 1.2
            }
        }


class TariffSectionModel(BaseModel):
    subscription: float = Field(
        ...,
        alias="abonnement",
        description="Annual subscription fee",
        example=40.0
    )
    usage_tiers: List[ConsumptionThresholds] = Field(
        ...,
        description="List of consumption thresholds and their associated prices"
    )

    class Config:
        populate_by_name = True
        validate_by_name = True
        json_schema_extra = {
            "example": {
                "subscription": 40.0,
                "usage_tiers": [
                    {
                        "threshold": 50.0,
                        "price": 1.2
                    },
                    {
                        "threshold": 100.0,
                        "price": 1.5
                    },
                    {
                        "threshold": 200.0,
                        "price": 2.0
                    }
                ]
            }
        }


class TariffModel(BaseModel):
    drinking_water: TariffSectionModel = Field(..., alias="ep")
    sanitation: TariffSectionModel = Field(..., alias="assainissement")

    class Config:
        populate_by_name = True
        validate_by_name = True


class CoefficientModel(BaseModel):
    a0: float = Field(..., description="Base coefficient", example=120.0)
    a1: float = Field(..., description="Price elasticity coefficient", example=-0.3)
    a2: float = Field(..., description="Income coefficient", example=0.2)
    a3: float = Field(..., description="Household size coefficient", example=0.4)
    a4: float = Field(..., description="Age coefficient", example=0.1)
    a5: float = Field(..., description="Education coefficient", example=0.05)
    a6: float = Field(..., description="Climate coefficient", example=0.02)

    class Config:
        json_schema_extra = {
            "example": {
                "a0": 120.0,
                "a1": -0.3,
                "a2": 0.2,
                "a3": 0.4,
                "a4": 0.1,
                "a5": 0.05,
                "a6": 0.02
            }
        }


class DemandModel(BaseModel):
    coefficients: CoefficientModel
    k: float = Field(..., description="Scaling factor", example=1)
    has_pool: bool = Field(..., alias="piscine", description="Whether the household has a swimming pool", example=False)
    has_garden: bool = Field(..., alias="jardin", description="Whether the household has a garden", example=True)

    class Config:
        populate_by_name = True
        validate_by_name = True


class LaunchModel(BaseModel):
    periods: int = Field(
        ...,
        alias="periodes",
        description="Number of simulation periods",
        example=10
    )
    simulation_name: str = Field(
        ...,
        alias="nom_simulation",
        description="Name of the simulation",
        example="Water Tariff Simulation 2025"
    )

    class Config:
        populate_by_name = True
        validate_by_name = True
        json_schema_extra = {
            "example": {
                "periods": 10,
                "simulation_name": "Water Tariff Simulation 2025"
            }
        }


# Main simulation payload model with a complete example
class SimulationPayload(BaseModel):
    primitives: PrimitivesModel
    population: PopulationModel
    tariff: TariffModel = Field(..., alias="tarification")
    demand: DemandModel = Field(..., alias="demande")
    launch: LaunchModel

    @property
    def sanitation_base_tva_per_unit_of_service(self):
        return self.tariff.sanitation.subscription * (self.primitives.taxation.sanitation.vat / 100)

    @property
    def epa_base_tva_per_unit_of_service(self):
        return self.potable_water_base_tva_per_unit_of_service + self.sanitation_base_tva_per_unit_of_service

    @property
    def sanitation_fees_tva_per_unit_of_service(self):
        res = []
        for price in self.sanitation_prix_tiers_tva:
            res.append(price * self.primitives.taxation.sanitation.vat / 100)
        return res

    @property
    def sanitation_prix_base_ttc(self):
        return self.sanitation_base_tva_per_unit_of_service + self.tariff.sanitation.subscription

    @property
    def epa_prix_base_ttc(self):
        return self.potable_water_prix_base_ttc + self.sanitation_prix_base_ttc

    @property
    def sanitation_prix_tiers_ttc(self):
        res = []
        for price in self.sanitation_prix_tiers_tva:
            res.append(price * self.primitives.taxation.sanitation.vat / 100 + price)
        return res

    @property
    def sanitation_nordin_tiers(self):
        res = [0]
        last_prix = self.sanitation_prix_tiers_ttc[0]
        for prix_tier, tier in zip(self.sanitation_prix_tiers_ttc[1:], self.tariff.sanitation.usage_tiers[1:]):
            res.append(res[-1] + (prix_tier - last_prix) * tier.threshold)
            last_prix = prix_tier
        return res

    @property
    def potable_water_nordin_tiers(self):
        res = [0]
        last_prix = self.potable_water_prix_tiers_ttc[0]
        for prix_tier, tier in zip(self.potable_water_prix_tiers_ttc[1:], self.tariff.drinking_water.usage_tiers[1:]):
            res.append(res[-1] + (prix_tier - last_prix) * tier.threshold)
            last_prix = prix_tier
        return res

    @property
    def potable_water_base_tva_per_unit_of_service(self):
        return self.tariff.drinking_water.subscription * (self.primitives.taxation.drinking_water.vat / 100)

    @property
    def potable_water_fees_tva_per_unit_of_service(self):
        res = []
        for price in self.potable_water_prix_tiers_tva:
            res.append(price * self.primitives.taxation.drinking_water.vat / 100)
        return res

    @property
    def potable_water_prix_base_ttc(self):
        return self.potable_water_base_tva_per_unit_of_service + self.tariff.drinking_water.subscription

    @property
    def potable_water_prix_tiers_ttc(self):
        res = []
        for price in self.potable_water_prix_tiers_tva:
            res.append(price * self.primitives.taxation.drinking_water.vat / 100 + price)
        return res

    @property
    def potable_water_prix_tiers_tva(self):
        res = []
        for prix_tier in self.tariff.drinking_water.usage_tiers:
            res.append(prix_tier.price + self.primitives.taxation.drinking_water.fees)
        return res

    @property
    def sanitation_prix_tiers_tva(self):
        res = []
        for prix_tier in self.tariff.sanitation.usage_tiers:
            res.append(prix_tier.price + self.primitives.taxation.sanitation.fees)
        return res

    @property
    def tbse_ep_variable_prix(self):
        return self.primitives.taxation.drinking_water.fees + self.primitives.drinking_water.variable_costs

    @property
    def tbse_a_variable_prix(self):
        return self.primitives.taxation.sanitation.fees + self.primitives.sanitation.variable_costs

    @property
    def tbse_potable_water_base_prix(self):
        cfm = self.primitives.drinking_water.fixed_costs / self.primitives.drinking_water.number_of_subscribers
        subscription = cfm / 4
        subscription += self.primitives.environment.fixed_costs_per_year
        montant_tva_per_unite_de_service = self.primitives.taxation.drinking_water.vat / 100 * subscription
        return montant_tva_per_unite_de_service + subscription

    @property
    def tbse_potable_water_variable_prix(self):
        prix_h_tva = self.primitives.drinking_water.variable_costs + self.primitives.taxation.drinking_water.fees
        montant_tva_per_unite_de_service = self.primitives.taxation.drinking_water.vat / 100 * prix_h_tva
        return prix_h_tva + montant_tva_per_unite_de_service

    @property
    def tbse_sanitation_base_prix(self):
        cfm = self.primitives.sanitation.fixed_costs / self.primitives.sanitation.number_of_subscribers
        subscription = cfm / 4
        subscription += self.primitives.environment.fixed_costs_per_year
        montant_tva_per_unite_de_service = self.primitives.taxation.sanitation.vat / 100 * subscription
        return subscription + montant_tva_per_unite_de_service

    @property
    def tbse_sanitation_variable_prix(self):
        prix_h_tva = self.primitives.sanitation.variable_costs + self.primitives.taxation.sanitation.fees
        montant_tva_per_unite_de_service = self.primitives.taxation.sanitation.vat / 100 * prix_h_tva
        return prix_h_tva + montant_tva_per_unite_de_service

    class Config:
        populate_by_name = True
        validate_by_name = True
        json_schema_extra = {
            "example": {
                "primitives": {
                    "drinking_water": {
                        "fixed_costs": 100000.0,
                        "variable_costs": 1.2,
                        "number_of_subscribers": 5000
                    },
                    "sanitation": {
                        "fixed_costs": 80000.0,
                        "variable_costs": 0.9,
                        "number_of_subscribers": 4800
                    },
                    "environment": {
                        "fixed_costs_per_year": 25000.0,
                        "average_variable_cost": 0.3
                    },
                    "taxation": {
                        "drinking_water": {
                            "vat": 5.5,
                            "fees": 0.35
                        },
                        "sanitation": {
                            "vat": 10.0,
                            "fees": 0.25
                        }
                    },
                    "social_data": {
                        "threshold_par": 550,
                        "threshold_car": 3300,
                        "poverty": 14.0,
                    }
                },
                "population": {
                    "bd": "lognormal",
                    "eps": 10000,
                    "std": 0.5
                },
                "tariff": {
                    "drinking_water": {
                        "subscription": 40.0,
                        "usage_tiers": [
                            {
                                "threshold": 50.0,
                                "price": 1.2
                            },
                            {
                                "threshold": 100.0,
                                "price": 1.5
                            },
                            {
                                "threshold": 200.0,
                                "price": 2.0
                            }
                        ]
                    },
                    "sanitation": {
                        "subscription": 30.0,
                        "usage_tiers": [
                            {
                                "threshold": 50.0,
                                "price": 0.8
                            },
                            {
                                "threshold": 100.0,
                                "price": 1.0
                            },
                            {
                                "threshold": 200.0,
                                "price": 1.3
                            }
                        ]
                    }
                },
                "demand": {
                    "coefficients": {
                        "a0": 120.0,
                        "a1": -0.3,
                        "a2": 0.2,
                        "a3": 0.4,
                        "a4": 0.1,
                        "a5": 0.05,
                        "a6": 0.02
                    },
                    "k": 1,
                    "has_pool": False,
                    "has_garden": True
                },
                "launch": {
                    "periods": 10,
                    "simulation_name": "Water Tariff Simulation 2025"
                }
            }
        }


class GetSimulationPayload(SimulationPayload):
    id: int
    status: str

    class Config:
        populate_by_name = True
        validate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "1234567890",
                "status": str(StatusEnum.first_evaluation),
                "primitives": {
                    "drinking_water": {
                        "fixed_costs": 100000.0,
                        "variable_costs": 1.2,
                        "number_of_subscribers": 5000
                    },
                    "sanitation": {
                        "fixed_costs": 80000.0,
                        "variable_costs": 0.9,
                        "number_of_subscribers": 4800
                    },
                    "environment": {
                        "fixed_costs_per_year": 25000.0,
                        "average_variable_cost": 0.3
                    },
                    "taxation": {
                        "drinking_water": {
                            "vat": 5.5,
                            "fees": 0.35
                        },
                        "sanitation": {
                            "vat": 10.0,
                            "fees": 0.25
                        }
                    },
                    "social_data": {
                        "threshold_par": 550,
                        "threshold_car": 3300,
                        "poverty": 14.0,
                    }
                },
                "population": {
                    "bd": "lognormal",
                    "eps": 10000,
                    "std": 0.5
                },
                "tariff": {
                    "drinking_water": {
                        "subscription": 40.0,
                        "usage_tiers": [
                            {
                                "threshold": 50.0,
                                "price": 1.2
                            },
                            {
                                "threshold": 100.0,
                                "price": 1.5
                            },
                            {
                                "threshold": 200.0,
                                "price": 2.0
                            }
                        ]
                    },
                    "sanitation": {
                        "subscription": 30.0,
                        "usage_tiers": [
                            {
                                "threshold": 50.0,
                                "price": 0.8
                            },
                            {
                                "threshold": 100.0,
                                "price": 1.0
                            },
                            {
                                "threshold": 200.0,
                                "price": 1.3
                            }
                        ]
                    }
                },
                "demand": {
                    "coefficients": {
                        "a0": 120.0,
                        "a1": -0.3,
                        "a2": 0.2,
                        "a3": 0.4,
                        "a4": 0.1,
                        "a5": 0.05,
                        "a6": 0.02
                    },
                    "k": 1,
                    "has_pool": False,
                    "has_garden": True
                },
                "launch": {
                    "periods": 10,
                    "simulation_name": "Water Tariff Simulation 2025"
                }
            }
        }


class DuplicationSchema(BaseModel):
    new_name: str
