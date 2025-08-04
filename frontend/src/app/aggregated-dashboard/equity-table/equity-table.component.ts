import { Component, OnInit } from '@angular/core';

export interface EquityData {
  metric: string;
  value1: string;
  value2: string;
}

@Component({
  selector: 'app-equity-table',
  templateUrl: './equity-table.component.html',
  styleUrls: ['./equity-table.component.css']
})
export class EquityTableComponent implements OnInit {
  displayedColumns: string[] = ['metric', 'value1', 'value2'];
  dataSource: EquityData[] = [
    { metric: 'IBT', value1: '0.491', value2: '' },
    { metric: 'IBT-AE', value1: '0.491', value2: '' },
    { metric: 'TBSE', value1: '0.494', value2: '' },
    { metric: 'Net Sub Basic C', value1: '0.09 € (DAE)', value2: '41.65 € (DAI)' },
    { metric: 'Omega ratio', value1: '0.67 (DAE)', value2: '0.97 (DAI)' },
    { metric: 'Net Taxes Basic C', value1: '9.43 € (DAE)', value2: '0.00 € (DAI)' },
    { metric: 'Omega ratio', value1: '1.26 (DAE)', value2: '*** (DAI)' },
    { metric: 'Net Sub C', value1: '0.00 € (AFE)', value2: '12.18 € (AFI)' },
    { metric: 'Omega ratio', value1: '2.12 (AFE)', value2: '1.31 (AFI)' },
    { metric: 'Net Taxation', value1: '50.98 € (AFE)', value2: '12.17 € (AFI)' },
    { metric: 'Oméga ratio', value1: '0.85 (AFE)', value2: '0.58 (AFI)' }
  ];

  constructor() { }

  ngOnInit(): void {
  }
} 