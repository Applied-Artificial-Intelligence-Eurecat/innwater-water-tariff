import {Component, Input, OnInit, OnDestroy} from '@angular/core';
import {
    AffordabilityParApiService,
    AffordabilityDeficitItem,
    DeficitApparentResponse,
    InequalityGiniItem,
    StatParItem,
    GiniSymMatrixItem,
    GiniSymMatrixResponse,
    IncidenceParItem,
    TfParItem,
    TfInegParGiniPdsItem,
    TfInegParGiniCtrIBTResponse,
    TfInegParGiniCtrResponse,
    TfInegParGiniPctItem,
    TfInegParGiniPctResponse,
    TfParResponse,
    IncidenceParResponse,
    AffordabilityDeficitResponse,
    InequalityGiniResponse,
    TfInegParGiniPdsResponse
} from "../../affordability-par-api.service";
import {
    AffordabilityCarApiService,
    CarMetricsItem,
    CarMetricsResponse,
    CarInequalityItem,
    CarInequalityResponse,
    IncidenceCarItem,
    IncidenceCarResponse
} from "../../affordability-car-api.service";
import {ChatDataProvider} from "../../interfaces/chat-data-provider.interface";
import {ChatService} from "../../services/chat.service";
import {TableData} from "../../interfaces/table-data.interface";


interface AffordabilityPar {
    incidence: AffordabilityDeficitItem[]
}


// Interface for the transformed TfInegParGiniCtrIBT data for mat-table
interface TfInegParGiniCtrIBTTableItem {
    rowLabel: string;
    g1ParIbtValue: number;
    g2ParIbtValue: number;
}

// Interface for the transformed TfInegParGiniCtr data for mat-table
interface TfInegParGiniCtrTableItem {
    rowLabel: string;
    g1ParTbseValue: number;
    g2ParTbseValue: number;
}

// Interface for the transformed TfInegParGiniPct data for mat-table
interface TfInegParGiniPctTableItem {
    rowLabel: string;
    g1Value: number;
    g2Value: number;
}


@Component({
    selector: 'app-affordability',
    templateUrl: './affordability.component.html',
    styleUrls: ['./affordability.component.css']
})
export class AffordabilityComponent implements OnInit, OnDestroy, ChatDataProvider {

    deficitEffectif: AffordabilityDeficitItem[] = [];
    deficitApparent: AffordabilityDeficitItem[] = [];
    giniData: InequalityGiniItem[] = [];
    statParData: StatParItem[] = [];
    giniSymMatrixData: GiniSymMatrixItem[] = [];
    incidenceParData: IncidenceParItem[] = [];
    tfParData: TfParItem[] = [];
    tfInegParGiniPdsData: TfInegParGiniPdsItem[] = [];
    tfInegParGiniCtrIBTData: TfInegParGiniCtrIBTResponse | null = null;
    tfInegParGiniCtrData: TfInegParGiniCtrResponse | null = null;
    tfInegParGiniPctData: TfInegParGiniPctItem[] = [];
    giniSymMatrixRowLabels: string[] = ['Between', 'Within', 'Transvariation', 'Ensemble'];

    // CAR data
    carMetricsData: CarMetricsItem[] = [];
    carInequalityData: CarInequalityItem[] = [];
    incidenceCarData: IncidenceCarItem[] = [];

    // Column definitions for mat-tables
    statParColumns: string[] = ['Metric', 'PAR_IBT_G1', 'PAR_IBT_G2', 'PAR_TBSEG1', 'PAR_TBSE_G2'];

    // Column definitions for CAR data table
    carMetricsColumns: string[] = ['Metric', 'CAR_IBT_G1', 'CAR_IBT_G2', 'CAR_TBSE_G1', 'CAR_TBSE_G2'];

    // Column definitions for CAR inequality table
    carInequalityColumns: string[] = ['variable', 'G1_car_ibt', 'G2_car_ibt'];

    // Header definitions for the CAR metrics table
    carMetricsHeaderColumns: string[] = ['Metric_header', 'CAR_IBT_header', 'CAR_TBSE_header'];

    // Column definitions for the tf_par table
    tfParColumns: string[] = ['statistique', 'PAR_IBT_G1', 'PAR_IBT_G2', 'PAR_TBSEG1', 'PAR_TBSE_G2', 'Delta_PAR_G1', 'Delta_PAR_G2'];

    // Header definitions for the tf_par table
    tfParHeaderColumns: string[] = ['statistique_header', 'PAR_IBT_header', 'PAR_TBSE_header', 'DELTA_PAR_header'];


    // Column definitions for the incidence table
    incidenceParColumns: string[] = ['f_i_pourcent', 'PAR_IBT_Menages', 'PAR_IBT_Individus', 'PAR_IBT_Enfants',
        'PAR_TBSE_Menages', 'PAR_TBSE_Individus', 'PAR_TBSE_Enfants'];

    deficitApparentColumns: string[] = ['id_projet', 'PAR_IBT', 'PAR_IBT_Moyenne', 'PAR_IBT_Variance',
        'PAR_TBSE_Moyenne', 'PAR_TBSE_Variance', 'Delta', 'Delta_Moyennes_Menages'];

    deficitEffectifColumns: string[] = ['id', 'id_projet', 'PAR_IBT', 'PAR_IBT_Moyenne', 'PAR_IBT_Variance',
        'PAR_TBSE', 'PAR_TBSE_Moyenne', 'PAR_TBSE_Variance',
        'g_j_PAR_IBT', 'g_j_PAR_TBSE', 'Delta', 'Delta_Moyennes_Menages'];

    giniIBTColumns: string[] = ['component', 'value', 'percentage'];
    giniTBSEColumns: string[] = ['component', 'value', 'percentage'];
    giniSymMatrixColumns: string[] = ['rowLabel', 'G1_PAR_TBSE', 'G2_PAR_TBSE'];

    // Column definitions for the tf_ineg_par_gini_pds table
    tfInegParGiniPdsColumns: string[] = ['groupe', 'f_j', 'f_j_cumul', 'alpha_j', 'alpha_j_cumul'];

    // Column definitions for the tf_ineg_par_gini_ctr_IBT table
    tfInegParGiniCtrIBTColumns: string[] = ['rowLabel', 'g1ParIbtValue', 'g2ParIbtValue'];

    // Column definitions for the tf_ineg_par_gini_ctr table
    tfInegParGiniCtrColumns: string[] = ['rowLabel', 'g1ParTbseValue', 'g2ParTbseValue'];

    // Column definitions for the tf_ineg_par_gini_pct table
    tfInegParGiniPctColumns: string[] = ['rowLabel', 'g1Value', 'g2Value'];

    constructor(
        private apiService: AffordabilityParApiService, 
        private carApiService: AffordabilityCarApiService,
        private chatService: ChatService
    ) {
        this.deficitEffectif = []
        this.deficitApparent = []
        this.giniData = []
        this.statParData = []
        this.giniSymMatrixData = []
        this.incidenceParData = []
        this.tfParData = []
        this.tfInegParGiniPdsData = []
        this.tfInegParGiniCtrIBTData = null
        this.tfInegParGiniCtrData = null
        this.tfInegParGiniPctData = []
        this.carMetricsData = []
        this.carInequalityData = []
    }

    /**
     * Converts the Gini Symmetric Matrix data to the TableData format
     */
    convertGiniSymMatrixToTableData(): TableData {
        const data = this.getGiniSymMatrixTableData();
        if (!data || data.length === 0) {
            return {
                tableName: 'Gini Symmetric Matrix',
                columnNames: ['Row', 'G1_PAR_TBSE', 'G2_PAR_TBSE'],
                values: []
            };
        }

        return {
            tableName: 'Gini Symmetric Matrix',
            columnNames: ['Row', 'G1_PAR_TBSE', 'G2_PAR_TBSE'],
            values: data.map(item => [item.rowLabel, item.G1_PAR_TBSE, item.G2_PAR_TBSE])
        };
    }

    /**
     * Converts the TfInegParGiniCtrIBT data to the TableData format
     */
    convertTfInegParGiniCtrIBTToTableData(): TableData {
        const data = this.getTfInegParGiniCtrIBTTableData();
        if (!data || data.length === 0) {
            return {
                tableName: 'TfInegParGiniCtrIBT',
                columnNames: ['Row', 'G1_PAR_IBT', 'G2_PAR_IBT'],
                values: []
            };
        }

        return {
            tableName: 'TfInegParGiniCtrIBT',
            columnNames: ['Row', 'G1_PAR_IBT', 'G2_PAR_IBT'],
            values: data.map(item => [item.rowLabel, item.g1ParIbtValue, item.g2ParIbtValue])
        };
    }

    /**
     * Converts the TfInegParGiniCtr data to the TableData format
     */
    convertTfInegParGiniCtrToTableData(): TableData {
        const data = this.getTfInegParGiniCtrTableData();
        if (!data || data.length === 0) {
            return {
                tableName: 'TfInegParGiniCtr',
                columnNames: ['Row', 'G1_PAR_TBSE', 'G2_PAR_TBSE'],
                values: []
            };
        }

        return {
            tableName: 'TfInegParGiniCtr',
            columnNames: ['Row', 'G1_PAR_TBSE', 'G2_PAR_TBSE'],
            values: data.map(item => [item.rowLabel, item.g1ParTbseValue, item.g2ParTbseValue])
        };
    }

    /**
     * Converts the TfInegParGiniPct data to the TableData format
     */
    convertTfInegParGiniPctToTableData(): TableData {
        const data = this.getTfInegParGiniPctTableData();
        if (!data || data.length === 0) {
            return {
                tableName: 'TfInegParGiniPct',
                columnNames: ['Row', 'G1_Value', 'G2_Value'],
                values: []
            };
        }

        return {
            tableName: 'TfInegParGiniPct',
            columnNames: ['Row', 'G1_Value', 'G2_Value'],
            values: data.map(item => [item.rowLabel, item.g1Value, item.g2Value])
        };
    }

    /**
     * Converts the StatPar data to the TableData format
     */
    convertStatParToTableData(): TableData {
        if (!this.statParData || this.statParData.length === 0) {
            return {
                tableName: 'Statistical Parameters',
                columnNames: ['Metric', 'PAR_IBT_G1', 'PAR_IBT_G2', 'PAR_TBSE_G1', 'PAR_TBSE_G2'],
                values: []
            };
        }

        return {
            tableName: 'Statistical Parameters',
            columnNames: ['Metric', 'PAR_IBT_G1', 'PAR_IBT_G2', 'PAR_TBSE_G1', 'PAR_TBSE_G2'],
            values: this.statParData.map(item => [
                item.statistique,
                item.PAR_IBT_G1,
                item.PAR_IBT_G2,
                item.PAR_TBSEG1,
                item.PAR_TBSE_G2
            ])
        };
    }

    /**
     * Converts the CAR metrics data to the TableData format
     */
    convertCarMetricsToTableData(): TableData {
        if (!this.carMetricsData || this.carMetricsData.length === 0) {
            return {
                tableName: 'CAR Metrics',
                columnNames: ['Metric', 'CAR_IBT_G1', 'CAR_IBT_G2', 'CAR_TBSE_G1', 'CAR_TBSE_G2'],
                values: []
            };
        }

        return {
            tableName: 'CAR Metrics',
            columnNames: ['Metric', 'CAR_IBT_G1', 'CAR_IBT_G2', 'CAR_TBSE_G1', 'CAR_TBSE_G2'],
            values: this.carMetricsData.map(item => [
                item.metric_type,
                item.g1_car_ibt,
                item.g2_car_ibt,
                item.g1_car_tbse,
                item.g2_car_tbse
            ])
        };
    }

    /**
     * Converts the CAR inequality data to the TableData format
     */
    convertCarInequalityToTableData(): TableData {
        if (!this.carInequalityData || this.carInequalityData.length === 0) {
            return {
                tableName: 'CAR Inequality',
                columnNames: ['Variable', 'G1_CAR_IBT', 'G2_CAR_IBT'],
                values: []
            };
        }

        return {
            tableName: 'CAR Inequality',
            columnNames: ['Variable', 'G1_CAR_IBT', 'G2_CAR_IBT'],
            values: this.carInequalityData.map(item => [
                item.variable,
                item.G1_car_ibt,
                item.G2_car_ibt
            ])
        };
    }

    /**
     * Converts the Gini data to the TableData format
     */
    convertGiniDataToTableData(): TableData {
        if (!this.giniData || this.giniData.length === 0) {
            return {
                tableName: 'Inequality Gini',
                columnNames: ['Indicator', 'Value', 'Percentage'],
                values: []
            };
        }

        return {
            tableName: 'Inequality Gini',
            columnNames: ['Indicator', 'Value', 'Percentage'],
            values: this.giniData.map(item => [
                item.indicateur,
                item.G1,
                item.G2
            ])
        };
    }

    /**
     * Converts the TfPar data to the TableData format
     */
    convertTfParToTableData(): TableData {
        if (!this.tfParData || this.tfParData.length === 0) {
            return {
                tableName: 'TF Parameters',
                columnNames: ['Statistic', 'PAR_IBT_G1', 'PAR_IBT_G2', 'PAR_TBSE_G1', 'PAR_TBSE_G2', 'Delta_PAR_G1', 'Delta_PAR_G2'],
                values: []
            };
        }

        return {
            tableName: 'TF Parameters',
            columnNames: ['Statistic', 'PAR_IBT_G1', 'PAR_IBT_G2', 'PAR_TBSE_G1', 'PAR_TBSE_G2', 'Delta_PAR_G1', 'Delta_PAR_G2'],
            values: this.tfParData.map(item => [
                item.statistique,
                item.PAR_IBT_G1,
                item.PAR_IBT_G2,
                item.PAR_TBSEG1,
                item.PAR_TBSE_G2,
                item.Delta_PAR_G1,
                item.Delta_PAR_G2
            ])
        };
    }

    /**
     * Converts the TfInegParGiniPds data to the TableData format
     */
    convertTfInegParGiniPdsToTableData(): TableData {
        if (!this.tfInegParGiniPdsData || this.tfInegParGiniPdsData.length === 0) {
            return {
                tableName: 'TF Ineg Par Gini Pds',
                columnNames: ['Group', 'F_j', 'F_j_cumul', 'Alpha_j', 'Alpha_j_cumul'],
                values: []
            };
        }

        return {
            tableName: 'TF Ineg Par Gini Pds',
            columnNames: ['Group', 'F_j', 'F_j_cumul', 'Alpha_j', 'Alpha_j_cumul'],
            values: this.tfInegParGiniPdsData.map(item => [
                item.groupe,
                item.f_j,
                item.f_j_cumul,
                item.alpha_j,
                item.alpha_j_cumul
            ])
        };
    }

    /**
     * Converts the IncidencePar data to the TableData format
     */
    convertIncidenceParToTableData(): TableData {
        if (!this.incidenceParData || this.incidenceParData.length === 0) {
            return {
                tableName: 'Incidence Parameters',
                columnNames: [
                    'Percentage',
                    'PAR_IBT_Menages',
                    'PAR_IBT_Individus',
                    'PAR_IBT_Enfants',
                    'PAR_TBSE_Menages',
                    'PAR_TBSE_Individus',
                    'PAR_TBSE_Enfants'
                ],
                values: []
            };
        }

        return {
            tableName: 'Incidence Parameters',
            columnNames: [
                'Percentage',
                'PAR_IBT_Menages',
                'PAR_IBT_Individus',
                'PAR_IBT_Enfants',
                'PAR_TBSE_Menages',
                'PAR_TBSE_Individus',
                'PAR_TBSE_Enfants'
            ],
            values: this.incidenceParData.map(item => [
                item.f_i_pourcent,
                item.PAR_IBT_Menages,
                item.PAR_IBT_Individus,
                item.PAR_IBT_Enfants,
                item.PAR_TBSE_Menages,
                item.PAR_TBSE_Individus,
                item.PAR_TBSE_Enfants
            ])
        };
    }

    /**
     * Converts the IncidenceCar data to a format suitable for display in a table
     */
    convertIncidenceCarToTableData(): any[] {
        if (!this.incidenceCarData || this.incidenceCarData.length === 0) {
            return [];
        }

        // Map the data to the required format
        // The first row is EP (Non assaini)
        // The second row is EPA (Assaini)
        // The third row is Ensemble
        return [
            {
                f_i_pourcent: 'EP (Non assaini)',
                PAR_IBT_Menages: this.incidenceCarData[0].EP_CAR,
                PAR_IBT_Individus: this.incidenceCarData[0].EP_CAR,
                PAR_IBT_Enfants: this.incidenceCarData[0].EP_CAR,
                PAR_TBSE_Menages: this.incidenceCarData[0].EP_CAR,
                PAR_TBSE_Individus: this.incidenceCarData[0].EP_CAR,
                PAR_TBSE_Enfants: this.incidenceCarData[0].EP_CAR
            },
            {
                f_i_pourcent: 'EPA (Assaini)',
                PAR_IBT_Menages: this.incidenceCarData[0].EPA_CAR,
                PAR_IBT_Individus: this.incidenceCarData[0].EPA_CAR,
                PAR_IBT_Enfants: this.incidenceCarData[0].EPA_CAR,
                PAR_TBSE_Menages: this.incidenceCarData[0].EPA_CAR,
                PAR_TBSE_Individus: this.incidenceCarData[0].EPA_CAR,
                PAR_TBSE_Enfants: this.incidenceCarData[0].EPA_CAR
            },
            {
                f_i_pourcent: 'Ensemble',
                PAR_IBT_Menages: this.incidenceCarData[0].Ensemble_CAR,
                PAR_IBT_Individus: this.incidenceCarData[0].Ensemble_CAR,
                PAR_IBT_Enfants: this.incidenceCarData[0].Ensemble_CAR,
                PAR_TBSE_Menages: this.incidenceCarData[0].Ensemble_CAR,
                PAR_TBSE_Individus: this.incidenceCarData[0].Ensemble_CAR,
                PAR_TBSE_Enfants: this.incidenceCarData[0].Ensemble_CAR
            }
        ];
    }

    /**
     * Converts the DeficitEffectif data to the TableData format
     */
    convertDeficitEffectifToTableData(): TableData {
        if (!this.deficitEffectif || this.deficitEffectif.length === 0) {
            return {
                tableName: 'Deficit Effectif',
                columnNames: this.deficitEffectifColumns,
                values: []
            };
        }

        // Handle multi-column headers as specified in the requirements
        const columnNames = this.deficitEffectifColumns.map(col => {
            if (col.includes('PAR_IBT') && col !== 'PAR_IBT') {
                return `PAR_IBT - ${col.replace('PAR_IBT_', '')}`;
            } else if (col.includes('PAR_TBSE') && col !== 'PAR_TBSE') {
                return `PAR_TBSE - ${col.replace('PAR_TBSE_', '')}`;
            } else {
                return col;
            }
        });

        return {
            tableName: 'Deficit Effectif',
            columnNames: columnNames,
            values: this.deficitEffectif.map(item =>
                this.deficitEffectifColumns.map(col => item[col as keyof AffordabilityDeficitItem])
            )
        };
    }

    /**
     * Converts the DeficitApparent data to the TableData format
     */
    convertDeficitApparentToTableData(): TableData {
        if (!this.deficitApparent || this.deficitApparent.length === 0) {
            return {
                tableName: 'Deficit Apparent',
                columnNames: this.deficitApparentColumns,
                values: []
            };
        }

        // Handle multi-column headers as specified in the requirements
        const columnNames = this.deficitApparentColumns.map(col => {
            if (col.includes('PAR_IBT') && col !== 'PAR_IBT') {
                return `PAR_IBT - ${col.replace('PAR_IBT_', '')}`;
            } else if (col.includes('PAR_TBSE') && col !== 'PAR_TBSE') {
                return `PAR_TBSE - ${col.replace('PAR_TBSE_', '')}`;
            } else {
                return col;
            }
        });

        return {
            tableName: 'Deficit Apparent',
            columnNames: columnNames,
            values: this.deficitApparent.map(item =>
                this.deficitApparentColumns.map(col => item[col as keyof AffordabilityDeficitItem])
            )
        };
    }

    /**
     * Implements the ChatDataProvider interface.
     * Returns the component's data for use in chat messages.
     */
    getChatData() {
        return {
            componentName: 'AffordabilityComponent',
            pageName: 'affordability',
            data: [
                this.convertGiniSymMatrixToTableData(),
                this.convertTfInegParGiniCtrIBTToTableData(),
                this.convertTfInegParGiniCtrToTableData(),
                this.convertTfInegParGiniPctToTableData(),
                this.convertStatParToTableData(),
                this.convertIncidenceParToTableData(),
                this.convertDeficitEffectifToTableData(),
                this.convertDeficitApparentToTableData(),
                this.convertCarMetricsToTableData(),
                this.convertCarInequalityToTableData(),
                this.convertGiniDataToTableData(),
                this.convertTfParToTableData(),
                this.convertTfInegParGiniPdsToTableData()
            ]
        };
    }

    ngOnDestroy(): void {
        // Unregister this component when it's destroyed
        this.chatService.unregisterComponent('affordability');
    }

    getComponentDescription(): string {
        return "In the context of the water tariff module, groups G1 and G2 are defined based on the type of tariff households are subject to, and these groups are critical for understanding differences in affordability as measured by various statistical metrics. Below is a summary and analysis of these groups, focusing on their characteristics, the affordability metrics used, and the statistics that differentiate them.\n" +
            "\n" +
            "Overview of Groups G1 and G2\n" +
            "Group G1: This group comprises households that are not connected to the sewage network and pay only for the drinking water (EP) tariff. They are generally subject to the Increasing Block Tariff (IBT) system, which is designed to provide subsidies for basic water needs, thus potentially leading to lower affordability ratios.\n" +
            "\n" +
            "Group G2: This group includes households that are connected to the sewage system and pay for both drinking water and wastewater services (EPA tariff). These households may not benefit from the same level of subsidization as those in Group G1, often leading to higher affordability ratios due to the additional costs associated with wastewater services.\n" +
            "\n";
    }

    ngOnInit(): void {
        // Register this component with the chat service
        this.chatService.registerComponent('affordability', this);

        this.apiService.getTfPar().subscribe((response: TfParResponse) => {
            this.tfParData = response.data;
        });


        this.apiService.getStatPar().subscribe((data: StatParItem[]) => {
            this.statParData = data;
        })

        this.apiService.getIncidencePar().subscribe((data: IncidenceParResponse) => {
            this.incidenceParData = data.data.map((item: IncidenceParItem) => {
                return {
                    ...
                        item,
                    PAR_IBT_Menages: item.PAR_IBT_Ménages,
                    PAR_TBSE_Menages: item.PAR_TBSE_Ménages
                }
            });
            this.incidenceParData
        })

        this.apiService.getAffordabilityDeficitEffectif().subscribe((data: AffordabilityDeficitResponse) => {
            this.deficitEffectif = data.data;
        })
        this.apiService.getAffordabilityDeficitApparent().subscribe((data: DeficitApparentResponse) => {
            this.deficitApparent = data.data;
        })
        this.apiService.getInequalityGini().subscribe((data: InequalityGiniResponse) => {
            this.giniData = data.data;
        })

        this.apiService.getGiniSymMatrix().subscribe((data: GiniSymMatrixResponse) => {
            this.giniSymMatrixData = data.data;
        })

        this.apiService.getTfInegParGiniPds().subscribe((data: TfInegParGiniPdsResponse) => {
            this.tfInegParGiniPdsData = data.data;
        })

        this.apiService.getTfInegParGiniCtrIBT().subscribe((data: TfInegParGiniCtrIBTResponse) => {
            this.tfInegParGiniCtrIBTData = data;
        })

        this.apiService.getTfInegParGiniCtr().subscribe((data: TfInegParGiniCtrResponse) => {
            this.tfInegParGiniCtrData = data;
        })

        this.apiService.getTfInegParGiniPct().subscribe((data: TfInegParGiniPctResponse) => {
            this.tfInegParGiniPctData = data.data;
        })

        // Fetch CAR metrics data
        this.carApiService.getCarMetrics().subscribe((data: CarMetricsResponse) => {
            this.carMetricsData = data.data;
        })

        // Fetch CAR inequality data
        this.carApiService.getCarInequality().subscribe((data: CarInequalityResponse) => {
            this.carInequalityData = data.data;
        })

        // Fetch CAR incidence data
        this.carApiService.getIncidenceCar().subscribe((data: IncidenceCarResponse) => {
            this.incidenceCarData = data.data;
        })
    }

    filter(data: InequalityGiniItem[], starts: string) {
        return data.filter(item => item.indicateur.startsWith(starts)).slice(0, 4)
    }

    // Create a data source for the Gini Symmetric Matrix table that combines the row labels with the API data
    getGiniSymMatrixTableData() {
        if (!this.giniSymMatrixData || this.giniSymMatrixData.length === 0) {
            return [];
        }

        return this.giniSymMatrixRowLabels.map((label, index) => {
            if (index < this.giniSymMatrixData.length) {
                return {
                    rowLabel: label,
                    G1_PAR_TBSE: this.giniSymMatrixData[index].G1_PAR_TBSE,
                    G2_PAR_TBSE: this.giniSymMatrixData[index].G2_PAR_TBSE
                };
            } else {
                return {
                    rowLabel: label,
                    G1_PAR_TBSE: 0,
                    G2_PAR_TBSE: 0
                };
            }
        });
    }


    // Create a data source for the TfInegParGiniCtrIBT table
    getTfInegParGiniCtrIBTTableData(): TfInegParGiniCtrIBTTableItem[] {
        if (!this.tfInegParGiniCtrIBTData || !this.tfInegParGiniCtrIBTData.data) {
            return [];
        }

        const data = this.tfInegParGiniCtrIBTData.data;
        const columns = data.groupe_source;

        // Transpose the table: use G1 and G2 as row labels
        return [
            {
                rowLabel: 'G1',
                g1ParIbtValue: data.valeurs[0][0],
                g2ParIbtValue: data.valeurs[1][0]
            },
            {
                rowLabel: 'G2',
                g1ParIbtValue: data.valeurs[0][1],
                g2ParIbtValue: data.valeurs[1][1]
            }
        ];
    }

    // Create a data source for the TfInegParGiniCtr table
    getTfInegParGiniCtrTableData(): TfInegParGiniCtrTableItem[] {
        if (!this.tfInegParGiniCtrData || !this.tfInegParGiniCtrData.data) {
            return [];
        }

        const data = this.tfInegParGiniCtrData.data;

        // Transform the data into a format suitable for display in a table
        return [
            {
                rowLabel: 'G1',
                g1ParTbseValue: data["G1_PAR TBSE"]["G1_PAR TBSE"],
                g2ParTbseValue: data["G1_PAR TBSE"]["G2_PAR TBSE"]
            },
            {
                rowLabel: 'G2',
                g1ParTbseValue: data["G2_PAR TBSE"]["G1_PAR TBSE"],
                g2ParTbseValue: data["G2_PAR TBSE"]["G2_PAR TBSE"]
            }
        ];
    }

    // Create a data source for the TfInegParGiniPct table
    getTfInegParGiniPctTableData(): TfInegParGiniPctTableItem[] {
        if (!this.tfInegParGiniPctData || this.tfInegParGiniPctData.length === 0) {
            return [];
        }

        // Transform the data into a format suitable for display in a table
        // Transpose the table: use G1_PAR and G2_PAR as row labels
        return [
            {
                rowLabel: 'G1',
                g1Value: this.tfInegParGiniPctData[0].g1_par_ibt,
                g2Value: this.tfInegParGiniPctData[1].g1_par_ibt
            },
            {
                rowLabel: 'G2',
                g1Value: this.tfInegParGiniPctData[0].g2_par_ibt,
                g2Value: this.tfInegParGiniPctData[1].g2_par_ibt
            }
        ];
    }
}
