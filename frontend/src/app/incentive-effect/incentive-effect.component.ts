import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {IncentiveEffectService, GeneralDescriptionResponse, DeltaGeneralDescriptionResponse, DecompositionTablesResponseRaw, ContingencyTableResponse, OverconsumptionDecompositionResponse, HouseholdsOverconsumeCompositionResponse, BreakdownOfOverconsumptionCompositionResponse} from '../incentive-effect.service';

@Component({
  selector: 'app-incentive-effect',
  templateUrl: './incentive-effect.component.html',
  styleUrls: ['./incentive-effect.component.css']
})
export class IncentiveEffectComponent implements OnInit {
  simulationId: number | null = null;
  loading = false;
  error: string | null = null;

  // tables data prepared for the template
  leftTableRows: Array<{ label: string; ibt?: number; ibt_pp?: number; tbse?: number } > = [];
  rightTableRows: Array<{ label: string; per_abonne?: number; per_tete?: number }> = [];
  dispersionLeftRows: Array<{ label: string; ibt?: number; ibt_pp?: number; tbse?: number }> = [];
  dispersionRightRows: Array<{ label: string; per_abonne?: number; per_tete?: number }> = [];
  concentrationRows: Array<{ label: string; ibt?: number; ibt_pp?: number; tbse?: number }> = [];

  // delta tables
  deltaTopRows: Array<{ label: string; delta_ibt_plus?: number; delta_ibt_minus?: number; delta_ibt_pp_plus?: number; delta_ibt_pp_minus?: number }> = [];
  deltaDispersionRows: Array<{ label: string; delta_ibt_plus?: number; delta_ibt_minus?: number; delta_ibt_pp_plus?: number; delta_ibt_pp_minus?: number }> = [];
  deltaConcentrationRows: Array<{ label: string; delta_ibt_plus?: number; delta_ibt_minus?: number; delta_ibt_pp_plus?: number; delta_ibt_pp_minus?: number }> = [];

  // decomposition tables
  decompOverallRows: Array<{ label: string; freq?: number; delta_c?: number; variance?: number; vcol?: string; percent?: number }> = [];
  decompG1G2Rows: Array<{ label: string; freq?: number; delta_c?: number; variance?: number; vcol?: string; percent?: number }> = [];
  decompPoorRows: Array<{ label: string; freq?: number; delta_c?: number; variance?: number; vcol?: string; percent?: number }> = [];

  // contingency tables
  contingencyPercentRows: Array<{ label: string; poor?: number; nonpoor?: number; ensemble?: number }> = [];
  contingencyConsumptionRows: Array<{ label: string; poor?: number; nonpoor?: number; ensemble?: number }> = [];

  // overconsumption decomposition
  overDecompMainRows: Array<{ label: string; freq?: number; delta_c?: number; variance?: number; vcol?: string; percent?: number }> = [];
  overDecompHouseholdsRows: Array<{ label: string; poor?: number; nonpoor?: number; ensemble?: number }> = [];
  overDecompBreakdownRows: Array<{ label: string; poor?: number; nonpoor?: number; ensemble?: number }> = [];

  constructor(private route: ActivatedRoute,
              private router: Router,
              private incentiveService: IncentiveEffectService) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      const idParam = params.get('id');
      this.simulationId = idParam ? Number(idParam) : null;
      if (this.simulationId) {
        this.fetchData(this.simulationId);
        this.fetchDelta(this.simulationId);
        this.fetchDecomposition(this.simulationId);
        this.fetchContingency(this.simulationId);
        this.fetchOverconsumptionDecomposition(this.simulationId);
      }
    });
  }

  private fetchData(id: number): void {
    this.loading = true;
    this.error = null;
    this.incentiveService.getGeneralDescription(id).subscribe({
      next: (data: GeneralDescriptionResponse) => {
        this.prepareTables(data);
        this.loading = false;
      },
      error: err => {
        this.error = 'Failed to load data';
        console.error(err);
        this.loading = false;
      }
    });
  }

  private prepareTables(d: GeneralDescriptionResponse): void {
    // Left top table (IBT / IBT PP / TBSE)
    const L = (label: string, m: keyof GeneralDescriptionResponse) => ({
      label,
      ibt: d[m].ibt,
      ibt_pp: d[m].ibt_pp,
      tbse: d[m].tbse
    });
    this.leftTableRows = [
      L('Mean', 'mean'),
      L('Median', 'median'),
      L('Min', 'min'),
      L('Max', 'max'),
      L('Q1', 'q1'),
      L('Q3', 'q3'),
      L('D1', 'd1'),
      L('D9', 'd9'),
      L('F (Mean)', 'percentile_rank'),
    ];

    // Right top table (surconso effective par abonné / par tête)
    const R = (label: string, m: keyof GeneralDescriptionResponse) => ({
      label,
      per_abonne: d[m].actual_overconsumption,
      per_tete: d[m].overconsumption_per_capita
    });
    this.rightTableRows = [
      R('Mean', 'mean'),
      R('Median', 'median'),
      R('Min', 'min'),
      R('Max', 'max'),
      R('Q1', 'q1'),
      R('Q3', 'q3'),
      R('D1', 'd1'),
      R('D9', 'd9'),
      R('F (Mean)', 'percentile_rank'),
    ];

    // Dispersion indicators
    this.dispersionLeftRows = [
      L('Variance', 'variance'),
      L('Standard deviation', 'ecart_type'),
      L('MAPE', 'mape'),
      L('Coefficient of variation', 'variation_coeff'),
      L('Interquartile range', 'iqr'),
      L('Interdecile range', 'idr'),
      L('Yule coefficients', 'yule_coeff'),
    ];
    this.dispersionRightRows = [
      R('Variance', 'variance'),
      R('Standard deviation', 'ecart_type'),
      R('MAPE', 'mape'),
      R('Coefficient of variation', 'variation_coeff'),
      R('Interquartile range', 'iqr'),
      R('Interdecile range', 'idr'),
      R('Yule coefficients', 'yule_coeff'),
    ];

    // Concentration indicators
    this.concentrationRows = [
      L('Gini', 'gini_schutz')
    ];
  }

  private fetchDelta(id: number): void {
    this.incentiveService.getDeltaGeneralDescription(id).subscribe({
      next: (d: DeltaGeneralDescriptionResponse) => this.prepareDeltaTables(d),
      error: err => console.error(err)
    });
  }

  private prepareDeltaTables(d: DeltaGeneralDescriptionResponse): void {
    const D = (label: string, m: keyof DeltaGeneralDescriptionResponse) => ({
      label,
      delta_ibt_plus: d[m].delta_ibt_plus,
      delta_ibt_minus: d[m].delta_ibt_minus,
      delta_ibt_pp_plus: d[m].delta_ibt_pp_plus,
      delta_ibt_pp_minus: d[m].delta_ibt_pp_minus,
    });

    this.deltaTopRows = [
      D('% de Ménage', 'percentile_rank'), // treat as header percentage row when provided
      D('Moyenne', 'mean'),
      D('Médiane', 'median'),
      D('Min', 'min'),
      D('Max', 'max'),
      D('Q1', 'q1'),
      D('Q3', 'q3'),
      D('D1', 'd1'),
      D('D9', 'd9'),
      D('F (Moyenne)', 'percentile_rank'),
    ];

    this.deltaDispersionRows = [
      D('Variance', 'variance'),
      D('Ecart-type', 'ecart_type'),
      D('MAPE', 'mape'),
      D('Coeff de Variation', 'variation_coeff'),
      D('Etendue Interquantiles', 'iqr'),
      D('Etendue Interdéciles', 'idr'),
      D('Coefficients de Yule', 'yule_coeff'),
    ];

    this.deltaConcentrationRows = [
      D('Schutz', 'gini_schutz')
    ];
  }

  private fetchDecomposition(id: number): void {
    this.incentiveService.getDecompositionTables(id).subscribe({
      next: (raw: DecompositionTablesResponseRaw) => this.prepareDecompositionTables(raw),
      error: err => console.error('Failed to load decomposition tables', err)
    });
  }

  private n(x: number | string): number | undefined {
    if (x === null || x === undefined) return undefined;
    const t = typeof x === 'string' ? x : String(x);
    const val = parseFloat(t);
    if (isNaN(val) || t.toLowerCase() === 'nan') return undefined;
    return val;
  }

  private prepareDecompositionTables(raw: DecompositionTablesResponseRaw): void {
    const row = (label: string, e: {frequency: number|string; delta_c_moyen: number|string; variance: number|string}) => ({
      label,
      freq: this.n(e.frequency),
      delta_c: this.n(e.delta_c_moyen),
      variance: this.n(e.variance),
    });

    // Overall table
    this.decompOverallRows = [
      row('All households', raw.ensemble),
      {label: 'Households increasing consumption (broad sense)', freq: this.n(raw.delta_plus.frequency), delta_c: this.n(raw.delta_plus.delta_c_moyen), variance: this.n(raw.delta_plus.variance)},
      {label: 'Households decreasing consumption', freq: this.n(raw.delta_minus.frequency), delta_c: this.n(raw.delta_minus.delta_c_moyen), variance: this.n(raw.delta_minus.variance)},
    ];

    // G1 / G2 table
    this.decompG1G2Rows = [
      row('All households', raw.ensemble),
      row('Increase & G1', raw.g1_delta_plus),
      row('Increase & G2', raw.g2_delta_plus),
      row('Decrease & G1', raw.g1_delta_minus),
      row('Decrease & G2', raw.g2_delta_minus),
    ];

    // Poor / Non poor table
    this.decompPoorRows = [
      row('All households', raw.ensemble),
      row('Increase & Poor', raw.poor_delta_plus),
      row('Increase & Non Poor', raw.nonpoor_delta_plus),
      row('Decrease & Poor', raw.poor_delta_minus),
      row('Decrease & Non Poor', raw.nonpoor_delta_minus),
    ];
  }

  private fetchContingency(id: number): void {
    this.incentiveService.getContingencyTablePercentages(id).subscribe({
      next: (percent: ContingencyTableResponse) => this.prepareContingencyPercent(percent),
      error: err => console.error('Failed to load contingency percentages', err)
    });
    this.incentiveService.getContingencyTableConsumption(id).subscribe({
      next: (consumption: ContingencyTableResponse) => this.prepareContingencyConsumption(consumption),
      error: err => console.error('Failed to load contingency consumption', err)
    });
  }

  private prepareContingencyPercent(data: ContingencyTableResponse): void {
    this.contingencyPercentRows = [
      { label: 'Increase', poor: data.increase.g1.poor, nonpoor: data.increase.g1.nonpoor, ensemble: data.increase.g1.ensemble },
      { label: 'G1 (service EP)', poor: data.increase.g1.poor, nonpoor: data.increase.g1.nonpoor, ensemble: data.increase.g1.ensemble },
      { label: 'G2 (service EPA)', poor: data.increase.g2.poor, nonpoor: data.increase.g2.nonpoor, ensemble: data.increase.g2.ensemble },
      { label: 'Total', poor: data.increase.total_population.poor, nonpoor: data.increase.total_population.nonpoor, ensemble: data.increase.total_population.ensemble },
      { label: 'Decrease', poor: data.decrease.g1.poor, nonpoor: data.decrease.g1.nonpoor, ensemble: data.decrease.g1.ensemble },
      { label: 'G1 (service EP)', poor: data.decrease.g1.poor, nonpoor: data.decrease.g1.nonpoor, ensemble: data.decrease.g1.ensemble },
      { label: 'G2 (service EPA)', poor: data.decrease.g2.poor, nonpoor: data.decrease.g2.nonpoor, ensemble: data.decrease.g2.ensemble },
      { label: 'Total', poor: data.decrease.total_population.poor, nonpoor: data.decrease.total_population.nonpoor, ensemble: data.decrease.total_population.ensemble },
    ];
  }

  // Overconsumption Decomposition Tab
  private fetchOverconsumptionDecomposition(id: number): void {
    this.incentiveService.getOverconsumptionDecomposition(id).subscribe({
      next: (resp: OverconsumptionDecompositionResponse) => {
        const d = resp.decomposed;
        const GV = resp.groups_variance;
        const PV = resp.poor_variance;

        this.overDecompMainRows = [
          { label: '% of households overconsuming', freq: d.households_percentage.frequency, delta_c: d.households_percentage.delta_c_moyen, variance: d.households_percentage.variance, vcol: 'V inter', percent: GV.v_inter },
          { label: 'G1', freq: d.g1.frequency, delta_c: d.g1.delta_c_moyen, variance: d.g1.variance, vcol: 'V intra', percent: GV.v_intra },
          { label: 'G2', freq: d.g2.frequency, delta_c: d.g2.delta_c_moyen, variance: d.g2.variance, vcol: 'Corr. ratio', percent: GV.correlation_ratio },
          { label: 'Poor', freq: d.poor.frequency, delta_c: d.poor.delta_c_moyen, variance: d.poor.variance, vcol: 'V inter', percent: PV.v_inter },
          { label: 'Non-Poor', freq: d.nonpoor.frequency, delta_c: d.nonpoor.delta_c_moyen, variance: d.nonpoor.variance, vcol: 'V intra', percent: PV.v_intra },
        ];
      },
      error: err => console.error('Failed to load overconsumption decomposition', err)
    });

    this.incentiveService.getHouseholdsThatOverconsumeComposition(id).subscribe({
      next: (comp: HouseholdsOverconsumeCompositionResponse) => {
        console.log(comp)
        this.overDecompHouseholdsRows = [
          { label: 'G1 (service EP)', poor: comp.g1.poor, nonpoor: comp.g1.nonpoor, ensemble: comp.g1.ensemble },
          { label: 'G2 (service EPA)', poor: comp.g2.poor, nonpoor: comp.g2.nonpoor, ensemble: comp.g2.ensemble },
          { label: 'Total', poor: comp.total_population.poor, nonpoor: comp.total_population.nonpoor, ensemble: comp.total_population.ensemble },
        ];
      },
      error: err => console.error('Failed to load households that overconsume composition', err)
    });

    this.incentiveService.getBreakdownOfOverconsumptionComposition(id).subscribe({
      next: (b: BreakdownOfOverconsumptionCompositionResponse) => {
        this.overDecompBreakdownRows = [
          { label: 'G1 (service EP)', poor: b.g1.poor, nonpoor: b.g1.nonpoor, ensemble: b.g1.ensemble },
          { label: 'G2 (service EPA)', poor: b.g2.poor, nonpoor: b.g2.nonpoor, ensemble: b.g2.ensemble },
          { label: 'Total', poor: b.total_population.poor, nonpoor: b.total_population.nonpoor, ensemble: b.total_population.ensemble },
        ];
      },
      error: err => console.error('Failed to load breakdown of overconsumption composition', err)
    });
  }

  private prepareContingencyConsumption(data: ContingencyTableResponse): void {
    this.contingencyConsumptionRows = [
      { label: 'Increase', poor: data.increase.g1.poor, nonpoor: data.increase.g1.nonpoor, ensemble: data.increase.g1.ensemble },
      { label: 'G1 (service EP)', poor: data.increase.g1.poor, nonpoor: data.increase.g1.nonpoor, ensemble: data.increase.g1.ensemble },
      { label: 'G2 (service EPA)', poor: data.increase.g2.poor, nonpoor: data.increase.g2.nonpoor, ensemble: data.increase.g2.ensemble },
      { label: 'Total', poor: data.increase.total_population.poor, nonpoor: data.increase.total_population.nonpoor, ensemble: data.increase.total_population.ensemble },
      { label: 'Decrease', poor: data.decrease.g1.poor, nonpoor: data.decrease.g1.nonpoor, ensemble: data.decrease.g1.ensemble },
      { label: 'G1 (service EP)', poor: data.decrease.g1.poor, nonpoor: data.decrease.g1.nonpoor, ensemble: data.decrease.g1.ensemble },
      { label: 'G2 (service EPA)', poor: data.decrease.g2.poor, nonpoor: data.decrease.g2.nonpoor, ensemble: data.decrease.g2.ensemble },
      { label: 'Total', poor: data.decrease.total_population.poor, nonpoor: data.decrease.total_population.nonpoor, ensemble: data.decrease.total_population.ensemble },
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
