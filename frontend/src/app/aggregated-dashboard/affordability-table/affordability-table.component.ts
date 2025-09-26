import {Component, Input, OnInit} from '@angular/core';
import { ResultsService, AffordabilityTable } from '../../results.service';

export interface AffordabilityData {
  metric: string;
  ibt: string;
  tbse: string;
}

@Component({
  selector: 'app-affordability-table',
  templateUrl: './affordability-table.component.html',
  styleUrls: ['./affordability-table.component.css']
})
export class AffordabilityTableComponent implements OnInit {
  displayedColumns: string[] = ['metric', 'ibt', 'tbse'];
  dataSource: AffordabilityData[] = [];
  @Input() simulationId: number | null = null;

  constructor(private resultsService: ResultsService) {}

  ngOnInit(): void {

    this.resultsService.getAffordabilityResults(this.simulationId ||0).subscribe({
      next: (data: AffordabilityTable) => {
        this.dataSource = [
          {
            metric: 'Headcount ratio',
            ibt: `${data.headcount_ratio.ibt}%`,
            tbse: `${data.headcount_ratio.tbse}%`
          },
          {
            metric: 'App. Afford. Deft',
            ibt: `${data.apparent_affordability_deficit.ibt} €`,
            tbse: `${data.apparent_affordability_deficit.tbse} €`
          },
          {
            metric: 'Effec. Afford. Defit',
            ibt: `${data.effective_affordability_deficit.ibt} €`,
            tbse: `${data.effective_affordability_deficit.tbse} €`
          },
          {
            metric: 'Gini_App',
            ibt: data.gini_app.ibt.toString(),
            tbse: data.gini_app.tbse.toString()
          },
         
        ];
      },
      error: (err) => {
        console.error('Failed to load affordability data', err);
      }
    });
  }
}
