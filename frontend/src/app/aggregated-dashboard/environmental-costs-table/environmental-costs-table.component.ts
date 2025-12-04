import {Component, Input, OnInit} from '@angular/core';
import { ResultsService, EnvironmentalCostTable } from '../../results.service';

export interface EnvironmentalCostsData {
  category: string;
  value: string;
}

@Component({
  selector: 'app-environmental-costs-table',
  templateUrl: './environmental-costs-table.component.html',
  styleUrls: ['./environmental-costs-table.component.css']
})
export class EnvironmentalCostsTableComponent implements OnInit {
  displayedColumns: string[] = ['category', 'value'];
  dataSource: EnvironmentalCostsData[] = [];
  @Input() simulationId!: number | null;

  constructor(private resultsService: ResultsService) {}

  ngOnInit(): void {
    const simulationId = this.simulationId!; // Replace with dynamic value if needed

    this.resultsService.getEnvironmentalCost(simulationId).subscribe({
      next: (data: EnvironmentalCostTable) => {
        this.dataSource = [
          { category: 'TBSE Conso Rang 1', value: this.formatEuro(data.tbse_conso_rang_1) },
          { category: 'Effective TBSE', value: this.formatEuro(data.effective_tbse) },
          { category: 'IBT', value: this.formatEuro(data.ibt) },
          { category: 'IBT PP', value: this.formatEuro(data.ibt_pp) }
        ];
      },
      error: (err) => {
        console.error('Failed to load environmental cost data', err);
      }
    });
  }

  private formatEuro(value: number | null): string {
    return value !== null ? `${value.toFixed(2)} €` : '-';
  }
}
