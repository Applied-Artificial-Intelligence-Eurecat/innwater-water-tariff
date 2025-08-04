import { Component, OnInit } from '@angular/core';

export interface AffordabilityData {
  metric: string;
  ibt: string;
  tbse: string;
}

@Component({
  selector: 'app-affordability-table',
  templateUrl: './affordability-table.component.html',
  styleUrls: ['./affordability-table.component.css']
})
export class AffordabilityTableComponent implements OnInit {
  displayedColumns: string[] = ['metric', 'ibt', 'tbse'];
  dataSource: AffordabilityData[] = [
    { metric: 'Headcount ratio', ibt: '15.9%', tbse: '32.1%' },
    { metric: 'App. Afford. Deft', ibt: '3.37 €', tbse: '16.87 €' },
    { metric: 'Effec. Afford. Defit', ibt: '17.69 €', tbse: '53.33 €' },
    { metric: 'Gini_App', ibt: '0.956', tbse: '0.793' },
    { metric: 'Gini_Eff', ibt: '0.725', tbse: '0.355' }
  ];

  constructor() { }

  ngOnInit(): void {
  }
} 