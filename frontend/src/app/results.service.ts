import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {environment} from 'src/environments/environment';

export interface AffordabilityColumnValues {
    ibt: number;
    tbse: number;
}

export interface AffordabilityTable {
    headcount_ratio: AffordabilityColumnValues;
    apparent_affordability_deficit: AffordabilityColumnValues;
    effective_affordability_deficit: AffordabilityColumnValues;
    gini_app: AffordabilityColumnValues;
    gini_eff: AffordabilityColumnValues;
}

// Define the structure for the consumption data
export interface IncentiveConsumptionEntry {
    average_consumption_m3_trim: number | null;
    average_bill_eur_trim: number | null;
}

export interface IncentiveConsumptionTable {
    ibt: IncentiveConsumptionEntry;
    ibt_pp: IncentiveConsumptionEntry;
    ibt_tbse: IncentiveConsumptionEntry;
}

// Define the structure for the efficiency data
export interface IncentiveEfficiencyEntry {
    eff_overconsumption: number | null;
    eff_mismanagement_cost: number | null;
}

export interface IncentiveEfficiencyTable {
    per_h: IncentiveEfficiencyEntry;
    per_ind: IncentiveEfficiencyEntry;
}


export interface EconomicEfficiencyRow {
    conso: number | null;
    delta_w: number | null;
}

export interface EconomicEfficiencyTable {
    first_best: EconomicEfficiencyRow;
    delta_tbse_a: EconomicEfficiencyRow;
    delta_ibt_a: EconomicEfficiencyRow;
    delta_ibt_pp_a: EconomicEfficiencyRow;
    impact_overconsumption: EconomicEfficiencyRow;
}

export interface SurplusDeltaRow {
    total_percent: number | null;
    g_percent: number | null;
    p_percent: number | null;
    total_value: number | null;
    g_value: number | null;
    p_value: number | null;
}

export interface SurplusImpactRow {
    total: number | null;
    overconsumers: number | null;
}

export interface EconomicEfficiencyDetailsTable {
    ibt_a_delta: SurplusDeltaRow;
    ibt_a_pp_delta: SurplusDeltaRow;
    impact_on_sur_co: SurplusImpactRow;
}

// Gini Index
export interface EquityGiniTable {
    ibt: number | null;
    ibt_ae: number | null;
    tbse: number | null;
}

// Basic Consumption (DAE / DAI)
export interface BasicConsumptionEquityRow {
    dae: number | null;
    dai: number | null;
}

export interface BasicConsumptionEquityTable {
    net_sub_basic_c: BasicConsumptionEquityRow;
    omega_ratio_1: BasicConsumptionEquityRow;
    net_taxes_basic_c: BasicConsumptionEquityRow;
    omega_ratio_2: BasicConsumptionEquityRow;
}

// Full Consumption (AFE / AFI)
export interface FullConsumptionEquityRow {
    afe: number | null;
    afi: number | null;
}

export interface FullConsumptionEquityTable {
    net_sub_c: FullConsumptionEquityRow;
    omega_ratio_1: FullConsumptionEquityRow;
    net_taxation: FullConsumptionEquityRow;
    omega_ratio_2: FullConsumptionEquityRow;
}

// /funding/rex_op
export interface FundingRexOp {
    general: number;
    total_cost: number;
}

// Funding metric row for DAE/DAI values
export interface FundingMetricRow {
    dae: number | null;
    dai: number | null;
}

// /funding/other
export interface FundingOther {
    net_contributors_percent: number | null;
    net_beneficiaries_percent: number | null;
    subsidized_basic_c_percent: number | null;
    subsidized_non_basic_c_percent: number | null;
    margined_c_percent: number | null;
    bad_sub_percent: FundingMetricRow;
    bad_tax_percent: FundingMetricRow;
}

// /environmental_cost
export interface EnvironmentalCostTable {
    tbse_conso_rang_1: number | null;
    effective_tbse: number | null;
    ibt: number | null;
    ibt_pp: number | null;
}

// /water_agency
export interface WaterAgency {
    exercise_duty: number | null;
}

// /state
export interface StateFunding {
    vat: number | null;
}


@Injectable({
    providedIn: 'root',
})
export class ResultsService {
    private apiUrl = environment.apiUrl;

    constructor(private http: HttpClient) {
    }

    /**
     * Gets the small assessment data for a specific simulation
     * @param id The simulation ID
     * @returns Observable with small assessment data
     */
    getAffordabilityResults(id: number): Observable<AffordabilityTable> {
        return this.http.get<AffordabilityTable>(
            `${this.apiUrl}/api/v1/results/${id}/affordability`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

    downloadCSV(id: number): Observable<any> {
        return this.http.get(
            `${this.apiUrl}/api/v1/results/${id}/csv`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                },
                responseType: 'blob'
            }
        );
    }

    getIncentiveConsumption(id: number): Observable<IncentiveConsumptionTable> {
        return this.http.get<IncentiveConsumptionTable>(
            `${this.apiUrl}/api/v1/results/${id}/incentive/consumption`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

    getIncentiveEfficiency(id: number): Observable<IncentiveEfficiencyTable> {
        return this.http.get<IncentiveEfficiencyTable>(
            `${this.apiUrl}/api/v1/results/${id}/incentive/efficiency`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

    getEconomicEfficiency(id: number): Observable<EconomicEfficiencyTable> {
        return this.http.get<EconomicEfficiencyTable>(
            `${this.apiUrl}/api/v1/results/${id}/economic_efficiency`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

    getEconomicEfficiencyDetails(id: number): Observable<EconomicEfficiencyDetailsTable> {
        return this.http.get<EconomicEfficiencyDetailsTable>(
            `${this.apiUrl}/api/v1/results/${id}/economic_efficiency/details`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

    getEquityGini(simulationId: number): Observable<EquityGiniTable> {
        return this.http.get<EquityGiniTable>(
            `${this.apiUrl}/api/v1/results/${simulationId}/equity/gini`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

    getBasicConsumptionEquity(simulationId: number): Observable<BasicConsumptionEquityTable> {
        return this.http.get<BasicConsumptionEquityTable>(
            `${this.apiUrl}/api/v1/results/${simulationId}/equity/basic_consumption`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

    getFullConsumptionEquity(simulationId: number): Observable<FullConsumptionEquityTable> {
        return this.http.get<FullConsumptionEquityTable>(
            `${this.apiUrl}/api/v1/results/${simulationId}/equity/full_consumption`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

    getFundingRexOp(simulationId: number): Observable<FundingRexOp> {
        return this.http.get<FundingRexOp>(
            `${this.apiUrl}/api/v1/results/${simulationId}/funding/rex_op`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

    getFundingOther(simulationId: number): Observable<FundingOther> {
        return this.http.get<FundingOther>(
            `${this.apiUrl}/api/v1/results/${simulationId}/funding/other`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

    getEnvironmentalCost(simulationId: number): Observable<EnvironmentalCostTable> {
        return this.http.get<EnvironmentalCostTable>(
            `${this.apiUrl}/api/v1/results/${simulationId}/environmental_cost`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

    getWaterAgency(simulationId: number): Observable<WaterAgency> {
        return this.http.get<WaterAgency>(
            `${this.apiUrl}/api/v1/results/${simulationId}/water_agency`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

    getStateFunding(simulationId: number): Observable<StateFunding> {
        return this.http.get<StateFunding>(
            `${this.apiUrl}/api/v1/results/${simulationId}/state`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }


}
