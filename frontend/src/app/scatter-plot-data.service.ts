import { Injectable } from '@angular/core';
import { Observable, of, throwError  } from 'rxjs';
import { delay } from 'rxjs/operators';
import { map } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { ScatterData } from './scatter-plot/plot-data.interface'; // Vérifie le chemin
import { catchError } from 'rxjs/operators'
import {  HttpErrorResponse } from '@angular/common/http';

@Injectable({
  providedIn: 'root', // Fournir le service au niveau racine
})
export class ScatterPlotDataService {
    constructor(private http: HttpClient) {}


    getPlotDataIterable(): Observable<ScatterData> {
        return this.http.get<any>('http://localhost:5001/scatter_plot_data').pipe(
          map(response => {
            if (!Array.isArray(response.x) || !Array.isArray(response.y)) {
              throw new Error('Les données renvoyées par l\'API ne sont pas au bon format');
            }
            const formattedData: ScatterData = {
              x: response.x,
              y: response.y
            };
            return formattedData;
          })
        );
      }


      
      getPlotDataScatterIerableTest(): Observable<ScatterData> {
        // Replace 'http://localhost:3000/api/data' with your actual API URL
        return this.http.get<any>('http://localhost:5001/scatter_plot_data').pipe(
          map((response) => {
            // Vérifie si la réponse est au bon format
            if (!response.data || !Array.isArray(response.data.Niveau_de_Vie_OCDE) || !Array.isArray(response.data.Par_TBSE)) {
              throw new Error('Les données renvoyées par l\'API ne sont pas au bon format');
            }
      
            // Transforme les données dans le format ScatterData
            const scatterData: ScatterData = {
              x: response.data.Niveau_de_Vie_OCDE,
              y: response.data.Par_TBSE,
            };
      
            return scatterData;
          }),
          catchError((error: HttpErrorResponse) => {
            console.error('Erreur de l\'API:', error.message);
            return throwError(() => new Error('Une erreur s\'est produite lors de la récupération des données.'));
          })
        );
      }
  
    // Méthode pour générer des données aléatoires pour le scatter plot
    getPlotDataScatter(): Observable<ScatterData> {
      const data: ScatterData = {
        x: Array.from({ length: 50 }, () => Math.floor(Math.random() * 2000)),
        y: Array.from({ length: 50 }, () => Math.random() * 25),
      };
      return of(data).pipe(delay(500)); // Simule un délai de réponse
    }
}
