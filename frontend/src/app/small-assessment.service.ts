import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

// Interface for the usage tier data
export interface UsageTier {
  seuil?: number;
  prix?: number;
  threshold?: number;
  price?: number;
}

// Interface for the GET response
export interface SmallAssessmentResponse {
  ep: {
    abonnement: number;
    usage_tiers: UsageTier[];
  };
  assainissement: {
    abonnement: number;
    usage_tiers: UsageTier[];
  };
}

// Interface for the PUT payload
export interface SmallAssessmentUpdatePayload {
  ep: {
    subscription: number;
    usage_tiers: {
      threshold: number;
      price: number;
    }[];
  };
  assainissement: {
    subscription: number;
    usage_tiers: {
      threshold: number;
      price: number;
    }[];
  };
}

@Injectable({
  providedIn: 'root',
})
export class SmallAssessmentService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  /**
   * Gets the small assessment data for a specific simulation
   * @param id The simulation ID
   * @returns Observable with small assessment data
   */
  getSmallAssessment(id: number): Observable<SmallAssessmentResponse> {
    return this.http.get<SmallAssessmentResponse>(
      `${this.apiUrl}/api/v1/small_assessment/ibt/${id}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }
    );
  }

  /**
   * Updates the small assessment data for a specific simulation
   * @param id The simulation ID
   * @param payload The updated small assessment data
   * @returns Observable with the response
   */
  updateSmallAssessment(id: number, payload: SmallAssessmentUpdatePayload): Observable<any> {
    return this.http.put(
      `${this.apiUrl}/api/v1/small_assessment/ibt/${id}`,
      payload,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }
    );
  }

  validateAndSimulate(id: number, payload: SmallAssessmentUpdatePayload): Observable<any> {
    return this.http.post(
      `${this.apiUrl}/api/v1/small_assessment/validate/${id}`,
      payload,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }
    );
  }
}