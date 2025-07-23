import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ScatterData {
  id: number;
  x: number;
  y: number;
}

export interface PenParadeData {
  base: ScatterData[];
  captive: ScatterData[];
}

@Injectable({
  providedIn: 'root'
})
export class PenParadeDataService {
  private apiUrl = 'http://127.0.0.1:5001/api/data_pen_parade'; // Remplace par l'URL de ton backend

  constructor(private http: HttpClient) {}

  getPlotData(): Observable<PenParadeData> {
    return this.http.get<PenParadeData>(this.apiUrl);
  }
}
