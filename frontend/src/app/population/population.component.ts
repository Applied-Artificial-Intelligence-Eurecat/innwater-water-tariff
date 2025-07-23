import {Component, OnDestroy, OnInit} from '@angular/core';
import {ChatDataProvider} from "../interfaces/chat-data-provider.interface";
import {TableData} from "../interfaces/table-data.interface";
import {ChatService} from "../services/chat.service";

@Component({
  selector: 'app-population',
  templateUrl: './population.component.html',
  styleUrls: ['./population.component.css']
})
export class PopulationComponent implements OnInit, OnDestroy, ChatDataProvider {
  // Expected Population Size (EPS) - default 1,000, min 1,000, max 10,000, increments of 1,000
  expectedPopulationSize: number = 1000;
  populationSizeOptions: number[] = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000];

  // Standard deviation for normal distribution - default 0.05, min 0.01, max 0.20, increments of 0.02
  standardDeviation: number = 0.05;
  standardDeviationOptions: number[] = [0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.20];

  // Flag to control the visibility of the scatter plot
  showScatterPlot: boolean = false;

  constructor(private chatService: ChatService) {
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

  ngOnInit(): void {
      // Register this component with the chat service
      this.chatService.registerComponent('population', this);
  }

  ngOnDestroy(): void {
      // Unregister this component when it's destroyed
      this.chatService.unregisterComponent('population');
  }

  /**
   * Converts the population data to the TableData format
   */
  convertPopulationDataToTableData(): TableData {
      return {
          tableName: 'Population Generation Parameters',
          columnNames: ['Choix BDD', 'Expected Population Size (EPS)'],
          values: [
              ['Reunion 2010', this.expectedPopulationSize.toString()]
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

  // Method to toggle the visibility of the scatter plot
  toggleScatterPlot(): void {
    this.showScatterPlot = true;
  }
}
