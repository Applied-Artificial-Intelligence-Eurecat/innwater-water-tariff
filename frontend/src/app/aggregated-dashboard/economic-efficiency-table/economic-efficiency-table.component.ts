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
          { category: 'Average', consumption: '-', deltaW: '-' },
          {
            category: 'First Best',
            consumption: this.format(data.first_best.conso),
            deltaW: this.format(data.first_best.delta_w, true)
          },
          {
            category: 'Delta IBT PP',
            consumption: this.format(data.delta_ibt_pp.conso),
            deltaW: this.format(data.delta_ibt_pp.delta_w, true)
          },
          {
            category: 'Impact Sur_Co',
            consumption: this.format(data.impact_sur_co.conso),
            deltaW: this.format(data.impact_sur_co.delta_w, true)
          },
          {
            category: 'Delta TBSE',
            consumption: this.format(data.delta_tbse.conso),
            deltaW: this.format(data.delta_tbse.delta_w, true)
          },
          {
            category: 'Delta Surplus M',
            consumption: this.format(data.delta_surplus_m.conso),
            deltaW: this.format(data.delta_surplus_m.delta_w, true)
          }
        ];
      },
      error: (err) => console.error('Error loading economic efficiency data', err)
    });
  }

  private format(value: number | null, isEuro = false): string {
    if (value === null) return isEuro ? '-' : '-';
    return isEuro ? `${value.toFixed(2)} €/trim` : value.toFixed(2);
  }
}
