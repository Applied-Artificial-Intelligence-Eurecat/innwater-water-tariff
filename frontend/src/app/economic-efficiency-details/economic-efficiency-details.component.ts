import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ResultsService, EconomicEfficiencyDetailsTable, SurplusDeltaRow, SurplusImpactRow } from '../results.service';

@Component({
  selector: 'app-economic-efficiency-details',
  templateUrl: './economic-efficiency-details.component.html',
  styleUrls: ['./economic-efficiency-details.component.css']
})
export class EconomicEfficiencyDetailsComponent implements OnInit {
  simulationId: number | null = null;
  loading = false;
  error: string | null = null;
  
  // Data for the Surplus Delta M IBT vs. TBSE table
  surplusDeltaTableData: any[] = [];
  surplusDeltaColumns: string[] = ['category', 'total', 'g', 'p'];
  
  // Data for the Impact on Sur_Co table
  impactTableData: any[] = [];
  impactColumns: string[] = ['category', 'total', 'overconsumers'];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private resultsService: ResultsService
  ) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      const idParam = params.get('id');
      this.simulationId = idParam ? Number(idParam) : null;
      if (this.simulationId) {
        this.fetchEconomicEfficiencyDetails(this.simulationId);
      }
    });
  }

  private fetchEconomicEfficiencyDetails(id: number): void {
    this.loading = true;
    this.error = null;
    this.resultsService.getEconomicEfficiencyDetails(id).subscribe({
      next: (data: EconomicEfficiencyDetailsTable) => {
        this.prepareSurplusDeltaTable(data);
        this.prepareImpactTable(data);
        this.loading = false;
      },
      error: err => {
        this.error = 'Failed to load economic efficiency details data';
        console.error(err);
        this.loading = false;
      }
    });
  }

  private prepareSurplusDeltaTable(data: EconomicEfficiencyDetailsTable): void {
    // First row: percentages
    this.surplusDeltaTableData = [
      {
        category: 'IBT A Delta',
        total: this.formatPercent(data.ibt_a_delta.total_percent),
        g: this.formatPercent(data.ibt_a_delta.g_percent),
        p: this.formatPercent(data.ibt_a_delta.p_percent),
        isPercentRow: true
      },
      {
        category: '',
        total: this.formatEuro(data.ibt_a_delta.total_value),
        g: this.formatEuro(data.ibt_a_delta.g_value),
        p: this.formatEuro(data.ibt_a_delta.p_value),
        isPercentRow: false
      },
      {
        category: 'IBT A PP Delta',
        total: this.formatPercent(data.ibt_a_pp_delta.total_percent),
        g: this.formatPercent(data.ibt_a_pp_delta.g_percent),
        p: this.formatPercent(data.ibt_a_pp_delta.p_percent),
        isPercentRow: true
      },
      {
        category: '',
        total: this.formatEuro(data.ibt_a_pp_delta.total_value),
        g: this.formatEuro(data.ibt_a_pp_delta.g_value),
        p: this.formatEuro(data.ibt_a_pp_delta.p_value),
        isPercentRow: false
      }
    ];
  }

  private prepareImpactTable(data: EconomicEfficiencyDetailsTable): void {
    this.impactTableData = [
      {
        category: 'Impact on Sur_Co',
        total: this.formatEuro(data.impact_on_sur_co.total),
        overconsumers: this.formatEuro(data.impact_on_sur_co.overconsumers)
      }
    ];
  }

  private formatPercent(value: number | null): string {
    return value !== null ? `${value.toFixed(1)}%` : '-';
  }

  private formatEuro(value: number | null): string {
    return value !== null ? `${value.toFixed(2)} €` : '-';
  }

  /**
   * Navigate to the simulation details page for the current simulation
   */
  goToSimulationDetails(): void {
    if (this.simulationId) {
      this.router.navigate(['/simulation/details', this.simulationId]);
    }
  }
}