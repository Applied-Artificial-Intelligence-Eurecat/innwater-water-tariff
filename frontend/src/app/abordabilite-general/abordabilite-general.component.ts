import {Component, Input, OnInit, OnDestroy} from '@angular/core';
import {ChatDataProvider} from '../interfaces/chat-data-provider.interface';
import {TableData} from '../interfaces/table-data.interface';
import {ChatService} from '../services/chat.service';

// Interface for the PAR statistics table data
export interface GeneralStatisticsItem {
    rowLabel: string;
    parIbt: number;
    parTbse: number;
    deltaPar: number;
}

// Interface for the CAR statistics table data
export interface GeneralStatisticsCarItem {
    rowLabel: string;
    carIbt: number;
    carTbse: number;
    deltaCar: number;
}

// Interface for the other general PAR statistics table data
export interface OtherGeneralStatisticsItem {
    metric: string;
    parIbt: number;
    parTbse: number;
}

// Interface for the other general CAR statistics table data
export interface OtherGeneralStatisticsCarItem {
    metric: string;
    carIbt: number;
    carTbse: number;
}

// Interface for the PAR incidence data
export interface ParIncidenceItem {
    category: string;
    parIbt: number;
    parTbse: number;
    deltaPar: number;
}

// Interface for the CAR incidence data
export interface CarIncidenceItem {
    category: string;
    carIbt: number;
    carTbse: number;
    deltaCar: number;
}

// Interface for the PAR deficit apparent data
export interface DeficitApparentParItem {
    metric: string;
    parIbt: string;
    parTbse: string;
    deltaPar: string;
}

// Interface for the CAR deficit apparent data
export interface DeficitApparentCarItem {
    metric: string;
    carIbt: string;
    carTbse: string;
    deltaCar: string;
}

// Interface for the PAR deficit effectif data
export interface DeficitEffectifParItem {
    metric: string;
    parIbt: string;
    parTbse: string;
    deltaPar: string;
}

// Interface for the CAR deficit effectif data
export interface DeficitEffectifCarItem {
    metric: string;
    carIbt: string;
    carTbse: string;
    deltaCar: string;
}

// Interface for the PAR inegalite data
export interface InegaliteParItem {
    ensemble: string;
    ibt: number;
    tbse: number;
}

// Interface for the CAR inegalite data
export interface InegaliteCarItem {
    ibt: number;
    tbse: number;
}

// Interface for the PAR abordability problem data
export interface AbordabiliteProblemParItem {
    metric: string;
    ibt: number;
    tbse: number;
}

// Interface for the CAR abordability problem data
export interface AbordabiliteProblemCarItem {
    ibt: number;
    tbse: number;
}

@Component({
    selector: 'app-abordabilite-general',
    templateUrl: './abordabilite-general.component.html',
    styleUrls: ['./abordabilite-general.component.css']
})
export class AbordabiliteGeneralComponent implements OnInit, OnDestroy, ChatDataProvider {
    @Input() panelOpenState: boolean = true;

    constructor(private chatService: ChatService) {
    }

    ngOnInit(): void {
        // Register this component with the chat service
        this.chatService.registerComponent('abordabilite-general', this);
    }

    getComponentDescription(): string {
        return "The Affordability module is designed to assess household affordability regarding water services, specifically through the use of economic indicators such as the Potential Affordability Ratio (PAR) and the Conventional Affordability Ratio (CAR) for different tariff systems. These ratios are fundamental for understanding how different segments of the population experience affordability issues, particularly in relation to the Increasing Block Tariff (IBT) and the Traditional Block Tariff (TBSE).";
    }

    ngOnDestroy(): void {
        // Unregister this component when it's destroyed
        this.chatService.unregisterComponent('abordabilite-general');
    }

    // Column definitions for the PAR statistics table
    generalMedianStatisticsColumns: string[] = ['rowLabel', 'parIbt', 'parTbse', 'deltaPar'];

    // Data for the PAR statistics table
    generalMedianStatistics: GeneralStatisticsItem[] = [
        {rowLabel: 'Moyenne', parIbt: 1.1, parTbse: 3.2, deltaPar: -2.0},
        {rowLabel: 'Médiane', parIbt: 0.7, parTbse: 2.0, deltaPar: -1.3}
    ];

    // Method to get the data for the PAR statistics table
    getGeneralMedianStatisticsData(): GeneralStatisticsItem[] {
        return this.generalMedianStatistics;
    }

    // Column definitions for the CAR statistics table
    generalMedianStatisticsCarColumns: string[] = ['rowLabel', 'carIbt', 'carTbse', 'deltaCar'];

    // Data for the CAR statistics table
    generalMedianStatisticsCar: GeneralStatisticsCarItem[] = [
        {rowLabel: 'Moyenne', carIbt: 0.9, carTbse: 2.8, deltaCar: -1.9},
        {rowLabel: 'Médiane', carIbt: 0.5, carTbse: 1.8, deltaCar: -1.3}
    ];

    // Method to get the data for the CAR statistics table
    getGeneralMedianStatisticsCarData(): GeneralStatisticsCarItem[] {
        return this.generalMedianStatisticsCar;
    }

    // Column definitions for the other general PAR statistics table
    otherGeneralStatisticsColumns: string[] = ['metric', 'parIbt', 'parTbse'];

    // Data for the other general PAR statistics table
    otherGeneralStatistics: OtherGeneralStatisticsItem[] = [
        {metric: 'Min', parIbt: 0, parTbse: 0.1},
        {metric: 'Max', parIbt: 10.9, parTbse: 21.9},
        {metric: 'Q1', parIbt: 0.3, parTbse: 0.9},
        {metric: 'Q3', parIbt: 1.4, parTbse: 3.9},
        {metric: 'D1', parIbt: 0.1, parTbse: 0.5},
        {metric: 'D9', parIbt: 2.6, parTbse: 8},
        {metric: 'F (Moyenne)', parIbt: 68.5, parTbse: 69.3},
        {metric: 'Variance', parIbt: 1.89, parTbse: 12.64},
        {metric: 'Ecart-type', parIbt: 1.4, parTbse: 3.6},
        {metric: 'MAPE', parIbt: 0.9, parTbse: 2.5},
        {metric: 'Coeff de Variation', parIbt: 1.216, parTbse: 1.119},
        {metric: 'Etendue Interquantiles', parIbt: 1.1, parTbse: 3},
        {metric: 'Etendue Interdéciles', parIbt: 2.5, parTbse: 7.5},
        {metric: 'Coefficients de Yule', parIbt: 0.29, parTbse: 0.3}
    ];

    // Method to get the data for the other general PAR statistics table
    getOtherGeneralStatisticsData(): OtherGeneralStatisticsItem[] {
        return this.otherGeneralStatistics;
    }

    // Column definitions for the other general CAR statistics table
    otherGeneralStatisticsCarColumns: string[] = ['metric', 'carIbt', 'carTbse'];

    // Data for the other general CAR statistics table
    otherGeneralStatisticsCar: OtherGeneralStatisticsCarItem[] = [
        {metric: 'Min', carIbt: 0, carTbse: 0.2},
        {metric: 'Max', carIbt: 9.5, carTbse: 19.8},
        {metric: 'Q1', carIbt: 0.2, carTbse: 0.7},
        {metric: 'Q3', carIbt: 1.2, carTbse: 3.5},
        {metric: 'D1', carIbt: 0.1, carTbse: 0.4},
        {metric: 'D9', carIbt: 2.3, carTbse: 7.2},
        {metric: 'F (Moyenne)', carIbt: 65.2, carTbse: 67.1},
        {metric: 'Variance', carIbt: 1.65, carTbse: 11.32},
        {metric: 'Ecart-type', carIbt: 1.3, carTbse: 3.4},
        {metric: 'MAPE', carIbt: 0.8, carTbse: 2.3},
        {metric: 'Coeff de Variation', carIbt: 1.185, carTbse: 1.098},
        {metric: 'Etendue Interquantiles', carIbt: 1.0, carTbse: 2.8},
        {metric: 'Etendue Interdéciles', carIbt: 2.2, carTbse: 6.8},
        {metric: 'Coefficients de Yule', carIbt: 0.27, carTbse: 0.28}
    ];

    // Method to get the data for the other general CAR statistics table
    getOtherGeneralStatisticsCarData(): OtherGeneralStatisticsCarItem[] {
        return this.otherGeneralStatisticsCar;
    }

    // Column definitions for the PAR incidence table
    parIncidenceColumns: string[] = ['category', 'parIbt', 'parTbse', 'deltaPar'];

    // Data for the PAR incidence table
    parIncidenceData: ParIncidenceItem[] = [
        {category: 'Ménages', parIbt: 7.9, parTbse: 32.8, deltaPar: -24.9},
        {category: 'Individus', parIbt: 7.9, parTbse: 31.6, deltaPar: -23.8},
        {category: 'Enfants', parIbt: 9.9, parTbse: 35.1, deltaPar: -25.2}
    ];

    // Method to get the data for the PAR incidence table
    getParIncidenceData(): ParIncidenceItem[] {
        return this.parIncidenceData;
    }

    // Column definitions for the CAR incidence table
    carIncidenceColumns: string[] = ['category', 'carIbt', 'carTbse', 'deltaCar'];

    // Data for the CAR incidence table
    carIncidenceData: CarIncidenceItem[] = [
        {category: 'Ménages', carIbt: 28.8, carTbse: 48.3, deltaCar: -19.4},
        {category: 'Individus', carIbt: 32.6, carTbse: 48.9, deltaCar: -16.3},
        {category: 'Enfants', carIbt: 38.0, carTbse: 52.3, deltaCar: -14.3}
    ];

    // Method to get the data for the CAR incidence table
    getCarIncidenceData(): CarIncidenceItem[] {
        return this.carIncidenceData;
    }

    // Column definitions for the PAR deficit apparent table
    deficitApparentParColumns: string[] = ['metric', 'parIbt', 'parTbse', 'deltaPar'];

    // Data for the PAR deficit apparent table
    deficitApparentParData: DeficitApparentParItem[] = [
        {metric: 'Moyenne', parIbt: '1,39€', parTbse: '17,47€', deltaPar: '-16,08€'},
        {metric: 'Médiane', parIbt: '0,00€', parTbse: '0,00€', deltaPar: '0,00€'},
        {metric: 'Variance', parIbt: '38,5366', parTbse: '1013,2596', deltaPar: ''},
        {metric: 'Ecart-type', parIbt: '6,21€', parTbse: '31,83€', deltaPar: ''},
        {metric: 'cv', parIbt: '4,47', parTbse: '1,82', deltaPar: ''},
        {metric: 'MAPE', parIbt: '2,57€', parTbse: '24,49€', deltaPar: ''}
    ];

    // Method to get the data for the PAR deficit apparent table
    getDeficitApparentParData(): DeficitApparentParItem[] {
        return this.deficitApparentParData;
    }

    // Column definitions for the CAR deficit apparent table
    deficitApparentCarColumns: string[] = ['metric', 'carIbt', 'carTbse', 'deltaCar'];

    // Data for the CAR deficit apparent table
    deficitApparentCarData: DeficitApparentCarItem[] = [
        {metric: 'Moyenne', carIbt: '9,51€', carTbse: '29,03€', deltaCar: '-19,52€'},
        {metric: 'Médiane', carIbt: '0,00€', carTbse: '0,00€', deltaCar: ''},
        {metric: 'Variance', carIbt: '389,6407', carTbse: '1718,7326', deltaCar: ''},
        {metric: 'Ecart-type', carIbt: '19,74€', carTbse: '41,46€', deltaCar: ''},
        {metric: 'cv', carIbt: '2,076', carTbse: '1,428', deltaCar: ''},
        {metric: 'MAPE', carIbt: '13,97€', carTbse: '34,32€', deltaCar: ''}
    ];

    // Method to get the data for the CAR deficit apparent table
    getDeficitApparentCarData(): DeficitApparentCarItem[] {
        return this.deficitApparentCarData;
    }

    // Column definitions for the PAR deficit effectif table
    deficitEffectifParColumns: string[] = ['metric', 'parIbt', 'parTbse', 'deltaPar'];

    // Data for the PAR deficit effectif table
    deficitEffectifParData: DeficitEffectifParItem[] = [
        {metric: 'Moyenne', parIbt: '17,69', parTbse: '53,33', deltaPar: '-35,64'},
        {metric: 'Médiane', parIbt: '16,15', parTbse: '43,78', deltaPar: ''},
        {metric: 'D1', parIbt: '2,08', parTbse: '11,03', deltaPar: ''},
        {metric: 'D9', parIbt: '37,01', parTbse: '102,79', deltaPar: ''},
        {metric: 'Variance', parIbt: '202,081', parTbse: '1181,3969', deltaPar: ''},
        {metric: 'Ecart-type', parIbt: '14,22', parTbse: '34,37', deltaPar: ''},
        {metric: 'cv', parIbt: '0,804', parTbse: '0,645', deltaPar: ''},
        {metric: 'MAPE', parIbt: '11,25', parTbse: '30,19', deltaPar: ''}
    ];

    // Method to get the data for the PAR deficit effectif table
    getDeficitEffectifParData(): DeficitEffectifParItem[] {
        return this.deficitEffectifParData;
    }

    // Column definitions for the CAR deficit effectif table
    deficitEffectifCarColumns: string[] = ['metric', 'carIbt', 'carTbse', 'deltaCar'];

    // Data for the CAR deficit effectif table
    deficitEffectifCarData: DeficitEffectifCarItem[] = [
        {metric: 'Moyenne', carIbt: '33', carTbse: '60,17', deltaCar: '-27,17'},
        {metric: 'Médiane', carIbt: '27,85', carTbse: '52,73', deltaCar: ''},
        {metric: 'D1', carIbt: '6,07', carTbse: '9,73', deltaCar: ''},
        {metric: 'D9', carIbt: '64,5', carTbse: '119,81', deltaCar: ''},
        {metric: 'Variance', carIbt: '576,8663', carTbse: '1688,4959', deltaCar: ''},
        {metric: 'Ecart-type', carIbt: '24,02', carTbse: '41,09', deltaCar: ''},
        {metric: 'cv', carIbt: '0,728', carTbse: '0,683', deltaCar: ''},
        {metric: 'MAPE', carIbt: '19,26', carTbse: '35,64', deltaCar: ''}
    ];

    // Method to get the data for the CAR deficit effectif table
    getDeficitEffectifCarData(): DeficitEffectifCarItem[] {
        return this.deficitEffectifCarData;
    }

    // Column definitions for the PAR inegalite table
    inegaliteParColumns: string[] = ['ensemble', 'ibt', 'tbse'];

    // Data for the PAR inegalite table
    inegaliteParData: InegaliteParItem[] = [
        {ensemble: 'Gini', ibt: 95.6, tbse: 79.3},
        {ensemble: 'Schutz', ibt: 92.3, tbse: 70.1}
    ];

    // Method to get the data for the PAR inegalite table
    getInegaliteParData(): InegaliteParItem[] {
        return this.inegaliteParData;
    }

    // Column definitions for the CAR inegalite table
    inegaliteCarColumns: string[] = ['ibt', 'tbse'];

    // Data for the CAR inegalite table
    inegaliteCarData: InegaliteCarItem[] = [
        {ibt: 82.7, tbse: 70.6},
        {ibt: 73.5, tbse: 59.1}
    ];

    // Method to get the data for the CAR inegalite table
    getInegaliteCarData(): InegaliteCarItem[] {
        return this.inegaliteCarData;
    }

    // Column definitions for the PAR abordability problem table
    abordabiliteProblemParColumns: string[] = ['metric', 'ibt', 'tbse'];

    // Data for the PAR abordability problem table
    abordabiliteProblemParData: AbordabiliteProblemParItem[] = [
        {metric: 'Gini', ibt: 44.1, tbse: 36.8},
        {metric: 'Schutz', ibt: 31.8, tbse: 28.3},
        {metric: 'Ratio interdéciles', ibt: 17.8, tbse: 9.3},
        {metric: 'Ratio interdécimes', ibt: 38.8, tbse: 23.1},
        {metric: 'Ratio S80 / S20', ibt: 19.1, tbse: 10.1}
    ];

    // Method to get the data for the PAR abordability problem table
    getAbordabiliteProblemParData(): AbordabiliteProblemParItem[] {
        return this.abordabiliteProblemParData;
    }

    // Column definitions for the CAR abordability problem table
    abordabiliteProblemCarColumns: string[] = ['ibt', 'tbse'];

    // Data for the CAR abordability problem table
    abordabiliteProblemCarData: AbordabiliteProblemCarItem[] = [
        {ibt: 39.8, tbse: 39.0},
        {ibt: 29.2, tbse: 29.6},
        {ibt: 10.6, tbse: 12.3},
        {ibt: 27.9, tbse: 25.7},
        {ibt: 12.0, tbse: 13.1}
    ];

    // Method to get the data for the CAR abordability problem table
    getAbordabiliteProblemCarData(): AbordabiliteProblemCarItem[] {
        return this.abordabiliteProblemCarData;
    }

    /**
     * Converts the general median statistics data to the TableData format
     */
    convertGeneralMedianStatisticsToTableData(): TableData {
        return {
            tableName: 'General Median Statistics (PAR)',
            columnNames: ['Row', 'PAR IBT', 'PAR TBSE', 'Delta PAR'],
            values: this.generalMedianStatistics.map(item => [
                item.rowLabel,
                item.parIbt,
                item.parTbse,
                item.deltaPar
            ])
        };
    }

    /**
     * Converts the general median statistics CAR data to the TableData format
     */
    convertGeneralMedianStatisticsCarToTableData(): TableData {
        return {
            tableName: 'General Median Statistics (CAR)',
            columnNames: ['Row', 'CAR IBT', 'CAR TBSE', 'Delta CAR'],
            values: this.generalMedianStatisticsCar.map(item => [
                item.rowLabel,
                item.carIbt,
                item.carTbse,
                item.deltaCar
            ])
        };
    }

    /**
     * Converts the other general statistics data to the TableData format
     */
    convertOtherGeneralStatisticsToTableData(): TableData {
        return {
            tableName: 'Other General Statistics (PAR)',
            columnNames: ['Metric', 'PAR IBT', 'PAR TBSE'],
            values: this.otherGeneralStatistics.map(item => [
                item.metric,
                item.parIbt,
                item.parTbse
            ])
        };
    }

    /**
     * Converts the other general statistics CAR data to the TableData format
     */
    convertOtherGeneralStatisticsCarToTableData(): TableData {
        return {
            tableName: 'Other General Statistics (CAR)',
            columnNames: ['Metric', 'CAR IBT', 'CAR TBSE'],
            values: this.otherGeneralStatisticsCar.map(item => [
                item.metric,
                item.carIbt,
                item.carTbse
            ])
        };
    }

    /**
     * Converts the PAR incidence data to the TableData format
     */
    convertParIncidenceToTableData(): TableData {
        return {
            tableName: 'PAR Incidence (Headcount ratio)',
            columnNames: ['Category', 'PAR IBT', 'PAR TBSE', 'Delta PAR'],
            values: this.parIncidenceData.map(item => [
                item.category,
                item.parIbt,
                item.parTbse,
                item.deltaPar
            ])
        };
    }

    /**
     * Converts the CAR incidence data to the TableData format
     */
    convertCarIncidenceToTableData(): TableData {
        return {
            tableName: 'CAR Incidence',
            columnNames: ['Category', 'CAR IBT', 'CAR TBSE', 'Delta CAR'],
            values: this.carIncidenceData.map(item => [
                item.category,
                item.carIbt,
                item.carTbse,
                item.deltaCar
            ])
        };
    }

    /**
     * Converts the PAR deficit apparent data to the TableData format
     */
    convertDeficitApparentParToTableData(): TableData {
        return {
            tableName: 'Déficit Apparent PAR',
            columnNames: ['Metric', 'PAR IBT', 'PAR TBSE', 'Delta PAR'],
            values: this.deficitApparentParData.map(item => [
                item.metric,
                item.parIbt,
                item.parTbse,
                item.deltaPar
            ])
        };
    }

    /**
     * Converts the CAR deficit apparent data to the TableData format
     */
    convertDeficitApparentCarToTableData(): TableData {
        return {
            tableName: 'Déficit Apparent CAR',
            columnNames: ['Metric', 'CAR IBT', 'CAR TBSE', 'Delta CAR'],
            values: this.deficitApparentCarData.map(item => [
                item.metric,
                item.carIbt,
                item.carTbse,
                item.deltaCar
            ])
        };
    }

    /**
     * Converts the PAR deficit effectif data to the TableData format
     */
    convertDeficitEffectifParToTableData(): TableData {
        return {
            tableName: 'Déficit Effectif PAR',
            columnNames: ['Metric', 'PAR IBT', 'PAR TBSE', 'Delta PAR'],
            values: this.deficitEffectifParData.map(item => [
                item.metric,
                item.parIbt,
                item.parTbse,
                item.deltaPar
            ])
        };
    }

    /**
     * Converts the CAR deficit effectif data to the TableData format
     */
    convertDeficitEffectifCarToTableData(): TableData {
        return {
            tableName: 'Déficit Effectif CAR',
            columnNames: ['Metric', 'CAR IBT', 'CAR TBSE', 'Delta CAR'],
            values: this.deficitEffectifCarData.map(item => [
                item.metric,
                item.carIbt,
                item.carTbse,
                item.deltaCar
            ])
        };
    }

    /**
     * Converts the PAR inegalite data to the TableData format
     */
    convertInegaliteParToTableData(): TableData {
        return {
            tableName: 'Inegalité PAR',
            columnNames: ['Ensemble', 'IBT', 'TBSE'],
            values: this.inegaliteParData.map(item => [
                item.ensemble,
                item.ibt,
                item.tbse
            ])
        };
    }

    /**
     * Converts the CAR inegalite data to the TableData format
     */
    convertInegaliteCarToTableData(): TableData {
        return {
            tableName: 'Inegalité CAR',
            columnNames: ['IBT', 'TBSE'],
            values: this.inegaliteCarData.map(item => [
                item.ibt,
                item.tbse
            ])
        };
    }

    /**
     * Converts the PAR abordability problem data to the TableData format
     */
    convertAbordabiliteProblemParToTableData(): TableData {
        return {
            tableName: 'Abordabilité Problème PAR',
            columnNames: ['Metric', 'IBT', 'TBSE'],
            values: this.abordabiliteProblemParData.map(item => [
                item.metric,
                item.ibt,
                item.tbse
            ])
        };
    }

    /**
     * Converts the CAR abordability problem data to the TableData format
     */
    convertAbordabiliteProblemCarToTableData(): TableData {
        return {
            tableName: 'Abordabilité Problème CAR',
            columnNames: ['IBT', 'TBSE'],
            values: this.abordabiliteProblemCarData.map(item => [
                item.ibt,
                item.tbse
            ])
        };
    }

    /**
     * Implements the ChatDataProvider interface.
     * Returns the component's data for use in chat messages.
     */
    getChatData(): { componentName: string; pageName: string; data: TableData[] } {
        return {
            componentName: 'AbordabiliteGeneralComponent',
            pageName: 'abordabilite-general',
            data: [
                this.convertGeneralMedianStatisticsToTableData(),
                this.convertGeneralMedianStatisticsCarToTableData(),
                this.convertOtherGeneralStatisticsToTableData(),
                this.convertOtherGeneralStatisticsCarToTableData(),
                this.convertParIncidenceToTableData(),
                this.convertCarIncidenceToTableData(),
                this.convertDeficitApparentParToTableData(),
                this.convertDeficitApparentCarToTableData(),
                this.convertDeficitEffectifParToTableData(),
                this.convertDeficitEffectifCarToTableData(),
                this.convertInegaliteParToTableData(),
                this.convertInegaliteCarToTableData(),
                this.convertAbordabiliteProblemParToTableData(),
                this.convertAbordabiliteProblemCarToTableData()
            ]
        };
    }
}
