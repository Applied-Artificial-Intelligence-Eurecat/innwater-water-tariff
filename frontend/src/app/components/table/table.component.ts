import { Component } from '@angular/core';
//import { Component,OnInit } from '@angular/core';
import { FormArray, FormControl, FormBuilder, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.css']
})
export class TableComponent {
  tableData = [
    { category: 'Moyenne', parIbt: 1.1, parTbse: 3.2, deltaPar: -2.0, carIbt: 2.5, carTbse: 4.1, deltaCar: -1.57 },
    { category: 'Médiane', parIbt: 0.7, parTbse: 2.0, deltaPar: -1.3, carIbt: 1.9, carTbse: 2.9, deltaCar: -0.99 },
    { category: 'Min', parIbt: 0.0, parTbse: 0.1, deltaPar: null, carIbt: 0.3, carTbse: 0.3, deltaCar: null },
    { category: 'Max', parIbt: 10.9, parTbse: 21.9, deltaPar: null, carIbt: 12.6, carTbse: 23.6, deltaCar: null },
    { category: 'Q1', parIbt: 0.3, parTbse: 0.9, deltaPar: null, carIbt: 1.0, carTbse: 1.4, deltaCar: null },
    { category: 'Q3', parIbt: 1.4, parTbse: 3.9, deltaPar: null, carIbt: 3.3, carTbse: 5.0, deltaCar: null },
    { category: 'D1', parIbt: 0.1, parTbse: 0.5, deltaPar: null, carIbt: 0.6, carTbse: 0.8, deltaCar: null },
    { category: 'D9', parIbt: 2.6, parTbse: 8.0, deltaPar: null, carIbt: 5.4, carTbse: 9.6, deltaCar: null },
    { category: 'F (Moyenne)', parIbt: 68.5, parTbse: 69.3, deltaPar: null, carIbt: 63.0, carTbse: 68.1, deltaCar: null },
    { category: 'Variance', parIbt: 1.89, parTbse: 12.64, deltaPar: null, carIbt: 4.24, carTbse: 15.73, deltaCar: null },
    { category: 'Écart-type', parIbt: 1.4, parTbse: 3.6, deltaPar: null, carIbt: 2.06, carTbse: 3.97, deltaCar: null },
    { category: 'MAPE', parIbt: 0.9, parTbse: 2.5, deltaPar: null, carIbt: 1.5, carTbse: 2.9, deltaCar: null },
    { category: 'Coeff de Variation', parIbt: 1.216, parTbse: 1.119, deltaPar: null, carIbt: 0.822, carTbse: 0.972, deltaCar: null },
    { category: 'Étendue Interquantiles', parIbt: 1.1, parTbse: 3.0, deltaPar: null, carIbt: 2.3, carTbse: 3.6, deltaCar: null },
    { category: 'Étendue Interdéciles', parIbt: 2.5, parTbse: 7.5, deltaPar: null, carIbt: 4.8, carTbse: 8.8, deltaCar: null },
    { category: 'Coefficients de Yule', parIbt: 0.29, parTbse: 0.30, deltaPar: null, carIbt: 0.23, carTbse: 0.18, deltaCar: null },
  ];

 
  
    tableData2 = [
      {
        category: 'Ménages',
        parIbt: 7.9,
        parTbse: 32.8,
        deltaPar: -24.9,
        carIbt: 28.8,
        carTbse: 48.3,
        deltaCar: -19.4
      },
      {
        category: 'Individus',
        parIbt: 7.9,
        parTbse: 31.6,
        deltaPar: -23.8,
        carIbt: 32.6,
        carTbse: 48.9,
        deltaCar: -16.3
      },
      {
        category: 'Enfants',
        parIbt: 9.9,
        parTbse: 35.1,
        deltaPar: -25.2,
        carIbt: 38.0,
        carTbse: 52.3,
        deltaCar: -14.3
      }
    ];
 
    tableData3 = [
      {
        category: 'Moyenne',
        parIbt: 1.39,
        parTbse: 17.47,
        deltaPar: -16.08,
        carIbt: 9.51,
        carTbse: 29.03,
        deltaCar: -19.52
      },
      {
        category: 'Médiane',
        parIbt: 0.0,
        parTbse: 0.0,
        deltaPar: 0.0,
        carIbt: 0.0,
        carTbse: 0.0,
        deltaCar: null // Valeur manquante
      },
      {
        category: 'Variance',
        parIbt: 38.5366,
        parTbse: 1013.2596,
        deltaPar: null, // Valeur manquante
        carIbt: 389.6407,
        carTbse: 1718.7326,
        deltaCar: null // Valeur manquante
      },
      {
        category: 'Ecart-type',
        parIbt: 6.21,
        parTbse: 31.83,
        deltaPar: null, // Valeur manquante
        carIbt: 19.74,
        carTbse: 41.46,
        deltaCar: null // Valeur manquante
      },
      {
        category: 'cv',
        parIbt: 4.47,
        parTbse: 1.82,
        deltaPar: null, // Valeur manquante
        carIbt: 2.076,
        carTbse: 1.428,
        deltaCar: null // Valeur manquante
      },
      {
        category: 'MAPE',
        parIbt: 2.57,
        parTbse: 24.49,
        deltaPar: null, // Valeur manquante
        carIbt: 13.97,
        carTbse: 34.32,
        deltaCar: null // Valeur manquante
      }
    ];



    tableData4 = [
      {
        category: 'Moyenne',
        parIbt: 17.69,
        parTbse: 53.33,
        deltaPar: -35.64,
        carIbt: 33.0,
        carTbse: 60.17,
        deltaCar: -27.17
      },
      {
        category: 'Médiane',
        parIbt: 16.15,
        parTbse: 43.78,
        deltaPar: null,
        carIbt: 27.85,
        carTbse: 52.73,
        deltaCar: null
      },
      {
        category: 'D1',
        parIbt: 2.08,
        parTbse: 11.03,
        deltaPar: null,
        carIbt: 6.07,
        carTbse: 9.73,
        deltaCar: null
      },
      {
        category: 'D9',
        parIbt: 37.01,
        parTbse: 102.79,
        deltaPar: null,
        carIbt: 64.5,
        carTbse: 119.81,
        deltaCar: null
      },
      {
        category: 'Variance',
        parIbt: 202.081,
        parTbse: 1181.3969,
        deltaPar: null,
        carIbt: 576.8663,
        carTbse: 1688.4959,
        deltaCar: null
      },
      {
        category: 'Ecart-type',
        parIbt: 14.22,
        parTbse: 34.37,
        deltaPar: null,
        carIbt: 24.02,
        carTbse: 41.09,
        deltaCar: null
      },
      {
        category: 'cv',
        parIbt: 0.804,
        parTbse: 0.645,
        deltaPar: null,
        carIbt: 0.728,
        carTbse: 0.683,
        deltaCar: null
      },
      {
        category: 'MAPE',
        parIbt: 11.25,
        parTbse: 30.19,
        deltaPar: null,
        carIbt: 19.26,
        carTbse: 35.64,
        deltaCar: null
      }
    ];

    tableData5 = [
      { ensemble: 'Gini', ibt1: '95,6', tbse1: '79,3', ibt2: '82,7', tbse2: '70,6' },
      { ensemble: 'Schutz', ibt1: '92,3', tbse1: '70,1', ibt2: '73,5', tbse2: '59,1' },
    ];


    tableData6 = [
      { indicateur: 'Gini', ibt1: '22,1', tbse1: '36,8', ibt2: '68,8', tbse2: '39,0' },
      { indicateur: 'Schutz', ibt1: '31,8', tbse1: '28,3', ibt2: '29,2', tbse2: '29,6' },
      { indicateur: 'Ratio interdéciles', ibt1: '17,8', tbse1: '9,3', ibt2: '10,6', tbse2: '12,3' },
    ];
  
    constructor( private http : HttpClient,private fb:FormBuilder,private router: Router){}
    redirectToDataDisplay() {
      this.router.navigateByUrl('/EtapesProcessus');
    }

    redirectToParam() {
      this.router.navigateByUrl('/addsimulation');
    }


}
