import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {InitialAPIService} from "../initial-api.service";
import {environment} from "../../environments/environment";
import {DomSanitizer, SafeResourceUrl} from "@angular/platform-browser";
import {GameRound, GameRoundParams, GameService} from "../game.service";
import {MatDialog} from '@angular/material/dialog';
import {LinkGameDialogComponent} from './link-game-dialog/link-game-dialog.component';
import {CreateGameDialogComponent} from './create-game-dialog/create-game-dialog.component';
import {ImagePopupDialogComponent} from './image-popup-dialog/image-popup-dialog.component';
import {ResultsService} from "../results.service";

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
    panelGameParticipationsOpenState: boolean = false;

    // Game participations
    gameParticipations: { id?: number; alpha: number; ratio_tbse: number; threshold_res: number; score: number }[] = [];
    loadingParticipations: boolean = false;
    displayedColumns: string[] = ['alpha', 'ratio_tbse', 'threshold_res', 'score', 'actions'];

    // Available game rounds for linking
    availableGameRounds: GameRound[] = [];
    loadingGameRounds: boolean = false;

    // New game round form
    newGameRound: GameRoundParams = {
        alpha: 0,
        ratio_tbse: 0,
        threshold_res: 0
    };

    private apiUrl = environment.apiUrl;
    tbseParPlotUrl: SafeResourceUrl | null = null;
    tbseConsumptionPlotUrl: SafeResourceUrl | null = null;
    tbsePensParadePlotUrl: SafeResourceUrl | null = null;
    tbseConsumptionDeviationLosesCostRecoveryPlot: SafeResourceUrl | null = null;
    populationPlotUrl: SafeResourceUrl | null = null;
    ibtParPlotUrl: SafeResourceUrl | null = null;
    ibtConsumptionPlotUrl: SafeResourceUrl | null = null;
    ibtPensParadePlotUrl: SafeResourceUrl | null = null;
    ibtConsumptionDeviationLosesCostRecoveryPlot: SafeResourceUrl | null = null;

    constructor(
        public route: ActivatedRoute,
        public router: Router,
        private initialApiService: InitialAPIService,
        private resultsService: ResultsService,
        private gameService: GameService,
        private dialog: MatDialog,
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

                            // Load game participations for this simulation
                            this.loadGameParticipations();
                        },
                        error: (err) => {
                            console.error('Error loading simulation:', err);
                            this.loading = false;
                            this.initialApiService.logout();
                            this.router.navigateByUrl('/')
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
        this.initialApiService.getPlot(`${this.apiUrl}/api/v1/initial/simulation/${this.simulationId}/ibt_par_plot`).subscribe(blob => {
            const objectURL = URL.createObjectURL(blob);
            this.ibtParPlotUrl = this.sanitizer.bypassSecurityTrustResourceUrl(objectURL);
        })
        this.initialApiService.getPlot(`${this.apiUrl}/api/v1/initial/simulation/${this.simulationId}/tbse_consumption_plot`).subscribe(blob => {
            const objectUrl = URL.createObjectURL(blob);
            this.tbseConsumptionPlotUrl = this.sanitizer.bypassSecurityTrustResourceUrl(objectUrl);
        })
        this.initialApiService.getPlot(`${this.apiUrl}/api/v1/initial/simulation/${this.simulationId}/ibt_consumption_plot`).subscribe(blob => {
            const objectUrl = URL.createObjectURL(blob);
            this.ibtConsumptionPlotUrl = this.sanitizer.bypassSecurityTrustResourceUrl(objectUrl);
        })
        this.initialApiService.getPlot(`${this.apiUrl}/api/v1/initial/simulation/${this.simulationId}/tbse_pens_parade_consumption_plot`).subscribe(blob => {
            const objectUrl = URL.createObjectURL(blob);
            this.tbsePensParadePlotUrl = this.sanitizer.bypassSecurityTrustResourceUrl(objectUrl);
        });
        this.initialApiService.getPlot(`${this.apiUrl}/api/v1/initial/simulation/${this.simulationId}/ibt_pens_parade_consumption_plot`).subscribe(blob => {
            const objectUrl = URL.createObjectURL(blob);
            this.ibtPensParadePlotUrl = this.sanitizer.bypassSecurityTrustResourceUrl(objectUrl);
        })
        this.initialApiService.getPlot(`${this.apiUrl}/api/v1/initial/simulation/${this.simulationId}/tbse_consumption_deviation_loses_cost_recovery_plot`).subscribe(blob => {
            const objectUrl = URL.createObjectURL(blob);
            this.tbseConsumptionDeviationLosesCostRecoveryPlot = this.sanitizer.bypassSecurityTrustResourceUrl(objectUrl);
        });
        this.initialApiService.getPlot(`${this.apiUrl}/api/v1/initial/simulation/${this.simulationId}/ibt_consumption_deviation_loses_cost_recovery_plot`).subscribe(blob => {
            const objectUrl = URL.createObjectURL(blob)
            this.ibtConsumptionDeviationLosesCostRecoveryPlot = this.sanitizer.bypassSecurityTrustResourceUrl(objectUrl);
        })
        this.initialApiService.getPlot(`${this.apiUrl}/api/v1/initial/simulation/${this.simulationId}/population_plot`).subscribe(blob => {
            const objectUrl = URL.createObjectURL(blob);
            this.populationPlotUrl = this.sanitizer.bypassSecurityTrustResourceUrl(objectUrl);
        })
    }

    /**
     * Loads game participations for the current simulation
     */
    loadGameParticipations(): void {
        if (!this.simulationId) return;

        this.loadingParticipations = true;
        this.gameService.getGameParticipations(this.simulationId).subscribe({
            next: (participations) => {
                this.gameParticipations = participations;
                this.loadingParticipations = false;
            },
            error: (err) => {
                console.error('Error loading game participations:', err);
                this.loadingParticipations = false;
            }
        });
    }

    /**
     * Opens the modal for linking to an existing game round
     */
    openLinkGameModal(): void {
        // Load available game rounds
        this.loadingGameRounds = true;
        this.gameService.getAllRounds().subscribe({
            next: (rounds) => {
                this.availableGameRounds = rounds;
                console.log(this.availableGameRounds);
                this.loadingGameRounds = false;

                // Open the modal dialog
                const dialogRef = this.dialog.open(LinkGameDialogComponent, {
                    width: '500px',
                    data: {
                        gameRounds: this.availableGameRounds,
                        simulationId: this.simulationId
                    }
                });

                dialogRef.afterClosed().subscribe(result => {
                    if (result) {
                        // Reload participations if a game was linked
                        this.loadGameParticipations();
                    }
                });
            },
            error: (err) => {
                console.error('Error loading game rounds:', err);
                this.loadingGameRounds = false;
            }
        });
    }

    /**
     * Opens the modal for creating a new game round
     */
    openCreateGameModal(): void {
        const dialogRef = this.dialog.open(CreateGameDialogComponent, {
            width: '500px',
            data: {
                newGameRound: this.newGameRound,
                simulationId: this.simulationId
            }
        });

        dialogRef.afterClosed().subscribe(result => {
            if (result) {
                // Reload participations if a game was created and linked
                this.loadGameParticipations();
            }
        });
    }

    /**
     * Opens an image in a popup dialog with zoom functionality
     * @param imageUrl The URL of the image to display
     * @param title Optional title for the dialog
     */
    openImagePopup(imageUrl: SafeResourceUrl | null, title?: string): void {
        this.dialog.open(ImagePopupDialogComponent, {
            width: '90vw',
            maxWidth: '1200px',
            data: {
                imageUrl: imageUrl,
                title: title
            }
        });
    }

downloadCSV() {
    if (this.simulationId !== null) {
        console.log("Downloading...", this.simulationId);
        this.resultsService.downloadCSV(this.simulationId).subscribe({
            next: (blob: Blob) => {
                // Create a URL for the blob
                const url = window.URL.createObjectURL(blob);

                // Create a temporary anchor element and trigger download
                const link = document.createElement('a');
                link.href = url;
                link.download = `simulation_${this.simulationId}_results.csv`;
                link.style.display = 'none';

                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);

                // Clean up the URL
                window.URL.revokeObjectURL(url);
            },
            error: (error) => {
                console.error('Error downloading CSV:', error);
                // You might want to show a user-friendly error message here
            }
        });
    }
}
}
