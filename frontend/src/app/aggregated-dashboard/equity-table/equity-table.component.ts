import {Component, OnInit} from '@angular/core';
import {
    BasicConsumptionEquityTable,
    EquityGiniTable,
    FullConsumptionEquityTable,
    ResultsService
} from '../../results.service';

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
    dataSource: EquityData[] = [];

    constructor(private resultsService: ResultsService) {
    }

    ngOnInit(): void {
        const simulationId = 2; // Replace with dynamic ID as needed

        this.resultsService.getEquityGini(simulationId).subscribe({
            next: (gini: EquityGiniTable) => {
                this.resultsService.getBasicConsumptionEquity(simulationId).subscribe({
                    next: (basic: BasicConsumptionEquityTable) => {
                        this.resultsService.getFullConsumptionEquity(simulationId).subscribe({
                            next: (full: FullConsumptionEquityTable) => {
                                this.dataSource = [
                                    {metric: 'Net Income Gini Index', value1: 'IBT', value2: this.format(gini.ibt)},
                                    {metric: '', value1: 'IBT-AE', value2: this.format(gini.ibt_ae)},
                                    {metric: '', value1: 'TBSE', value2: this.format(gini.tbse)},

                                    {metric: '', value1: 'DAE', value2: 'DAI'},
                                    {
                                        metric: 'Net Sub Basic C',
                                        value1: this.formatEuro(basic.net_sub_basic_c.dae),
                                        value2: this.formatEuro(basic.net_sub_basic_c.dai)
                                    },
                                    {
                                        metric: 'Omega Ratio',
                                        value1: this.format(basic.omega_ratio_1.dae),
                                        value2: this.format(basic.omega_ratio_1.dai)
                                    },
                                    {
                                        metric: 'Net Taxes Basic C',
                                        value1: this.formatEuro(basic.net_taxes_basic_c.dae),
                                        value2: this.formatEuro(basic.net_taxes_basic_c.dai)
                                    },
                                    {
                                        metric: 'Omega Ratio',
                                        value1: this.format(basic.omega_ratio_2.dae),
                                        value2: this.format(basic.omega_ratio_2.dai)
                                    },

                                    {metric: '', value1: 'AFE', value2: 'AFI'},
                                    {
                                        metric: 'Net Sub C',
                                        value1: this.formatEuro(full.net_sub_c.afe),
                                        value2: this.formatEuro(full.net_sub_c.afi)
                                    },
                                    {
                                        metric: 'Omega Ratio',
                                        value1: this.format(full.omega_ratio_1.afe),
                                        value2: this.format(full.omega_ratio_1.afi)
                                    },
                                    {
                                        metric: 'Net Taxation',
                                        value1: this.formatEuro(full.net_taxation.afe),
                                        value2: this.formatEuro(full.net_taxation.afi)
                                    },
                                    {
                                        metric: 'Omega Ratio',
                                        value1: this.format(full.omega_ratio_2.afe),
                                        value2: this.format(full.omega_ratio_2.afi)
                                    }
                                ];
                            },
                            error: err => console.error('Failed to load full consumption equity', err)
                        });
                    },
                    error: err => console.error('Failed to load basic consumption equity', err)
                });
            },
            error: err => console.error('Failed to load equity gini', err)
        });
    }

    private format(value: number | null): string {
        return value !== null ? value.toFixed(3) : '-';
    }

    private formatEuro(value: number | null): string {
        return value !== null ? `${value.toFixed(2)} €` : '-';
    }

    isSectionBreak(row: EquityData): boolean {
        return (row.value1 === 'DAE' ||row.value1 === 'AFE') && row.metric === '';
    }

}
