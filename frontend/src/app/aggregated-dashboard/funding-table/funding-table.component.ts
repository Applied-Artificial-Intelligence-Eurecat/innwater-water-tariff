import { Component, OnInit } from '@angular/core';
import { ResultsService, FundingRexOp, FundingOther } from '../../results.service';

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
  dataSource: FundingData[] = [];

  constructor(private resultsService: ResultsService) {}

  ngOnInit(): void {
    const simulationId = 2; // replace with dynamic value if needed

    this.resultsService.getFundingRexOp(simulationId).subscribe({
      next: (rex: FundingRexOp) => {
        this.resultsService.getFundingOther(simulationId).subscribe({
          next: (other: FundingOther) => {
            this.dataSource = [
              {
                metric: 'REX_Op',
                general: this.formatEuro(rex.general),
                percentTotalCost: this.formatPercent(rex.total_cost)
              },
              { metric: 'Net Contributors', general: this.formatPercent(other.net_contributors_percent), percentTotalCost: '' },
              { metric: 'Net Beneficiaries', general: this.formatPercent(other.net_beneficiaries_percent), percentTotalCost: '' },
              { metric: 'Subsididized basic C', general: this.formatPercent(other.subsidized_basic_c_percent), percentTotalCost: '' },
              { metric: 'Subsididized non basic C', general: this.formatPercent(other.subsidized_non_basic_c_percent), percentTotalCost: '' },
              { metric: 'Margined C', general: this.formatPercent(other.margined_c_percent), percentTotalCost: '' },
              { metric: '"Bad" Sub', general: this.formatPercent(other.bad_sub_percent), percentTotalCost: '' },
              { metric: '"Bad" Tax', general: this.formatPercent(other.bad_tax_percent), percentTotalCost: '' }
            ];
          },
          error: err => console.error('Error loading funding/other data', err)
        });
      },
      error: err => console.error('Error loading funding/rex_op data', err)
    });
  }

  private formatEuro(value: number | null): string {
    return value !== null ? `${value.toLocaleString('en-US', { minimumFractionDigits: 0 })} €` : '-';
  }

  private formatPercent(value: number | null): string {
    return value !== null ? `${value.toFixed(1)} %` : '- %';
  }
}
