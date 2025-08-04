import { Component, OnInit } from '@angular/core';

export interface EconomicEfficiencyData {
  category: string;
  consumption: string;
  deltaW: string;
}

@Component({
  selector: 'app-economic-efficiency-table',
  templateUrl: './economic-efficiency-table.component.html',
  styleUrls: ['./economic-efficiency-table.component.css']
})
export class EconomicEfficiencyTableComponent implements OnInit {
  displayedColumns: string[] = ['category', 'consumption', 'deltaW'];
  dataSource: EconomicEfficiencyData[] = [
    { category: 'Average', consumption: '-', deltaW: '-' },
    { category: 'First Best', consumption: '90.4', deltaW: '***' },
    { category: 'Delta IBT PP', consumption: '-51.9', deltaW: '-961.28 €/trim' },
    { category: 'Impact Sur_Co', consumption: '2.4', deltaW: '198.03 €/trim' },
    { category: 'Delta TBSE', consumption: '-42.9', deltaW: '-170.46 €/trim' },
    { category: 'Delta Surplus M', consumption: '-', deltaW: '-781.05 €/trim' }
  ];

  constructor() { }

  ngOnInit(): void {
  }
} 