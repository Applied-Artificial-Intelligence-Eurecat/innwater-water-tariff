import { Component, OnInit } from '@angular/core';

export interface IncentiveEffectData {
  category: string;
  averageConsumption: string;
  averageBill: string;
}

@Component({
  selector: 'app-incentive-effect-table',
  templateUrl: './incentive-effect-table.component.html',
  styleUrls: ['./incentive-effect-table.component.css']
})
export class IncentiveEffectTableComponent implements OnInit {
  displayedColumns: string[] = ['category', 'averageConsumption', 'averageBill'];
  dataSource: IncentiveEffectData[] = [
    { category: 'IBT', averageConsumption: '40.9', averageBill: '91.6' },
    { category: 'IBT PP', averageConsumption: '38.5', averageBill: '73.8' },
    { category: 'IBT TBSE', averageConsumption: '47.5', averageBill: '95.8' },
    { category: 'Eff Overconsumption', averageConsumption: '-', averageBill: '-' },
    { category: 'Eff Mis-mng Cost', averageConsumption: '-', averageBill: '-' },
    { category: 'per H', averageConsumption: '6.7', averageBill: '19.8' },
    { category: 'per Ind', averageConsumption: '2.3', averageBill: '2.3' }
  ];

  constructor() { }

  ngOnInit(): void {
  }
} 