import {Component, OnInit} from '@angular/core';
import {InitialAPIService, Simulation} from '../initial-api.service';
import {Router} from "@angular/router";
import {MatDialog} from '@angular/material/dialog';
import {ConfirmDialogComponent} from '../components/confirm-dialog/confirm-dialog.component';

@Component({
    selector: 'app-list-simulation',
    templateUrl: './list-simulation.component.html',
    styleUrls: ['./list-simulation.component.css']
})
export class ListSimulationComponent implements OnInit {
    simulations: Simulation[] = [];
    loading = false;
    error = '';

    constructor(
        private initialApiService: InitialAPIService,
        private router: Router,
        private dialog: MatDialog
    ) {
    }

    ngOnInit(): void {
        this.loading = true;
        this.refreshData();
    }

    private refreshData() {
        this.initialApiService.getSimulations().subscribe({
            next: (response) => {
                this.simulations = response.data;
                this.loading = false;
            },
            error: (err) => {
                if (err.status === 401) {
                    this.initialApiService.logout();
                    this.router.navigateByUrl('/');
                    return;
                }
                this.error = 'Failed to load simulations. Please try again later.';
                this.loading = false;
                console.error('Error loading simulations:', err);
            }
        });
    }

    deleteSimulation(id: number) {
        const dialogRef = this.dialog.open(ConfirmDialogComponent, {
            width: '400px',
            data: {
                title: 'Delete Simulation',
                message: 'Are you sure you want to delete the simulation?',
                confirmText: 'Yes, delete it',
                cancelText: 'Cancel'
            }
        });

        dialogRef.afterClosed().subscribe(result => {
            if (result) {
                this.initialApiService.deleteSimulation(id).subscribe({
                    next: (response) => {
                        this.refreshData();
                    },
                    error: (err) => {
                        if (err.status === 401) {
                            this.initialApiService.logout();
                            this.router.navigateByUrl('/');
                        }
                    }
                });
            }
        });
    }

    editSimulation(simulation: Simulation) {
        if (simulation.status === '1st Round Evaluation') {
            this.dialog.open(ConfirmDialogComponent, {
                width: '400px',
                data: {
                    title: 'Cannot Edit Simulation',
                    message: 'Simulations in evaluation cannot be edited.',
                    confirmText: 'OK',
                    cancelText: ''
                }
            });
        } else {
            this.router.navigate(['/edit-simulation', simulation.id]);
        }
    }

    copySimulation(id: number) {
        const dialogRef = this.dialog.open(ConfirmDialogComponent, {
            width: '400px',
            data: {
                title: 'Duplicate Simulation',
                message: 'You can duplicate a simulation. The first status will be Initialized so that you can change the values of the simulation.',
                confirmText: 'Duplicate',
                cancelText: 'Cancel',
                showInput: true,
                inputLabel: 'New Simulation Name'
            }
        });

        dialogRef.afterClosed().subscribe(result => {
            if (result) {
                this.initialApiService.duplicateSimulation(id, result).subscribe({
                    next: (response) => {
                        this.refreshData();
                    },
                    error: (err) => {
                        if (err.status === 401) {
                            this.initialApiService.logout();
                            this.router.navigateByUrl('/');
                        } else {
                            this.error = 'Failed to duplicate simulation. Please try again later.';
                            console.error('Error duplicating simulation:', err);
                        }
                    }
                });
            }
        });
    }
}
