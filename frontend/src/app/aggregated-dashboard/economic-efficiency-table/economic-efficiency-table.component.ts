import {Component, Input, OnInit} from '@angular/core';
import { ResultsService, EconomicEfficiencyTable } from '../../results.service';

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
  dataSource: EconomicEfficiencyData[] = [];
    @Input() simulationId!: number | null;

  constructor(private resultsService: ResultsService) {}

  ngOnInit(): void {

    this.resultsService.getEconomicEfficiency(this.simulationId!).subscribe({
      next: (data: EconomicEfficiencyTable) => {
        this.dataSource = [
          {
            category: 'First Best',
            consumption: this.format(data.first_best.conso),
            deltaW: this.format(data.first_best.delta_w, true)
          },
          {
            category: 'Delta TBSE A',
            consumption: this.format(data.delta_tbse_a.conso),
            deltaW: this.format(data.delta_tbse_a.delta_w, true)
          },
          {
            category: 'Delta IBT A',
            consumption: this.format(data.delta_ibt_a.conso),
            deltaW: this.format(data.delta_ibt_a.delta_w, true)
          },
          {
            category: 'Delta IBT PP A',
            consumption: this.format(data.delta_ibt_pp_a.conso),
            deltaW: this.format(data.delta_ibt_pp_a.delta_w, true)
          },
          {
            category: 'Impact Overconsumption',
            consumption: this.format(data.impact_overconsumption.conso),
            deltaW: this.format(data.impact_overconsumption.delta_w, true)
          }
        ];
      },
      error: (err) => console.error('Error loading economic efficiency data', err)
    });
  }

  private format(value: number | null, isEuro = false): string {
    if (value === null) return isEuro ? '-' : '-';
    return isEuro ? `${value.toFixed(2)} €` : value.toFixed(2);
  }
}
