import {Component, Input, OnInit} from '@angular/core';
import {FundingOther, FundingRexOp, ResultsService} from '../../results.service';

export interface FundingData {
    metric: string;
    general: string;
    percentTotalCost: string;
    isSubHeader?: boolean;
    dae?: string;
    dai?: string;
}

@Component({
    selector: 'app-funding-table',
    templateUrl: './funding-table.component.html',
    styleUrls: ['./funding-table.component.css']
})
export class FundingTableComponent implements OnInit {
    displayedColumns: string[] = ['metric', 'general', 'percentTotalCost'];
    dataSource: FundingData[] = [];
    @Input() simulationId: number | null = 1;

    constructor(private resultsService: ResultsService) {
    }

    ngOnInit(): void {

        this.resultsService.getFundingRexOp(this.simulationId || 1).subscribe({
            next: (rex: FundingRexOp) => {
                this.resultsService.getFundingOther(this.simulationId || 1).subscribe({
                    next: (other: FundingOther) => {
                        this.dataSource = [
                            {
                                metric: 'REX_Op',
                                general: this.formatEuro(rex.general),
                                percentTotalCost: this.formatPercent(rex.total_cost)
                            },
                            {
                                metric: 'Net Contributors',
                                general: '',
                                percentTotalCost: this.formatPercent(other.net_contributors_percent)
                            },
                            {
                                metric: 'Net Beneficiaries',
                                general: '',
                                percentTotalCost: this.formatPercent(other.net_beneficiaries_percent)
                            },
                            {
                                metric: 'Subsididized basic C',
                                general: '',
                                percentTotalCost: this.formatPercent(other.subsidized_basic_c_percent)
                            },
                            {
                                metric: 'Subsididized non basic C',
                                general: '',
                                percentTotalCost: this.formatPercent(other.subsidized_non_basic_c_percent)
                            },
                            {
                                metric: 'Margined C',
                                general: '',
                                percentTotalCost: this.formatPercent(other.margined_c_percent),
                            },
                            {
                                metric: '',
                                general: 'DAE',
                                percentTotalCost: 'DAI',
                                isSubHeader: true
                            },
                            {
                                metric: '"Bad" Sub',
                                general: '',
                                percentTotalCost: '',
                                dae: this.formatPercent(other.bad_sub_percent.dae),
                                dai: this.formatPercent(other.bad_sub_percent.dai)
                            },
                            {
                                metric: '"Bad" Tax',
                                general: '',
                                percentTotalCost: '',
                                dae: this.formatPercent(other.bad_tax_percent.dae),
                                dai: this.formatPercent(other.bad_tax_percent.dai)
                            }
                        ];
                    },
                    error: err => console.error('Error loading funding/other data', err)
                });
            },
            error: err => console.error('Error loading funding/rex_op data', err)
        });
    }

    private formatEuro(value: number | null): string {
        return value !== null ? `${value.toLocaleString('en-US', {minimumFractionDigits: 0})} €` : '-';
    }

    private formatPercent(value: number | null): string {
        return value !== null ? `${value.toFixed(1)} %` : '- %';
    }
}
