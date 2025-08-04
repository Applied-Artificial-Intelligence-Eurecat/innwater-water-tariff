import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {InitialAPIService} from "../initial-api.service";
import {environment} from "../../environments/environment";
import {DomSanitizer, SafeResourceUrl} from "@angular/platform-browser";

@Component({
    selector: 'app-simulation-details',
    templateUrl: './simulation-details.component.html',
    styleUrls: ['./simulation-details.component.css']
})
export class SimulationDetailsComponent implements OnInit {
    simulationId: number | null = null;
    simulationData: any = null;
    loading: boolean = true;
    error: string | null = null;
    panelInitializationOpenState: boolean = false;
    panelPopulationOpenState: boolean = false;

    private apiUrl = environment.apiUrl;
    tbseParPlotUrl: SafeResourceUrl | null = null;
    tbseConsumptionPlotUrl: SafeResourceUrl | null = null;
    pensParadePlotUrl: SafeResourceUrl | null = null;
    consumptionDeviationLosesCostRecoveryPlot: SafeResourceUrl | null = null;
    populationPlotUrl: SafeResourceUrl | null = null;

    constructor(
        private route: ActivatedRoute,
        private router: Router,
        private initialApiService: InitialAPIService,
        private sanitizer: DomSanitizer
    ) {
    }

    ngOnInit(): void {
        // Get the simulation ID from the route parameter
        this.route.paramMap.subscribe(params => {
            let idParam = params.get('id');
            this.simulationId = idParam !== null ? Number(idParam) : null;
            if (this.simulationId) {
                this.initialApiService.getSimulationById(this.simulationId).subscribe({
                        next: (response) => {
                            this.simulationData = response.data;
                            this.loading = false;
                            console.log(this.simulationData);
                        },
                        error: (err) => {
                            console.error('Error loading simulation:', err);
                            this.loading = false;
                            this.error = 'Failed to load simulation data. Please try again.';

                        }
                    }
                );
            } else {
                this.error = 'No simulation ID provided';
                this.loading = false;
            }
        });
        this.initialApiService.getPlot(`${this.apiUrl}/api/v1/initial/simulation/${this.simulationId}/tbse_par_plot`).subscribe(blob => {
            const objectURL = URL.createObjectURL(blob);
            this.tbseParPlotUrl = this.sanitizer.bypassSecurityTrustResourceUrl(objectURL);
        });
        this.initialApiService.getPlot(`${this.apiUrl}/api/v1/initial/simulation/${this.simulationId}/tbse_consumption_plot`).subscribe(blob => {
            const objectUrl = URL.createObjectURL(blob);
            this.tbseConsumptionPlotUrl = this.sanitizer.bypassSecurityTrustResourceUrl(objectUrl);
        })
        this.initialApiService.getPlot(`${this.apiUrl}/api/v1/initial/simulation/${this.simulationId}/pens_parade_consumption_plot`).subscribe(blob => {
            const objectUrl = URL.createObjectURL(blob);
            this.pensParadePlotUrl = this.sanitizer.bypassSecurityTrustResourceUrl(objectUrl);
        });
        this.initialApiService.getPlot(`${this.apiUrl}/api/v1/initial/simulation/${this.simulationId}/consumption_deviation_loses_cost_recovery_plot`).subscribe(blob => {
            const objectUrl = URL.createObjectURL(blob);
            this.consumptionDeviationLosesCostRecoveryPlot = this.sanitizer.bypassSecurityTrustResourceUrl(objectUrl);
        });
        this.initialApiService.getPlot(`${this.apiUrl}/api/v1/initial/simulation/${this.simulationId}/population_plot`).subscribe(blob => {
            const objectUrl = URL.createObjectURL(blob);
            this.populationPlotUrl = this.sanitizer.bypassSecurityTrustResourceUrl(objectUrl);
        })
    }

}