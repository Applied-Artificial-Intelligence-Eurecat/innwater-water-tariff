import {Component, Input, OnInit} from '@angular/core';
import { ResultsService, StateFunding } from '../../results.service';

export interface StateData {
  category: string;
  totalAnnuel: string;
}

@Component({
  selector: 'app-state-table',
  templateUrl: './state-table.component.html',
  styleUrls: ['./state-table.component.css']
})
export class StateTableComponent implements OnInit {
  displayedColumns: string[] = ['category', 'totalAnnuel'];
  dataSource: StateData[] = [];
    @Input() simulationId!: number | null;

  constructor(private resultsService: ResultsService) {}

  ngOnInit(): void {
    const simulationId = this.simulationId!; // Replace with a dynamic ID if needed

    this.resultsService.getStateFunding(simulationId).subscribe({
      next: (data: StateFunding) => {
        this.dataSource = [
          {
            category: 'VAT',
            totalAnnuel: this.formatEuro(data.vat)
          }
        ];
      },
      error: err => {
        console.error('Failed to load state funding data', err);
      }
    });
  }

  private formatEuro(value: number | null): string {
    return value !== null ? `${value.toLocaleString('en-US', { minimumFractionDigits: 0 })} €` : '-';
  }
}
