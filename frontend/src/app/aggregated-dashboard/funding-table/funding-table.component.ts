import { Component, OnInit } from '@angular/core';

export interface FundingData {
  metric: string;
  general: string;
  percentTotalCost: string;
}

@Component({
  selector: 'app-funding-table',
  templateUrl: './funding-table.component.html',
  styleUrls: ['./funding-table.component.css']
})
export class FundingTableComponent implements OnInit {
  displayedColumns: string[] = ['metric', 'general', 'percentTotalCost'];
  dataSource: FundingData[] = [
    { metric: 'REX_Op', general: '-179,449 €', percentTotalCost: '-0.8%' },
    { metric: '% H', general: '-', percentTotalCost: '-' },
    { metric: 'Net Contributors', general: '42.8', percentTotalCost: '' },
    { metric: 'Net Beneficiaries', general: '57.2', percentTotalCost: '' },
    { metric: 'Subsididized basic C (en %)', general: '69.20', percentTotalCost: '' },
    { metric: 'Subsididized non basic C (en %)', general: '41.6', percentTotalCost: '' },
    { metric: 'Margined C (en %)', general: '34.5', percentTotalCost: '' },
    { metric: 'In %', general: '-', percentTotalCost: '' },
    { metric: '"Bad" Sub', general: '0.1', percentTotalCost: '' },
    { metric: '"Bad" Tax', general: '18.2', percentTotalCost: '' }
  ];

  constructor() { }

  ngOnInit(): void {
  }
} 