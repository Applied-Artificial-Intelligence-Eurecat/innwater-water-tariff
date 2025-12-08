import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {AffordabilityParApiService, GeneralParDescriptionResponse, StatParItem, GiniSymMatrixResponse, GiniIndexComparisonResponse, GeneralDescriptiveResponse, GeneralIncidenceResponse, GeneralDeficitsResponse, GeneralInequalityResponse, G1G2IncidenceResponse, G1G2IntensityResponse} from "../affordability-par-api.service";

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

    // General Statistics > Descriptive Statistics tab data
    descriptiveParTableRows: Array<{ label: string; ibt?: number; tbse?: number; delta?: number }> = [];
    descriptiveStatsTableRows: Array<{ label: string; ibt?: number; tbse?: number }> = [];
    descriptiveDispersionTableRows: Array<{ label: string; ibt?: number; tbse?: number }> = [];

    // General Statistics > Incidence tab data
    incidenceTableRows: Array<{ label: string; ibt?: number; tbse?: number; delta?: number }> = [];

    // General Statistics > Intensity tab data
    apparentDeficitTableRows: Array<{ label: string; ibt?: number; tbse?: number; delta?: number }> = [];
    effectiveDeficitTableRows: Array<{ label: string; ibt?: number; tbse?: number; delta?: number }> = [];

    // General Statistics > Inequality tab data
    overallInequalityTableRows: Array<{ label: string; ibt?: number; tbse?: number }> = [];
    unaffordInequalityTableRows: Array<{ label: string; ibt?: number; tbse?: number }> = [];

    // Focus G1 vs G2 > Incidence tab data
    g1g2IncidenceTableRows: Array<{ group: string; percHouseholdsIbt?: number; ibtHouseholds?: number; percPeopleIbt?: number; ibtPeople?: number; percChildrenIbt?: number; ibtChildren?: number; tbseHouseholds?: number; tbsePeople?: number; tbseChildren?: number }> = [];

    // Focus G1 vs G2 > Intensity tab data
    ibtApparentDeficitTableRows: Array<{ group: string; percentage?: number; mean?: number; variance?: number; decomposition?: string }> = [];
    tbseApparentDeficitTableRows: Array<{ group: string; percentage?: number; mean?: number; variance?: number; decomposition?: string }> = [];
    ibtEffectiveDeficitTableRows: Array<{ group: string; percentage?: number; mean?: number; variance?: number; decomposition?: string }> = [];
    tbseEffectiveDeficitTableRows: Array<{ group: string; percentage?: number; mean?: number; variance?: number; decomposition?: string }> = [];

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
                this.fetchGeneralDescriptive(this.simulationId);
                this.fetchGeneralIncidence(this.simulationId);
                this.fetchGeneralDeficits(this.simulationId);
                this.fetchGeneralInequality(this.simulationId);
                this.fetchGiniData(this.simulationId);
                this.fetchG1G2Incidence(this.simulationId);
                this.fetchG1G2Intensity(this.simulationId);
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

    private fetchGeneralDescriptive(id: number): void {
        this.loading = true;
        this.error = null;
        this.affordabilityParService.getGeneralDescriptive(id).subscribe({
            next: (data: GeneralDescriptiveResponse) => {
                this.prepareGeneralDescriptiveTables(data);
                this.loading = false;
            },
            error: err => {
                this.error = 'Failed to load descriptive statistics data';
                console.error(err);
                this.loading = false;
            }
        });
    }

    private prepareGeneralDescriptiveTables(data: GeneralDescriptiveResponse): void {
        // Process data for PAR table
        this.descriptiveParTableRows = [
            {
                label: 'Mean',
                ibt: data.mean.par_ibt,
                tbse: data.mean.par_tbse,
                delta: data.mean.delta_par
            },
            {
                label: 'Median',
                ibt: data.median.par_ibt,
                tbse: data.median.par_tbse,
                delta: data.median.delta_par
            }
        ];

        // Process data for Statistics table
        this.descriptiveStatsTableRows = [
            {
                label: 'Min',
                ibt: data.min.par_ibt,
                tbse: data.min.par_tbse
            },
            {
                label: 'Max',
                ibt: data.max.par_ibt,
                tbse: data.max.par_tbse
            },
            {
                label: 'Q1',
                ibt: data.q1.par_ibt,
                tbse: data.q1.par_tbse
            },
            {
                label: 'Q3',
                ibt: data.q3.par_ibt,
                tbse: data.q3.par_tbse
            },
            {
                label: 'D1',
                ibt: data.d1.par_ibt,
                tbse: data.d1.par_tbse
            },
            {
                label: 'D9',
                ibt: data.d9.par_ibt,
                tbse: data.d9.par_tbse
            },
            {
                label: 'F (Mean)',
                ibt: data.f.par_ibt,
                tbse: data.f.par_tbse
            }
        ];

        // Process data for Dispersion table
        this.descriptiveDispersionTableRows = [
            {
                label: 'Variance',
                ibt: data.variance.par_ibt,
                tbse: data.variance.par_tbse
            },
            {
                label: 'Écart-type',
                ibt: data.ecart_type.par_ibt,
                tbse: data.ecart_type.par_tbse
            },
            {
                label: 'MAPE',
                ibt: data.MAPE.par_ibt,
                tbse: data.MAPE.par_tbse
            },
            {
                label: 'Coefficient variation',
                ibt: data.coeff_variation.par_ibt,
                tbse: data.coeff_variation.par_tbse
            }
        ];
    }

    private fetchGeneralIncidence(id: number): void {
        this.loading = true;
        this.error = null;
        this.affordabilityParService.getGeneralIncidence(id).subscribe({
            next: (data: GeneralIncidenceResponse) => {
                this.prepareIncidenceTable(data);
                this.loading = false;
            },
            error: err => {
                this.error = 'Failed to load incidence data';
                console.error(err);
                this.loading = false;
            }
        });
    }

    private prepareIncidenceTable(data: GeneralIncidenceResponse): void {
        // Process data for Incidence table
        this.incidenceTableRows = [
            {
                label: 'Households',
                ibt: data.household.par_ibt,
                tbse: data.household.par_tbse,
                delta: data.household.delta_par
            },
            {
                label: 'Individuals',
                ibt: data.people.par_ibt,
                tbse: data.people.par_tbse,
                delta: data.people.delta_par
            },
            {
                label: 'Children',
                ibt: data.children.par_ibt,
                tbse: data.children.par_tbse,
                delta: data.children.delta_par
            }
        ];
    }

    private fetchGeneralDeficits(id: number): void {
        this.loading = true;
        this.error = null;
        this.affordabilityParService.getGeneralDeficits(id).subscribe({
            next: (data: GeneralDeficitsResponse) => {
                this.prepareDeficitTables(data);
                this.loading = false;
            },
            error: err => {
                this.error = 'Failed to load deficit data';
                console.error(err);
                this.loading = false;
            }
        });
    }

    private prepareDeficitTables(data: GeneralDeficitsResponse): void {
        // Process data for Apparent Deficit table
        this.apparentDeficitTableRows = [
            {
                label: 'Mean',
                ibt: data.apparent.mean.par_ibt,
                tbse: data.apparent.mean.par_tbse,
                delta: data.apparent.mean.delta_par
            },
            {
                label: 'Median',
                ibt: data.apparent.median.par_ibt,
                tbse: data.apparent.median.par_tbse
            },
            {
                label: 'D1',
                ibt: data.apparent.d1.par_ibt,
                tbse: data.apparent.d1.par_tbse
            },
            {
                label: 'D9',
                ibt: data.apparent.d9.par_ibt,
                tbse: data.apparent.d9.par_tbse
            },
            {
                label: 'Variance',
                ibt: data.apparent.variance.par_ibt,
                tbse: data.apparent.variance.par_tbse
            },
            {
                label: 'Std. deviation',
                ibt: data.apparent.ecart_type.par_ibt,
                tbse: data.apparent.ecart_type.par_tbse
            },
            {
                label: 'CV',
                ibt: data.apparent.cv.par_ibt,
                tbse: data.apparent.cv.par_tbse
            },
            {
                label: 'MAPE',
                ibt: data.apparent.mape.par_ibt,
                tbse: data.apparent.mape.par_tbse
            }
        ];

        // Process data for Effective Deficit table
        this.effectiveDeficitTableRows = [
            {
                label: 'Mean',
                ibt: data.effective.mean.par_ibt,
                tbse: data.effective.mean.par_tbse,
                delta: data.effective.mean.delta_par
            },
            {
                label: 'Median',
                ibt: data.effective.median.par_ibt,
                tbse: data.effective.median.par_tbse
            },
            {
                label: 'D1',
                ibt: data.effective.d1.par_ibt,
                tbse: data.effective.d1.par_tbse
            },
            {
                label: 'D9',
                ibt: data.effective.d9.par_ibt,
                tbse: data.effective.d9.par_tbse
            },
            {
                label: 'Variance',
                ibt: data.effective.variance.par_ibt,
                tbse: data.effective.variance.par_tbse
            },
            {
                label: 'Std. deviation',
                ibt: data.effective.ecart_type.par_ibt,
                tbse: data.effective.ecart_type.par_tbse
            },
            {
                label: 'CV',
                ibt: data.effective.cv.par_ibt,
                tbse: data.effective.cv.par_tbse
            },
            {
                label: 'MAPE',
                ibt: data.effective.mape.par_ibt,
                tbse: data.effective.mape.par_tbse
            }
        ];
    }

    private fetchGeneralInequality(id: number): void {
        this.loading = true;
        this.error = null;
        this.affordabilityParService.getGeneralInequality(id).subscribe({
            next: (data: GeneralInequalityResponse) => {
                this.prepareInequalityTables(data);
                this.loading = false;
            },
            error: err => {
                this.error = 'Failed to load inequality data';
                console.error(err);
                this.loading = false;
            }
        });
    }

    private prepareInequalityTables(data: GeneralInequalityResponse): void {
        // Process data for Overall population table
        this.overallInequalityTableRows = [
            {
                label: 'Gini',
                ibt: data.all.gini.par_ibt,
                tbse: data.all.gini.par_tbse
            },
            {
                label: 'Schutz',
                ibt: data.all.schutz.par_ibt,
                tbse: data.all.schutz.par_tbse
            }
        ];

        // Process data for Households Facing an Affordability Problem table
        this.unaffordInequalityTableRows = [
            {
                label: 'Gini',
                ibt: data.unafford.gini.par_ibt,
                tbse: data.unafford.gini.par_tbse
            },
            {
                label: 'Schutz',
                ibt: data.unafford.schutz.par_ibt,
                tbse: data.unafford.schutz.par_tbse
            }
        ];
    }

    private fetchG1G2Incidence(id: number): void {
        this.loading = true;
        this.error = null;
        this.affordabilityParService.getG1G2Incidence(id).subscribe({
            next: (data: G1G2IncidenceResponse) => {
                this.prepareG1G2IncidenceTable(data);
                this.loading = false;
            },
            error: err => {
                this.error = 'Failed to load G1 vs G2 incidence data';
                console.error(err);
                this.loading = false;
            }
        });
    }

    private prepareG1G2IncidenceTable(data: G1G2IncidenceResponse): void {
        // Process data for G1 vs G2 Incidence table
        this.g1g2IncidenceTableRows = [
            {
                group: 'G1',
                percHouseholdsIbt: data.g1.perc_household * 100,
                ibtHouseholds: data.g1.ibt_household,
                percPeopleIbt: data.g1.perc_people,
                ibtPeople: data.g1.ibt_people,
                percChildrenIbt: data.g1.perc_children,
                ibtChildren: data.g1.ibt_children,
                tbseHouseholds: data.g1.tbse_household,
                tbsePeople: data.g1.tbse_people,
                tbseChildren: data.g1.tbse_children
            },
            {
                group: 'G2',
                percHouseholdsIbt: data.g2.perc_household * 100,
                ibtHouseholds: data.g2.ibt_household,
                percPeopleIbt: data.g2.perc_people,
                ibtPeople: data.g2.ibt_people,
                percChildrenIbt: data.g2.perc_children,
                ibtChildren: data.g2.ibt_children,
                tbseHouseholds: data.g2.tbse_household,
                tbsePeople: data.g2.tbse_people,
                tbseChildren: data.g2.tbse_children
            },
            {
                group: 'Total',
                percHouseholdsIbt: data.total.perc_household,
                ibtHouseholds: data.total.ibt_household,
                percPeopleIbt: data.total.perc_people,
                ibtPeople: data.total.ibt_people,
                percChildrenIbt: data.total.perc_children,
                ibtChildren: data.total.ibt_children,
                tbseHouseholds: data.total.tbse_household,
                tbsePeople: data.total.tbse_people,
                tbseChildren: data.total.tbse_children
            }
        ];
    }

    private fetchG1G2Intensity(id: number): void {
        this.loading = true;
        this.error = null;
        this.affordabilityParService.getG1G2Intensity(id).subscribe({
            next: (data: G1G2IntensityResponse) => {
                this.prepareG1G2IntensityTables(data);
                this.loading = false;
            },
            error: err => {
                this.error = 'Failed to load G1 vs G2 intensity data';
                console.error(err);
                this.loading = false;
            }
        });
    }

    private prepareG1G2IntensityTables(data: G1G2IntensityResponse): void {
        // Process data for PAR IBT Deficit Apparent table
        this.ibtApparentDeficitTableRows = [
            {
                group: 'G1',
                percentage: data.apparent.par_ibt.g1.perc,
                mean: data.apparent.par_ibt.g1.mean,
                variance: data.apparent.par_ibt.g1.var,
                decomposition: 'Var Inter'
            },
            {
                group: 'G2',
                percentage: data.apparent.par_ibt.g2.perc,
                mean: data.apparent.par_ibt.g2.mean,
                variance: data.apparent.par_ibt.g2.var,
                decomposition: 'Var intra'
            },
            {
                group: 'Ensemble',
                percentage: data.apparent.par_ibt.ensemble.perc,
                mean: data.apparent.par_ibt.ensemble.mean,
                variance: data.apparent.par_ibt.ensemble.var,
                decomposition: 'Rap. Corr.'
            },
            {
                group: '',
                decomposition: data.apparent.par_ibt.rap_corr.toFixed(2)
            }
        ];

        // Process data for PAR TBSE Deficit Apparent table
        this.tbseApparentDeficitTableRows = [
            {
                group: 'G1',
                percentage: data.apparent.par_tbse.g1.perc,
                mean: data.apparent.par_tbse.g1.mean,
                variance: data.apparent.par_tbse.g1.var,
                decomposition: 'Var Inter'
            },
            {
                group: 'G2',
                percentage: data.apparent.par_tbse.g2.perc,
                mean: data.apparent.par_tbse.g2.mean,
                variance: data.apparent.par_tbse.g2.var,
                decomposition: 'Var intra'
            },
            {
                group: 'Ensemble',
                percentage: data.apparent.par_tbse.ensemble.perc,
                mean: data.apparent.par_tbse.ensemble.mean,
                variance: data.apparent.par_tbse.ensemble.var,
                decomposition: 'Rap. Corr.'
            },
            {
                group: '',
                decomposition: data.apparent.par_tbse.rap_corr.toFixed(2)
            }
        ];

        // Process data for PAR IBT Deficit Effective table
        this.ibtEffectiveDeficitTableRows = [
            {
                group: 'G1',
                percentage: data.effective.par_ibt.g1.perc,
                mean: data.effective.par_ibt.g1.mean,
                variance: data.effective.par_ibt.g1.var,
                decomposition: 'Var Inter'
            },
            {
                group: 'G2',
                percentage: data.effective.par_ibt.g2.perc,
                mean: data.effective.par_ibt.g2.mean,
                variance: data.effective.par_ibt.g2.var,
                decomposition: 'Var intra'
            },
            {
                group: 'Ensemble',
                percentage: data.effective.par_ibt.ensemble.perc,
                mean: data.effective.par_ibt.ensemble.mean,
                variance: data.effective.par_ibt.ensemble.var,
                decomposition: 'Rap. Corr.'
            },
            {
                group: '',
                decomposition: data.effective.par_ibt.rap_corr.toFixed(2)
            }
        ];

        // Process data for PAR TBSE Deficit Effective table
        this.tbseEffectiveDeficitTableRows = [
            {
                group: 'G1',
                percentage: data.effective.par_tbse.g1.perc,
                mean: data.effective.par_tbse.g1.mean,
                variance: data.effective.par_tbse.g1.var,
                decomposition: 'Var Inter'
            },
            {
                group: 'G2',
                percentage: data.effective.par_tbse.g2.perc,
                mean: data.effective.par_tbse.g2.mean,
                variance: data.effective.par_tbse.g2.var,
                decomposition: 'Var intra'
            },
            {
                group: 'Ensemble',
                percentage: data.effective.par_tbse.ensemble.perc,
                mean: data.effective.par_tbse.ensemble.mean,
                variance: data.effective.par_tbse.ensemble.var,
                decomposition: 'Rap. Corr.'
            },
            {
                group: '',
                decomposition: data.effective.par_tbse.rap_corr.toFixed(2)
            }
        ];
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
