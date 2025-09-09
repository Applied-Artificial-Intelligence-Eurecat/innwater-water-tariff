import { Component, OnInit } from '@angular/core';
import { ResultsService, WaterAgency } from '../../results.service';

export interface WaterAgencyData {
  category: string;
  totalAnnuel: string;
}

@Component({
  selector: 'app-water-agency-table',
  templateUrl: './water-agency-table.component.html',
  styleUrls: ['./water-agency-table.component.css']
})
export class WaterAgencyTableComponent implements OnInit {
  displayedColumns: string[] = ['category', 'totalAnnuel'];
  dataSource: WaterAgencyData[] = [];

  constructor(private resultsService: ResultsService) {}

  ngOnInit(): void {
    const simulationId = 2; // Replace with dynamic value if needed

    this.resultsService.getWaterAgency(simulationId).subscribe({
      next: (data: WaterAgency) => {
        this.dataSource = [
          {
            category: 'Excise duty',
            totalAnnuel: this.formatEuro(data.exercise_duty)
          }
        ];
      },
      error: err => {
        console.error('Error loading water agency data', err);
      }
    });
  }

  private formatEuro(value: number | null): string {
    return value !== null ? `${value.toLocaleString('en-US', { minimumFractionDigits: 0 })} €` : '-';
  }
}
