import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {environment} from '../environments/environment';

export interface GeneralDescriptionMetrics {
    ibt: number;
    ibt_pp: number;
    tbse: number;
    actual_overconsumption: number;
    overconsumption_per_capita: number;
}

export interface GeneralDescriptionResponse {
    mean: GeneralDescriptionMetrics;
    median: GeneralDescriptionMetrics;
    min: GeneralDescriptionMetrics;
    max: GeneralDescriptionMetrics;
    q1: GeneralDescriptionMetrics;
    q3: GeneralDescriptionMetrics;
    d1: GeneralDescriptionMetrics;
    d9: GeneralDescriptionMetrics;
    percentile_rank: GeneralDescriptionMetrics;
    variance: GeneralDescriptionMetrics;
    ecart_type: GeneralDescriptionMetrics;
    mape: GeneralDescriptionMetrics;
    variation_coeff: GeneralDescriptionMetrics;
    iqr: GeneralDescriptionMetrics;
    idr: GeneralDescriptionMetrics;
    yule_coeff: GeneralDescriptionMetrics;
    gini_schutz: GeneralDescriptionMetrics;
}

export interface DeltaGeneralMetrics {
    delta_ibt_plus: number;
    delta_ibt_minus: number;
    delta_ibt_pp_plus: number;
    delta_ibt_pp_minus: number;
}

export interface DeltaGeneralDescriptionResponse {
    perc_households: DeltaGeneralMetrics;
    mean: DeltaGeneralMetrics;
    median: DeltaGeneralMetrics;
    min: DeltaGeneralMetrics;
    max: DeltaGeneralMetrics;
    q1: DeltaGeneralMetrics;
    q3: DeltaGeneralMetrics;
    d1: DeltaGeneralMetrics;
    d9: DeltaGeneralMetrics;
    percentile_rank: DeltaGeneralMetrics;
    variance: DeltaGeneralMetrics;
    ecart_type: DeltaGeneralMetrics;
    mape: DeltaGeneralMetrics;
    variation_coeff: DeltaGeneralMetrics;
    iqr: DeltaGeneralMetrics;
    idr: DeltaGeneralMetrics;
    yule_coeff: DeltaGeneralMetrics;
    gini_schutz: DeltaGeneralMetrics;
}

export interface DecompositionEntryRaw {
    frequency: number | string;
    delta_c_moyen: number | string;
    variance: number | string;
}

export interface DecompositionTablesResponseRaw {
    ensemble: DecompositionEntryRaw;
    delta_plus: DecompositionEntryRaw;
    delta_minus: DecompositionEntryRaw;
    g1_delta_plus: DecompositionEntryRaw;
    g2_delta_plus: DecompositionEntryRaw;
    g1_delta_minus: DecompositionEntryRaw;
    g2_delta_minus: DecompositionEntryRaw;
    poor_delta_plus: DecompositionEntryRaw;
    poor_delta_minus: DecompositionEntryRaw;
    nonpoor_delta_plus: DecompositionEntryRaw;
    nonpoor_delta_minus: DecompositionEntryRaw;
}

export interface ContingencyTableEntry {
    poor: number;
    nonpoor: number;
    ensemble: number;
}

export interface ContingencyTableResponse {
    increase: {
        g1: ContingencyTableEntry;
        g2: ContingencyTableEntry;
        total_population: ContingencyTableEntry;
    };
    decrease: {
        g1: ContingencyTableEntry;
        g2: ContingencyTableEntry;
        total_population: ContingencyTableEntry;
    };
}

export interface OverconsumptionDecompositionEntry { frequency: number; delta_c_moyen: number; variance: number; }
export interface OverconsumptionDecompositionResponse {
    decomposed: {
        households_percentage: OverconsumptionDecompositionEntry;
        g1: OverconsumptionDecompositionEntry;
        g2: OverconsumptionDecompositionEntry;
        poor: OverconsumptionDecompositionEntry;
        nonpoor: OverconsumptionDecompositionEntry;
    };
    groups_variance: { v_inter: number; v_intra: number; correlation_ratio: number };
    poor_variance: { v_inter: number; v_intra: number; correlation_ratio: number };
}

export interface HouseholdsOverconsumeCompositionResponse {
    g1: ContingencyTableEntry;
    g2: ContingencyTableEntry;
    total_population: ContingencyTableEntry;
}

export interface BreakdownOfOverconsumptionCompositionResponse {
    g1: ContingencyTableEntry;
    g2: ContingencyTableEntry;
    total_population: ContingencyTableEntry;
}

@Injectable({ providedIn: 'root' })
export class IncentiveEffectService {
    private apiUrl = environment.apiUrl;

    constructor(private http: HttpClient) {}

    getGeneralDescription(simulationId: number): Observable<GeneralDescriptionResponse> {
        return this.http.get<GeneralDescriptionResponse>(
            `${this.apiUrl}/api/v1/results/incentive/${simulationId}/general_description`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

    getDeltaGeneralDescription(simulationId: number): Observable<DeltaGeneralDescriptionResponse> {
        return this.http.get<DeltaGeneralDescriptionResponse>(
            `${this.apiUrl}/api/v1/results/incentive/${simulationId}/delta_general_description`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

    getDecompositionTables(simulationId: number): Observable<DecompositionTablesResponseRaw> {
        return this.http.get<DecompositionTablesResponseRaw>(
            `${this.apiUrl}/api/v1/results/incentive/${simulationId}/decomposition_tables`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

    getContingencyTablePercentages(simulationId: number): Observable<ContingencyTableResponse> {
        return this.http.get<ContingencyTableResponse>(
            `${this.apiUrl}/api/v1/results/incentive/${simulationId}/contingency_table_percentages`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

    getContingencyTableConsumption(simulationId: number): Observable<ContingencyTableResponse> {
        return this.http.get<ContingencyTableResponse>(
            `${this.apiUrl}/api/v1/results/incentive/${simulationId}/contingency_table_consumption`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

    getOverconsumptionDecomposition(simulationId: number): Observable<OverconsumptionDecompositionResponse> {
        return this.http.get<OverconsumptionDecompositionResponse>(
            `${this.apiUrl}/api/v1/results/incentive/${simulationId}/overconsumption_decomposition`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

    getHouseholdsThatOverconsumeComposition(simulationId: number): Observable<HouseholdsOverconsumeCompositionResponse> {
        return this.http.get<HouseholdsOverconsumeCompositionResponse>(
            `${this.apiUrl}/api/v1/results/incentive/${simulationId}/households_that_overconsume_composition`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

    getBreakdownOfOverconsumptionComposition(simulationId: number): Observable<BreakdownOfOverconsumptionCompositionResponse> {
        return this.http.get<BreakdownOfOverconsumptionCompositionResponse>(
            `${this.apiUrl}/api/v1/results/incentive/${simulationId}/breakdown_of_overconsumption_composition`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }
}


