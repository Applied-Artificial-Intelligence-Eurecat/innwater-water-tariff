import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

// Interface for the g1_g2/intensity endpoint response
export interface G1G2IntensityRowDeficit {
  perc: number;
  mean: number;
  var: number;
}

export interface G1G2IntensityGroupDeficit {
  g1: G1G2IntensityRowDeficit;
  g2: G1G2IntensityRowDeficit;
  ensemble: G1G2IntensityRowDeficit;
  var_inter: number;
  var_intra: number;
  rap_corr: number;
}

export interface G1G2IntensityDeficitTable {
  par_ibt: G1G2IntensityGroupDeficit;
  par_tbse: G1G2IntensityGroupDeficit;
}

export interface G1G2IntensityResponse {
  apparent: G1G2IntensityDeficitTable;
  effective: G1G2IntensityDeficitTable;
}

// Interface for the poor/intensity endpoint response
export interface PoorIntensityRowDeficit {
  perc: number;
  mean: number;
  var: number;
}

export interface PoorIntensityGroupDeficit {
  g1: PoorIntensityRowDeficit;
  g2: PoorIntensityRowDeficit;
  ensemble: PoorIntensityRowDeficit;
  var_inter: number;
  var_intra: number;
  rap_corr: number;
}

export interface PoorIntensityDeficitTable {
  par_ibt: PoorIntensityGroupDeficit;
  par_tbse: PoorIntensityGroupDeficit;
}

export interface PoorIntensityResponse {
  apparent: PoorIntensityDeficitTable;
  effective: PoorIntensityDeficitTable;
}

// Interface for the g1_g2/incidence endpoint response
export interface G1G2IncidenceResponse {
  g1: {
    perc_household: number;
    ibt_household: number;
    perc_people: number;
    ibt_people: number;
    perc_children: number;
    ibt_children: number;
    tbse_household: number;
    tbse_people: number;
    tbse_children: number;
  };
  g2: {
    perc_household: number;
    ibt_household: number;
    perc_people: number;
    ibt_people: number;
    perc_children: number;
    ibt_children: number;
    tbse_household: number;
    tbse_people: number;
    tbse_children: number;
  };
  total: {
    perc_household: number;
    ibt_household: number;
    perc_people: number;
    ibt_people: number;
    perc_children: number;
    ibt_children: number;
    tbse_household: number;
    tbse_people: number;
    tbse_children: number;
  };
}

// Interface for the poor/incidence endpoint response
export interface PoorIncidenceResponse {
  g1: {
    perc_household: number;
    ibt_household: number;
    perc_people: number;
    ibt_people: number;
    perc_children: number;
    ibt_children: number;
    tbse_household: number;
    tbse_people: number;
    tbse_children: number;
  };
  g2: {
    perc_household: number;
    ibt_household: number;
    perc_people: number;
    ibt_people: number;
    perc_children: number;
    ibt_children: number;
    tbse_household: number;
    tbse_people: number;
    tbse_children: number;
  };
  total: {
    perc_household: number;
    ibt_household: number;
    perc_people: number;
    ibt_people: number;
    perc_children: number;
    ibt_children: number;
    tbse_household: number;
    tbse_people: number;
    tbse_children: number;
  };
}

// Interface for the general/inequality endpoint response
export interface GeneralInequalityResponse {
  all: {
    gini: {
      par_ibt: number;
      par_tbse: number;
    };
    schutz: {
      par_ibt: number;
      par_tbse: number;
    };
  };
  unafford: {
    gini: {
      par_ibt: number;
      par_tbse: number;
    };
    schutz: {
      par_ibt: number;
      par_tbse: number;
    };
  };
}

// Interface for the poor/par_inequality endpoint response
export interface PoorInequalityResponse {
  par_ibt: {
    between: {
      value: number;
      perc: number;
    };
    within: {
      value: number;
      perc: number;
    };
    transvariation: {
      value: number;
      perc: number;
    };
    ensemble: {
      value: number;
      perc: number;
    };
  };
  par_tbse: {
    between: {
      value: number;
      perc: number;
    };
    within: {
      value: number;
      perc: number;
    };
    transvariation: {
      value: number;
      perc: number;
    };
    ensemble: {
      value: number;
      perc: number;
    };
  };
  excess_par_ibt: {
    between: {
      value: number;
      perc: number;
    };
    within: {
      value: number;
      perc: number;
    };
    transvariation: {
      value: number;
      perc: number;
    };
    ensemble: {
      value: number;
      perc: number;
    };
  };
  excess_par_tbse: {
    between: {
      value: number;
      perc: number;
    };
    within: {
      value: number;
      perc: number;
    };
    transvariation: {
      value: number;
      perc: number;
    };
    ensemble: {
      value: number;
      perc: number;
    };
  };
}

// Interface for the general/deficits endpoint response
export interface GeneralDeficitsResponse {
  apparent: {
    mean: {
      par_ibt: number;
      par_tbse: number;
      delta_par: number;
    };
    median: {
      par_ibt: number;
      par_tbse: number;
    };
    d1: {
      par_ibt: number;
      par_tbse: number;
    };
    d9: {
      par_ibt: number;
      par_tbse: number;
    };
    variance: {
      par_ibt: number;
      par_tbse: number;
    };
    ecart_type: {
      par_ibt: number;
      par_tbse: number;
    };
    cv: {
      par_ibt: number;
      par_tbse: number;
    };
    mape: {
      par_ibt: number;
      par_tbse: number;
    };
  };
  effective: {
    mean: {
      par_ibt: number;
      par_tbse: number;
      delta_par: number;
    };
    median: {
      par_ibt: number;
      par_tbse: number;
    };
    d1: {
      par_ibt: number;
      par_tbse: number;
    };
    d9: {
      par_ibt: number;
      par_tbse: number;
    };
    variance: {
      par_ibt: number;
      par_tbse: number;
    };
    ecart_type: {
      par_ibt: number;
      par_tbse: number;
    };
    cv: {
      par_ibt: number;
      par_tbse: number;
    };
    mape: {
      par_ibt: number;
      par_tbse: number;
    };
  };
}

// Interface for the general/incidence endpoint response
export interface GeneralIncidenceResponse {
  household: {
    par_ibt: number;
    par_tbse: number;
    delta_par: number;
  };
  people: {
    par_ibt: number;
    par_tbse: number;
    delta_par: number;
  };
  children: {
    par_ibt: number;
    par_tbse: number;
    delta_par: number;
  };
}

// Interface for the general/descriptive endpoint response
export interface GeneralDescriptiveResponse {
  mean: {
    par_ibt: number;
    par_tbse: number;
    delta_par: number;
  };
  median: {
    par_ibt: number;
    par_tbse: number;
    delta_par: number;
  };
  min: {
    par_ibt: number;
    par_tbse: number;
  };
  max: {
    par_ibt: number;
    par_tbse: number;
  };
  q1: {
    par_ibt: number;
    par_tbse: number;
  };
  q3: {
    par_ibt: number;
    par_tbse: number;
  };
  d1: {
    par_ibt: number;
    par_tbse: number;
  };
  d9: {
    par_ibt: number;
    par_tbse: number;
  };
  f: {
    par_ibt: number;
    par_tbse: number;
  };
  variance: {
    par_ibt: number;
    par_tbse: number;
  };
  ecart_type: {
    par_ibt: number;
    par_tbse: number;
  };
  MAPE: {
    par_ibt: number;
    par_tbse: number;
  };
  coeff_variation: {
    par_ibt: number;
    par_tbse: number;
  };
}

// Interface for the general_par_description endpoint response
export interface GeneralParDescriptionResponse {
  mean: {
    par_ibt_g1: number;
    par_ibt_g2: number;
    par_tbse_g1: number;
    par_tbse_g2: number;
    delta_par_g1: number;
    delta_par_g2: number;
  };
  median: {
    par_ibt_g1: number;
    par_ibt_g2: number;
    par_tbse_g1: number;
    par_tbse_g2: number;
    delta_par_g1: number;
    delta_par_g2: number;
  };
  min: {
    par_ibt_g1: number;
    par_ibt_g2: number;
    par_tbse_g1: number;
    par_tbse_g2: number;
  };
  max: {
    par_ibt_g1: number;
    par_ibt_g2: number;
    par_tbse_g1: number;
    par_tbse_g2: number;
  };
  q1: {
    par_ibt_g1: number;
    par_ibt_g2: number;
    par_tbse_g1: number;
    par_tbse_g2: number;
  };
  q3: {
    par_ibt_g1: number;
    par_ibt_g2: number;
    par_tbse_g1: number;
    par_tbse_g2: number;
  };
  d1: {
    par_ibt_g1: number;
    par_ibt_g2: number;
    par_tbse_g1: number;
    par_tbse_g2: number;
  };
  d9: {
    par_ibt_g1: number;
    par_ibt_g2: number;
    par_tbse_g1: number;
    par_tbse_g2: number;
  };
  f: {
    par_ibt_g1: number;
    par_ibt_g2: number;
    par_tbse_g1: number;
    par_tbse_g2: number;
  };
  variance: {
    par_ibt_g1: number;
    par_ibt_g2: number;
    par_tbse_g1: number;
    par_tbse_g2: number;
  };
  ecart_type: {
    par_ibt_g1: number;
    par_ibt_g2: number;
    par_tbse_g1: number;
    par_tbse_g2: number;
  };
  MAPE: {
    par_ibt_g1: number;
    par_ibt_g2: number;
    par_tbse_g1: number;
    par_tbse_g2: number;
  };
  coeff_variation: {
    par_ibt_g1: number;
    par_ibt_g2: number;
    par_tbse_g1: number;
    par_tbse_g2: number;
  };
}

// Interface for the poor/par_description endpoint response
export interface PoorDescriptiveResponse {
  mean: {
    par_ibt_g1: number;
    par_ibt_g2: number;
    par_tbse_g1: number;
    par_tbse_g2: number;
    delta_par_g1: number;
    delta_par_g2: number;
  };
  median: {
    par_ibt_g1: number;
    par_ibt_g2: number;
    par_tbse_g1: number;
    par_tbse_g2: number;
    delta_par_g1: number;
    delta_par_g2: number;
  };
  min: {
    par_ibt_g1: number;
    par_ibt_g2: number;
    par_tbse_g1: number;
    par_tbse_g2: number;
  };
  max: {
    par_ibt_g1: number;
    par_ibt_g2: number;
    par_tbse_g1: number;
    par_tbse_g2: number;
  };
  q1: {
    par_ibt_g1: number;
    par_ibt_g2: number;
    par_tbse_g1: number;
    par_tbse_g2: number;
  };
  q3: {
    par_ibt_g1: number;
    par_ibt_g2: number;
    par_tbse_g1: number;
    par_tbse_g2: number;
  };
  d1: {
    par_ibt_g1: number;
    par_ibt_g2: number;
    par_tbse_g1: number;
    par_tbse_g2: number;
  };
  d9: {
    par_ibt_g1: number;
    par_ibt_g2: number;
    par_tbse_g1: number;
    par_tbse_g2: number;
  };
  f: {
    par_ibt_g1: number;
    par_ibt_g2: number;
    par_tbse_g1: number;
    par_tbse_g2: number;
  };
  variance: {
    par_ibt_g1: number;
    par_ibt_g2: number;
    par_tbse_g1: number;
    par_tbse_g2: number;
  };
  ecart_type: {
    par_ibt_g1: number;
    par_ibt_g2: number;
    par_tbse_g1: number;
    par_tbse_g2: number;
  };
  MAPE: {
    par_ibt_g1: number;
    par_ibt_g2: number;
    par_tbse_g1: number;
    par_tbse_g2: number;
  };
  coeff_variation: {
    par_ibt_g1: number;
    par_ibt_g2: number;
    par_tbse_g1: number;
    par_tbse_g2: number;
  };
}

// Interface for the stat_par endpoint
export interface StatParItem {
  statistique: string;
  PAR_IBT_G1: number;
  PAR_IBT_G2: number;
  PAR_TBSEG1: number;
  PAR_TBSE_G2: number;
}

// Interface for the gini_sym_matrix endpoint
export interface GiniSymMatrixResponse {
  between: number;
  within: number;
  transvariation: number;
  ensemble: number;
  between_percent: number;
  within_percent: number;
  transvariation_percent: number;
  ensemble_percent: number;
}

// Interface for the gini_index_comparison endpoint
export interface GiniIndexComparisonResponse {
  par_ibt: {
    between: {
      value: number;
      perc: number;
    };
    within: {
      value: number;
      perc: number;
    };
    transvariation: {
      value: number;
      perc: number;
    };
    ensemble: {
      value: number;
      perc: number;
    };
  };
  par_tbse: {
    between: {
      value: number;
      perc: number;
    };
    within: {
      value: number;
      perc: number;
    };
    transvariation: {
      value: number;
      perc: number;
    };
    ensemble: {
      value: number;
      perc: number;
    };
  };
  excess_par_ibt: {
    between: {
      value: number;
      perc: number;
    };
    within: {
      value: number;
      perc: number;
    };
    transvariation: {
      value: number;
      perc: number;
    };
    ensemble: {
      value: number;
      perc: number;
    };
  };
  excess_par_tbse: {
    between: {
      value: number;
      perc: number;
    };
    within: {
      value: number;
      perc: number;
    };
    transvariation: {
      value: number;
      perc: number;
    };
    ensemble: {
      value: number;
      perc: number;
    };
  };
}

@Injectable({
  providedIn: 'root'
})
export class AffordabilityParApiService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  /**
   * Gets the general PAR description data for a specific simulation
   * @param id The simulation ID
   * @returns Observable with general PAR description data
   */
  getGeneralParDescription(id: number): Observable<GeneralParDescriptionResponse> {
    return this.http.get<GeneralParDescriptionResponse>(
      `${this.apiUrl}/api/v1/results/affordability/${id}/g1_g2_par_description`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }
    );
  }

  /**
   * Gets the statistical PAR data for a specific simulation
   * @param id The simulation ID
   * @returns Observable with statistical PAR data
   */
  getStatPar(id: number): Observable<StatParItem[]> {
    return this.http.get<StatParItem[]>(
      `${this.apiUrl}/api/v1/results/affordability/${id}/stat_par`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }
    );
  }

  /**
   * Gets the Gini symmetrical matrix data for a specific simulation
   * @param id The simulation ID
   * @returns Observable with Gini symmetrical matrix data
   */
  getGiniSymMatrix(id: number): Observable<GiniSymMatrixResponse> {
    return this.http.get<GiniSymMatrixResponse>(
      `${this.apiUrl}/api/v1/results/affordability/${id}/gini_sym_matrix`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }
    );
  }

  /**
   * Gets the inequality Gini data
   * @returns Observable with inequality Gini data
   */
  getInequalityGini(): Observable<any> {
    return this.http.get<any>(
      `${this.apiUrl}/api/v1/results/affordability/inequality_gini`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }
    );
  }

  /**
   * Gets the Gini index comparison data for a specific simulation
   * @param id The simulation ID
   * @returns Observable with Gini index comparison data
   */
  getGiniIndexComparison(id: number): Observable<GiniIndexComparisonResponse> {
    return this.http.get<GiniIndexComparisonResponse>(
      `${this.apiUrl}/api/v1/results/affordability/${id}/g1_g2_par_inequality`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }
    );
  }

  /**
   * Gets the general descriptive statistics for a specific simulation
   * @param id The simulation ID
   * @returns Observable with general descriptive statistics
   */
  getGeneralDescriptive(id: number): Observable<GeneralDescriptiveResponse> {
    return this.http.post<GeneralDescriptiveResponse>(
      `${this.apiUrl}/api/v1/results/affordability/${id}/general/descriptive`,
      {},
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }
    );
  }

  /**
   * Gets the general incidence statistics for a specific simulation
   * @param id The simulation ID
   * @returns Observable with general incidence statistics
   */
  getGeneralIncidence(id: number): Observable<GeneralIncidenceResponse> {
    return this.http.post<GeneralIncidenceResponse>(
      `${this.apiUrl}/api/v1/results/affordability/${id}/general/incidence`,
      {},
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }
    );
  }

  /**
   * Gets the general deficits statistics for a specific simulation
   * @param id The simulation ID
   * @returns Observable with general deficits statistics
   */
  getGeneralDeficits(id: number): Observable<GeneralDeficitsResponse> {
    return this.http.get<GeneralDeficitsResponse>(
      `${this.apiUrl}/api/v1/results/affordability/${id}/general/deficits`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }
    );
  }

  /**
   * Gets the general inequality statistics for a specific simulation
   * @param id The simulation ID
   * @returns Observable with general inequality statistics
   */
  getGeneralInequality(id: number): Observable<GeneralInequalityResponse> {
    return this.http.get<GeneralInequalityResponse>(
      `${this.apiUrl}/api/v1/results/affordability/${id}/general/inequality`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }
    );
  }

  /**
   * Gets the G1 vs G2 incidence data for a specific simulation
   * @param id The simulation ID
   * @returns Observable with G1 vs G2 incidence data
   */
  getG1G2Incidence(id: number): Observable<G1G2IncidenceResponse> {
    return this.http.get<G1G2IncidenceResponse>(
      `${this.apiUrl}/api/v1/results/affordability/${id}/g1_g2/incidence`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }
    );
  }

  /**
   * Gets the G1 vs G2 intensity data for a specific simulation
   * @param id The simulation ID
   * @returns Observable with G1 vs G2 intensity data
   */
  getG1G2Intensity(id: number): Observable<G1G2IntensityResponse> {
    return this.http.get<G1G2IntensityResponse>(
      `${this.apiUrl}/api/v1/results/affordability/${id}/g1_g2/intensity`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }
    );
  }

  /**
   * Gets the Poor vs Non-poor descriptive statistics for a specific simulation
   * @param id The simulation ID
   * @returns Observable with Poor vs Non-poor descriptive statistics
   */
  getPoorDescriptive(id: number): Observable<PoorDescriptiveResponse> {
    return this.http.get<PoorDescriptiveResponse>(
      `${this.apiUrl}/api/v1/results/affordability/${id}/poor/par_description`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }
    );
  }

  /**
   * Gets the Poor vs Non-poor incidence data for a specific simulation
   * @param id The simulation ID
   * @returns Observable with Poor vs Non-poor incidence data
   */
  getPoorIncidence(id: number): Observable<PoorIncidenceResponse> {
    return this.http.get<PoorIncidenceResponse>(
      `${this.apiUrl}/api/v1/results/affordability/${id}/poor/incidence`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }
    );
  }

  /**
   * Gets the Poor vs Non-poor intensity data for a specific simulation
   * @param id The simulation ID
   * @returns Observable with Poor vs Non-poor intensity data
   */
  getPoorIntensity(id: number): Observable<PoorIntensityResponse> {
    return this.http.get<PoorIntensityResponse>(
      `${this.apiUrl}/api/v1/results/affordability/${id}/poor/intensity`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }
    );
  }

  /**
   * Gets the Poor vs Non-poor inequality data for a specific simulation
   * @param id The simulation ID
   * @returns Observable with Poor vs Non-poor inequality data
   */
  getPoorInequality(id: number): Observable<PoorInequalityResponse> {
    return this.http.get<PoorInequalityResponse>(
      `${this.apiUrl}/api/v1/results/affordability/${id}/poor/par_inequality`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }
    );
  }
}
