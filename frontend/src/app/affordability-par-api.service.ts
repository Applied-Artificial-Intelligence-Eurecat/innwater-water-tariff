import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {environment} from 'src/environments/environment';
import {map} from "rxjs/operators";

export interface AffordabilityDeficitItem {
    Delta: number;
    Delta_Moyennes_Menages: number;
    PAR_IBT: number;
    PAR_IBT_Moyenne: number;
    PAR_IBT_Variance: number;
    PAR_TBSE: number;
    PAR_TBSE_Moyenne: number;
    PAR_TBSE_Variance: number;
    g_j_PAR_IBT: number;
    g_j_PAR_TBSE: number;
    id: number;
    id_projet: number;
}

export interface DeficitApparentResponse {
    data: AffordabilityDeficitItem[];
    status: string;
}


export interface AffordabilityDeficitResponse {
    count: number;
    data: AffordabilityDeficitItem[];
    id_projet: number;
}

export interface InequalityGiniItem {
    id: number;
    id_projet: number;
    indicateur: string;  // e.g., "PAR IBT_Between"
    G1: number;          // Raw value
    G2: number;          // % of population Gini
}

export interface InequalityGiniResponse {
    count: number;
    id_projet: number;
    data: InequalityGiniItem[];
}

export interface StatParItem {
    Metric: string;
    PAR_IBT_G1: number;
    PAR_IBT_G2: number;
    PAR_TBSEG1: number;
    PAR_TBSE_G2: number;
    id_projet: number;
    statistique: string;
}

export interface IncidenceParItem {
    Delta_Enfants: number;
    Delta_Individus: number;
    Delta_Menages: number;
    PAR_IBT_Enfants: number;
    PAR_IBT_Individus: number;
    PAR_IBT_Menages: number;
    PAR_IBT_Ménages: number;
    PAR_TBSE_Enfants: number;
    PAR_TBSE_Individus: number;
    PAR_TBSE_Menages: number;
    PAR_TBSE_Ménages: number;
    f_i_pourcent: string;
    id_projet: string;
}

export interface IncidenceParResponse {
    data: IncidenceParItem[];
    id_projet: string;
}

export interface GiniSymMatrixItem {
    G1_PAR_TBSE: number;
    G2_PAR_TBSE: number;
    id_projet: number;
}

export interface GiniSymMatrixResponse {
    data: GiniSymMatrixItem[];
    id_projet: number;
}

export interface TfParItem {
    Delta_PAR_G1: number;
    Delta_PAR_G2: number;
    PAR_IBT_G1: number;
    PAR_IBT_G2: number;
    PAR_TBSEG1: number;
    PAR_TBSE_G2: number;
    id_projet: string;
    statistique: string;
}

export interface TfParResponse {
    data: TfParItem[];
    metadata: {
        count: number;
        db_name: string;
        id_projet: string;
        table_name: string;
    };
}



export interface TfInegParGiniPdsItem {
    alpha_j: number;
    alpha_j_cumul: number;
    f_j: number;
    f_j_cumul: number;
    groupe: string;
    id_projet: number;
}

export interface TfInegParGiniPdsResponse {
    count: number;
    data: TfInegParGiniPdsItem[];
    id_projet: number;
}

export interface TfInegParGiniCtrIBTResponse {
    data: {
        groupe_cible: string[];
        groupe_source: string[];
        valeurs: number[][];
    };
    id_projet: string;
}

export interface TfInegParGiniCtrResponse {
    data: {
        "G1_PAR TBSE": {
            "G1_PAR TBSE": number;
            "G2_PAR TBSE": number;
        };
        "G2_PAR TBSE": {
            "G1_PAR TBSE": number;
            "G2_PAR TBSE": number;
        };
    };
    id_projet: number;
    status: string;
}

export interface TfInegParGiniPctItem {
    g1_par_ibt: number;
    g2_par_ibt: number;
    id_projet: number;
}

export interface TfInegParGiniPctResponse {
    count: number;
    data: TfInegParGiniPctItem[];
    success: boolean;
}


@Injectable({
    providedIn: 'root',
})
export class AffordabilityParApiService {
    private apiUrl = environment.apiUrl;


    constructor(private http: HttpClient) {
    }

    login(username: string, password: string) {
        return this.http.post(`${this.apiUrl}/api/signup`, {username, password});
    }

    getAffordabilityDeficitEffectif(projectId: number = 1): Observable<AffordabilityDeficitResponse> {
        return this.http.get<AffordabilityDeficitResponse>(`${this.apiUrl}/api/tf_int_par_de?id_projet=${projectId}`);
    }

    getAffordabilityDeficitApparent(projectId: string = "PROJET_TEST"): Observable<DeficitApparentResponse> {
        return this.http.get<DeficitApparentResponse>(`${this.apiUrl}/api/tf_int_par_da?id_projet=${projectId}`);
    }

    getInequalityGini(): Observable<InequalityGiniResponse> {
        return this.http.get<InequalityGiniResponse>(`${this.apiUrl}/api/tf_ineg_par_gini?id_projet=1`);
    }

    getStatPar(projectId: number = 1): Observable<StatParItem[]> {
        return this.http.get<StatParItem[]>(`${this.apiUrl}/api/stat_par/${projectId}`);
    }

    getGiniSymMatrix(projectId: number = 1): Observable<GiniSymMatrixResponse> {
        return this.http.get<GiniSymMatrixResponse>(`${this.apiUrl}/api/tf_ineg_par_gini_sym_TBSE/${projectId}`);
    }

    getIncidencePar(projectId: number = 1): Observable<IncidenceParResponse> {
        return this.http.get<any>(`${this.apiUrl}/api/tf_inc_par?id_projet=${projectId}`).pipe(map(response => {
            var result: any = {...response, PAR_IBT_Menages: 0}
            result['data'].map((val: { PAR_IBT_Ménages: any; }) => {
                return {
                    ...val,
                    PAR_IBT_Menages: val.PAR_IBT_Ménages
                }
            })
            return result
        }));
    }

    getTfPar(projectId: number = 1): Observable<TfParResponse> {
        return this.http.get<TfParResponse>(`${this.apiUrl}/api/tf_par?id_projet=${projectId}`);
    }


    getTfInegParGiniPds(projectId: number = 1): Observable<TfInegParGiniPdsResponse> {
        return this.http.get<TfInegParGiniPdsResponse>(`${this.apiUrl}/api/tf_ineg_par_gini_pds?id_projet=${projectId}`);
    }

    getTfInegParGiniCtrIBT(projectId: string = 'PROJET_TEST'): Observable<TfInegParGiniCtrIBTResponse> {
        return this.http.get<TfInegParGiniCtrIBTResponse>(`${this.apiUrl}/api/tf_ineg_par_gini_ctr_IBT?id_projet=${projectId}`);
    }

    getTfInegParGiniCtr(projectId: number = 1): Observable<TfInegParGiniCtrResponse> {
        return this.http.get<TfInegParGiniCtrResponse>(`${this.apiUrl}/api/tf_ineg_par_gini_ctr/${projectId}`);
    }

    getTfInegParGiniPct(projectId: number = 1): Observable<TfInegParGiniPctResponse> {
        return this.http.get<TfInegParGiniPctResponse>(`${this.apiUrl}/api/tf_ineg_par_gini_pct?id_projet=${projectId}`);
    }
}
