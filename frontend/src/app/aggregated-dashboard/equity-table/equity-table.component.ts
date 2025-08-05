import {Component, OnInit} from '@angular/core';

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
    dataSource = [
        {metric: 'Net Income Gini Index', value1: 'IBT', value2: '0.491'},
        {metric: '', value1: 'IBT-AE', value2: '0.491'},
        {metric: '', value1: 'TBSE', value2: '0.494'},

        {metric: '', value1: 'DAE', value2: ' DAI'},
        {metric: 'Net Sub Basic C', value1: '0.09 €', value2: '41.65 €'},
        {metric: 'Omega Ratio', value1: '0.67', value2: '0.97'},
        {metric: 'Net Taxes Basic C', value1: '9.43 €', value2: '0.00 €'},
        {metric: 'Omega Ratio', value1: '1.26', value2: '***'},

        {metric: '', value1: 'AFE', value2: 'AFI'},
        {metric: 'Net Sub C', value1: '0.00 €', value2: '12.18 €'},
        {metric: 'Omega Ratio', value1: '2.12', value2: '1.31'},
        {metric: 'Net Taxation', value1: '50.98 €', value2: '12.17 €'},
        {metric: 'Omega Ratio', value1: '0.85', value2: '0.58'}
    ];

    constructor() {
    }

    ngOnInit(): void {
    }
} 