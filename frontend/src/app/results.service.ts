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
    delta_ibt_pp: EconomicEfficiencyRow;
    impact_sur_co: EconomicEfficiencyRow;
    delta_tbse: EconomicEfficiencyRow;
    delta_surplus_m: EconomicEfficiencyRow;
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

}