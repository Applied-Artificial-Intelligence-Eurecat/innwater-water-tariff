import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {AffordabilityParApiService, GeneralParDescriptionResponse, StatParItem, GiniSymMatrixResponse, GiniIndexComparisonResponse} from "../affordability-par-api.service";

@Component({
    selector: 'app-affordability-details',
    templateUrl: './affordability-details.component.html',
    styleUrls: ['./affordability-details.component.css']
})
export class AffordabilityDetailsComponent implements OnInit {
    simulationId: number | null = null;
    loading = false;
    error: string | null = null;

    // General Statistics tab data
    parTableRows: Array<{ label: string; g1_ibt?: number; g2_ibt?: number; g1_tbse?: number; g2_tbse?: number; g1_delta?: number; g2_delta?: number }> = [];
    statsTableRows: Array<{ label: string; g1_ibt?: number; g2_ibt?: number; g1_tbse?: number; g2_tbse?: number }> = [];
    dispersionTableRows: Array<{ label: string; g1_ibt?: number; g2_ibt?: number; g1_tbse?: number; g2_tbse?: number }> = [];

    // Gini Index Comparison tab data
    giniIbtTableRows: Array<{ label: string; value?: number; percent?: number }> = [];
    giniTbseTableRows: Array<{ label: string; value?: number; percent?: number }> = [];
    excessGiniIbtTableRows: Array<{ label: string; value?: number; percent?: number }> = [];
    excessGiniTbseTableRows: Array<{ label: string; value?: number; percent?: number }> = [];

    constructor(
        private route: ActivatedRoute,
        private router: Router,
        private affordabilityParService: AffordabilityParApiService
    ) {}

    ngOnInit(): void {
        this.route.paramMap.subscribe(params => {
            const idParam = params.get('id');
            this.simulationId = idParam ? Number(idParam) : null;
            if (this.simulationId) {
                this.fetchGeneralParDescription(this.simulationId);
                this.fetchGiniData(this.simulationId);
            }
        });
    }

    private fetchGeneralParDescription(id: number): void {
        this.loading = true;
        this.error = null;
        this.affordabilityParService.getGeneralParDescription(id).subscribe({
            next: (data: GeneralParDescriptionResponse) => {
                this.prepareGeneralStatTables(data);
                this.loading = false;
            },
            error: err => {
                this.error = 'Failed to load data';
                console.error(err);
                this.loading = false;
            }
        });
    }

    private prepareGeneralStatTables(data: GeneralParDescriptionResponse): void {
        // Process data for PAR table
        this.parTableRows = [
            {
                label: 'Mean',
                g1_ibt: data.mean.par_ibt_g1,
                g2_ibt: data.mean.par_ibt_g2,
                g1_tbse: data.mean.par_tbse_g1,
                g2_tbse: data.mean.par_tbse_g2,
                g1_delta: data.mean.delta_par_g1,
                g2_delta: data.mean.delta_par_g2
            },
            {
                label: 'Median',
                g1_ibt: data.median.par_ibt_g1,
                g2_ibt: data.median.par_ibt_g2,
                g1_tbse: data.median.par_tbse_g1,
                g2_tbse: data.median.par_tbse_g2,
                g1_delta: data.median.delta_par_g1,
                g2_delta: data.median.delta_par_g2
            }
        ];

        // Process data for Statistics table
        this.statsTableRows = [
            {
                label: 'Min',
                g1_ibt: data.min.par_ibt_g1,
                g2_ibt: data.min.par_ibt_g2,
                g1_tbse: data.min.par_tbse_g1,
                g2_tbse: data.min.par_tbse_g2
            },
            {
                label: 'Max',
                g1_ibt: data.max.par_ibt_g1,
                g2_ibt: data.max.par_ibt_g2,
                g1_tbse: data.max.par_tbse_g1,
                g2_tbse: data.max.par_tbse_g2
            },
            {
                label: 'Q1',
                g1_ibt: data.q1.par_ibt_g1,
                g2_ibt: data.q1.par_ibt_g2,
                g1_tbse: data.q1.par_tbse_g1,
                g2_tbse: data.q1.par_tbse_g2
            },
            {
                label: 'Q3',
                g1_ibt: data.q3.par_ibt_g1,
                g2_ibt: data.q3.par_ibt_g2,
                g1_tbse: data.q3.par_tbse_g1,
                g2_tbse: data.q3.par_tbse_g2
            },
            {
                label: 'D1',
                g1_ibt: data.d1.par_ibt_g1,
                g2_ibt: data.d1.par_ibt_g2,
                g1_tbse: data.d1.par_tbse_g1,
                g2_tbse: data.d1.par_tbse_g2
            },
            {
                label: 'D9',
                g1_ibt: data.d9.par_ibt_g1,
                g2_ibt: data.d9.par_ibt_g2,
                g1_tbse: data.d9.par_tbse_g1,
                g2_tbse: data.d9.par_tbse_g2
            },
            {
                label: 'F (Mean)',
                g1_ibt: data.f.par_ibt_g1,
                g2_ibt: data.f.par_ibt_g2,
                g1_tbse: data.f.par_tbse_g1,
                g2_tbse: data.f.par_tbse_g2
            }
        ];

        // Process data for Dispersion table
        this.dispersionTableRows = [
            {
                label: 'Variance',
                g1_ibt: data.variance.par_ibt_g1,
                g2_ibt: data.variance.par_ibt_g2,
                g1_tbse: data.variance.par_tbse_g1,
                g2_tbse: data.variance.par_tbse_g2
            },
            {
                label: 'Écart-type',
                g1_ibt: data.ecart_type.par_ibt_g1,
                g2_ibt: data.ecart_type.par_ibt_g2,
                g1_tbse: data.ecart_type.par_tbse_g1,
                g2_tbse: data.ecart_type.par_tbse_g2
            },
            {
                label: 'MAPE',
                g1_ibt: data.MAPE.par_ibt_g1,
                g2_ibt: data.MAPE.par_ibt_g2,
                g1_tbse: data.MAPE.par_tbse_g1,
                g2_tbse: data.MAPE.par_tbse_g2
            },
            {
                label: 'Coefficient variation',
                g1_ibt: data.coeff_variation.par_ibt_g1,
                g2_ibt: data.coeff_variation.par_ibt_g2,
                g1_tbse: data.coeff_variation.par_tbse_g1,
                g2_tbse: data.coeff_variation.par_tbse_g2
            }
        ];
    }

    private fetchGiniData(id: number): void {
        // Fetch Gini Sym Matrix data
        this.affordabilityParService.getGiniSymMatrix(id).subscribe({
            next: (data: GiniSymMatrixResponse) => {
                this.prepareGiniTables(data);
            },
            error: err => {
                console.error('Failed to load Gini data', err);
            }
        });

        // Fetch Gini Index Comparison data
        this.affordabilityParService.getGiniIndexComparison(id).subscribe({
            next: (data: GiniIndexComparisonResponse) => {
                this.prepareGiniIndexComparisonTables(data);
            },
            error: err => {
                console.error('Failed to load Gini Index Comparison data', err);
            }
        });
    }

    private prepareGiniTables(data: GiniSymMatrixResponse): void {
        // Prepare Gini IBT table
        this.giniIbtTableRows = [
            {
                label: 'Between',
                value: data.between,
                percent: data.between_percent
            },
            {
                label: 'Within',
                value: data.within,
                percent: data.within_percent
            },
            {
                label: 'Transvariation',
                value: data.transvariation,
                percent: data.transvariation_percent
            },
            {
                label: 'Ensemble',
                value: data.ensemble,
                percent: data.ensemble_percent
            }
        ];

        // Use the same data for TBSE for now
        this.giniTbseTableRows = [...this.giniIbtTableRows];
    }

    private prepareGiniIndexComparisonTables(data: GiniIndexComparisonResponse): void {
        // Prepare Gini IBT table
        this.giniIbtTableRows = [
            {
                label: 'Between',
                value: data.par_ibt.between.value,
                percent: data.par_ibt.between.perc
            },
            {
                label: 'Within',
                value: data.par_ibt.within.value,
                percent: data.par_ibt.within.perc
            },
            {
                label: 'Transvariation',
                value: data.par_ibt.transvariation.value,
                percent: data.par_ibt.transvariation.perc
            },
            {
                label: 'Ensemble',
                value: data.par_ibt.ensemble.value,
                percent: data.par_ibt.ensemble.perc
            }
        ];

        // Prepare Gini TBSE table
        this.giniTbseTableRows = [
            {
                label: 'Between',
                value: data.par_tbse.between.value,
                percent: data.par_tbse.between.perc
            },
            {
                label: 'Within',
                value: data.par_tbse.within.value,
                percent: data.par_tbse.within.perc
            },
            {
                label: 'Transvariation',
                value: data.par_tbse.transvariation.value,
                percent: data.par_tbse.transvariation.perc
            },
            {
                label: 'Ensemble',
                value: data.par_tbse.ensemble.value,
                percent: data.par_tbse.ensemble.perc
            }
        ];

        // Prepare Excess Gini IBT table
        this.excessGiniIbtTableRows = [
            {
                label: 'Between',
                value: data.excess_par_ibt.between.value,
                percent: data.excess_par_ibt.between.perc
            },
            {
                label: 'Within',
                value: data.excess_par_ibt.within.value,
                percent: data.excess_par_ibt.within.perc
            },
            {
                label: 'Transvariation',
                value: data.excess_par_ibt.transvariation.value,
                percent: data.excess_par_ibt.transvariation.perc
            },
            {
                label: 'Ensemble',
                value: data.excess_par_ibt.ensemble.value,
                percent: data.excess_par_ibt.ensemble.perc
            }
        ];

        // Prepare Excess Gini TBSE table
        this.excessGiniTbseTableRows = [
            {
                label: 'Between',
                value: data.excess_par_tbse.between.value,
                percent: data.excess_par_tbse.between.perc
            },
            {
                label: 'Within',
                value: data.excess_par_tbse.within.value,
                percent: data.excess_par_tbse.within.perc
            },
            {
                label: 'Transvariation',
                value: data.excess_par_tbse.transvariation.value,
                percent: data.excess_par_tbse.transvariation.perc
            },
            {
                label: 'Ensemble',
                value: data.excess_par_tbse.ensemble.value,
                percent: data.excess_par_tbse.ensemble.perc
            }
        ];
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
