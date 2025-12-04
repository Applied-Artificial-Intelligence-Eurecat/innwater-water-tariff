import { Component, OnInit, Input } from '@angular/core';
import { ResultsService, IncentiveConsumptionTable, IncentiveEfficiencyTable } from '../../results.service';

export interface IncentiveEffectData {
  category_metric: string;
  averageConsumption: string;
  averageBill: string;
}

@Component({
  selector: ' app-incentive-effect-table',
  templateUrl: './incentive-effect-table.component.html',
  styleUrls: ['./incentive-effect-table.component.css']
})
export class IncentiveEffectTableComponent implements OnInit {
  displayedColumns: string[] = ['category', 'averageConsumption', 'averageBill'];
  dataSource: IncentiveEffectData[] = [];
  @Input() simulationId: number | null = 1;

  constructor(private resultsService: ResultsService) {}

  ngOnInit(): void {

    this.resultsService.getIncentiveConsumption(this.simulationId || 1).subscribe({
      next: (consumption: IncentiveConsumptionTable) => {
        this.resultsService.getIncentiveEfficiency(this.simulationId || 1).subscribe({
          next: (efficiency: IncentiveEfficiencyTable) => {
            this.dataSource = [
              {
                category_metric: 'IBT',
                averageConsumption: this.format(consumption.ibt.average_consumption_m3_trim),
                averageBill: this.format(consumption.ibt.average_bill_eur_trim)
              },
              {
                category_metric: 'IBT PP',
                averageConsumption: this.format(consumption.ibt_pp.average_consumption_m3_trim),
                averageBill: this.format(consumption.ibt_pp.average_bill_eur_trim)
              },
              {
                category_metric: 'TBSE',
                averageConsumption: this.format(consumption.ibt_tbse.average_consumption_m3_trim),
                averageBill: this.format(consumption.ibt_tbse.average_bill_eur_trim)
              },
              {
                category_metric: '',
                averageConsumption: 'Eff Overconsumption',
                averageBill: 'Eff Mis-mng Cost'
              },
              {
                category_metric: 'per H',
                averageConsumption: this.format(efficiency.per_h.eff_overconsumption),
                averageBill: this.format(efficiency.per_h.eff_mismanagement_cost)
              },
              {
                category_metric: 'per Ind',
                averageConsumption: this.format(efficiency.per_ind.eff_overconsumption),
                averageBill: this.format(efficiency.per_ind.eff_mismanagement_cost)
              }
            ];
          },
          error: err => console.error('Error loading efficiency data', err)
        });
      },
      error: err => console.error('Error loading consumption data', err)
    });
  }

  private format(value: number | null): string {
    return value !== null ? value.toFixed(2) : '-';
  }
}
