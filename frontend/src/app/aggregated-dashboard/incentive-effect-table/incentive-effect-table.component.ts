import { Component, OnInit } from '@angular/core';
import { ResultsService, IncentiveConsumptionTable, IncentiveEfficiencyTable } from '../../results.service';

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
  dataSource: IncentiveEffectData[] = [];

  constructor(private resultsService: ResultsService) {}

  ngOnInit(): void {
    const simulationId = 2; // Replace with dynamic ID if needed

    this.resultsService.getIncentiveConsumption(simulationId).subscribe({
      next: (consumption: IncentiveConsumptionTable) => {
        this.resultsService.getIncentiveEfficiency(simulationId).subscribe({
          next: (efficiency: IncentiveEfficiencyTable) => {
            this.dataSource = [
              {
                category: 'IBT',
                averageConsumption: this.format(consumption.ibt.average_consumption_m3_trim),
                averageBill: this.format(consumption.ibt.average_bill_eur_trim)
              },
              {
                category: 'IBT PP',
                averageConsumption: this.format(consumption.ibt_pp.average_consumption_m3_trim),
                averageBill: this.format(consumption.ibt_pp.average_bill_eur_trim)
              },
              {
                category: 'IBT TBSE',
                averageConsumption: this.format(consumption.ibt_tbse.average_consumption_m3_trim),
                averageBill: this.format(consumption.ibt_tbse.average_bill_eur_trim)
              },
              {
                category: '',
                averageConsumption: 'Eff Overconsumption',
                averageBill: 'Eff Mis-mng Cost'
              },
              {
                category: 'per H',
                averageConsumption: this.format(efficiency.per_h.eff_overconsumption),
                averageBill: this.format(efficiency.per_h.eff_mismanagement_cost)
              },
              {
                category: 'per Ind',
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
