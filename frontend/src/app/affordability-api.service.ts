import {Injectable} from '@angular/core';
import {environment} from "../environments/environment";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

export interface AffordabilityGeneralRow {
    metric: string;
    par_ibt: number | null;
    par_tbse: number | null;
    delta_par: number | null;
    car_ibt: number | null;
    car_tbse: number | null;
    delta_car: number | null;
}

@Injectable({
    providedIn: 'root'
})
export class AffordabilityApiService {
    private apiUrl = environment.apiUrl;

    constructor(private http: HttpClient) {
    }

    /**
     * Gets the small assessment data for a specific simulation
     * @param id The simulation ID
     * @returns Observable with small assessment data
     */
    getGeneralInfo(id: number): Observable<AffordabilityGeneralRow[]> {
        return this.http.get<AffordabilityGeneralRow[]>(
            `${this.apiUrl}/api/v1/results/affordability/${id}/general`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

}
