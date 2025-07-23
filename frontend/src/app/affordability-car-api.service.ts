import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {environment} from 'src/environments/environment';

export interface CarMetricsItem {
  g1_car_ibt: number;
  g1_car_tbse: number;
  g2_car_ibt: number;
  g2_car_tbse: number;
  id_projet: number;
  metric_type: string;
}

export interface CarMetricsResponse {
  data: CarMetricsItem[];
  id_projet: number;
  status: string;
}

export interface CarInequalityItem {
  G1_car_ibt: number;
  G2_car_ibt: number;
  id_projet: number;
  variable: string;
}

export interface CarInequalityResponse {
  data: CarInequalityItem[];
  id_projet: number;
  status: string;
}

export interface IncidenceCarItem {
  Delta_Moyennes_Menages: number;
  EPA_CAR: number;
  EP_CAR: number;
  Ensemble_CAR: number;
  Moyenne_CAR_TBSE: number;
  Variance_CAR_IBT: number;
  Variance_CAR_TBSE: number;
  f_i_menages: number;
  id_projet: number;
  moyenne_car_ibt: number;
}

export interface IncidenceCarResponse {
  data: IncidenceCarItem[];
  id_projet: number;
  status: string;
}

@Injectable({
  providedIn: 'root',
})
export class AffordabilityCarApiService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {
  }

  getCarMetrics(projectId: number = 1): Observable<CarMetricsResponse> {
    return this.http.get<CarMetricsResponse>(`${this.apiUrl}/api/car_metrics/${projectId}`);
  }

  getCarInequality(projectId: number = 1): Observable<CarInequalityResponse> {
    return this.http.get<CarInequalityResponse>(`${this.apiUrl}/api/ineg_car_eff_pct_ibt/${projectId}`);
  }

  getIncidenceCar(projectId: number = 1): Observable<IncidenceCarResponse> {
    return this.http.get<IncidenceCarResponse>(`${this.apiUrl}/api/inc_car/${projectId}`);
  }
}
