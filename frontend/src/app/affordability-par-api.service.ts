import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

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
      `${this.apiUrl}/api/v1/results/affordability/${id}/general_par_description`,
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
      `${this.apiUrl}/api/v1/results/affordability/${id}/gini_index_comparison`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }
    );
  }
}
