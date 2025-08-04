import { Component, OnInit } from '@angular/core';

export interface EnvironmentalCostsData {
  category: string;
  value: string;
}

@Component({
  selector: 'app-environmental-costs-table',
  templateUrl: './environmental-costs-table.component.html',
  styleUrls: ['./environmental-costs-table.component.css']
})
export class EnvironmentalCostsTableComponent implements OnInit {
  displayedColumns: string[] = ['category', 'value'];
  dataSource: EnvironmentalCostsData[] = [
    { category: 'TBSE Conso Rang 1', value: '423.18 €' },
    { category: 'Effective TBSE', value: '683.76 €' },
    { category: 'IBT', value: '192.41 €' },
    { category: 'IBT PP', value: '181.08 €' }
  ];

  constructor() { }

  ngOnInit(): void {
  }
} 