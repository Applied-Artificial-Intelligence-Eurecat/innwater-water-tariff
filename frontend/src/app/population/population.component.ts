import { Component, Input, OnChanges, OnDestroy, OnInit } from '@angular/core';
import { ChatDataProvider } from "../interfaces/chat-data-provider.interface";
import { TableData } from "../interfaces/table-data.interface";
import { ChatService } from "../services/chat.service";
import { DomSanitizer } from "@angular/platform-browser";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { environment } from "../../environments/environment";
import { HintService } from "../services/hint.service";

@Component({
    selector: 'app-population',
    templateUrl: './population.component.html',
    styleUrls: ['./population.component.css']
})
export class PopulationComponent implements OnInit, OnDestroy, OnChanges, ChatDataProvider {
    // Expected Population Size (EPS) - default 1,000, min 1,000, max 10,000, increments of 1,000
    @Input() totalSubscribers: number | null | undefined = null;
    @Input() sanitationSubscribers: number | null | undefined = null;

    private apiUrl: string = environment.apiUrl;

    // Flag to control whether to use original datasource
    useOriginalDatasource: boolean = false;

    expectedPopulationSize: number = 1000;
    populationSizeOptions: number[] = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000];

    // Standard deviation for normal distribution - default 0.05, min 0.01, max 0.20, increments of 0.02
    standardDeviation: number = 0.05;
    standardDeviationOptions: number[] = [0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.20];

    // Flag to control the visibility of the scatter plot
    showScatterPlot: boolean = false;
    imageSrc: any;

    constructor(
        private chatService: ChatService, 
        private sanitizer: DomSanitizer, 
        private http: HttpClient,
        private hintService: HintService
    ) {
    }

    /**
     * Shows a hint about the population module
     */
    showPopulationHint() {
        this.hintService.showHint(
            'Population Module',
            '<p>Population module describes the population of households with regard to some relevant variables for calculation and decomposition of (i) water consumptions, (ii) water bills and (iii) indicators making up the dashboard.</p>',
            true
        );
    }

    ngOnChanges(changes: any): void {
        console.log(this.totalSubscribers)
    }

    getComponentDescription(): string {
        return "The Population component allows users to generate a household population sample based on the Data_La_Reunion_2 data file. Users can specify the Expected Population Size (EPS) and the Standard Deviation for the normal distribution that will be used to modify the income of randomly selected households." +
            "This component is essential for creating a representative sample of households for water tariff analysis." +
            "The user specifies how many households he wants in the Household\n" +
            "population sample. By default, the value is 1,000 (which is also the minimum\n" +
            "value; the user can go up to 10,000 in increments of 1,000; provide a drop-down\n" +
            "list: 1,000, 2,000, ..., 10,000).\n\n" +
            "Also, the user must declare the value of the standard deviation of the\n" +
            "normal distribution from which a value will be drawn to modify the income." +
            "The default value is 0.05 (the minimum\n" +
            "value is 0.01, the maximum value is 0.20; a drop-down list with possible values\n" +
            "in increments of 0.02 (0.01, 0.03, 0.05, ..., 0.19, 0.20) seems to us to be the most\n" +
            "appropriate)." +
            "The standard deviation is a value that will be drawn to modify the **income** of the randomly selected household.";
    }


    getPopulationPlot() {
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Accept': 'image/png'
        });
        const randomNumber = Math.ceil(Math.random() * 100000);
        const body = {
            bd: 'Reunion 2010',
            original_datasource: this.useOriginalDatasource,
            eps: this.expectedPopulationSize,
            std: this.standardDeviation,
            total_subscribers: this.totalSubscribers,
            sanitation_subscribers: this.sanitationSubscribers,
            random_seed: randomNumber,
        };
        this.http.post(`${this.apiUrl}/api/v1/initial/population/plot`, body, {
            headers: headers,
            responseType: 'blob'
        }).subscribe(blob => {
            const objectURL = URL.createObjectURL(blob);
            this.imageSrc = this.sanitizer.bypassSecurityTrustResourceUrl(objectURL);
        });
    }

    ngOnInit(): void {
        this.chatService.registerComponent('population', this);
        console.log(this.totalSubscribers)
    }

    ngOnDestroy(): void {
        this.chatService.unregisterComponent('population');
    }

    /**
     * Converts the population data to the TableData format
     */
    convertPopulationDataToTableData(): TableData {
        return {
            tableName: 'Population Generation Parameters',
            columnNames: ['Choice Source Database', 'Use Original Datasource', 'Expected Population Size (EPS)'],
            values: [
                ['Reunion 2010', this.useOriginalDatasource ? 'Yes' : 'No', this.expectedPopulationSize.toString()]
            ]
        };
    }

    /**
     * Implements the ChatDataProvider interface.
     * Returns the component's data for use in chat messages.
     */
    getChatData(): { componentName: string; pageName: string; data: TableData[]; } {
        return {
            componentName: 'PopulationComponent',
            pageName: 'population',
            data: [
                this.convertPopulationDataToTableData(),
                {
                    tableName: "Population Income Parameters",
                    columnNames: ['Standard Deviation for Normal distribution'],
                    values: [
                        [this.standardDeviation.toString()]
                    ]
                }
            ]
        };
    }

    // Method to handle changes to the Expected Population Size
    onPopulationSizeChange(event: any): void {
        this.expectedPopulationSize = Number(event.target.value);
    }

    // Method to handle changes to the Standard Deviation
    onStandardDeviationChange(event: any): void {
        this.standardDeviation = Number(event.target.value);
    }

    // Method to handle changes to the Use Original Datasource checkbox
    onUseOriginalDatasourceChange(event: any): void {
        this.useOriginalDatasource = event.target.checked;
    }

    // Method to toggle the visibility of the scatter plot
    toggleScatterPlot(): void {
        this.showScatterPlot = true;
        this.getPopulationPlot()
    }
}
