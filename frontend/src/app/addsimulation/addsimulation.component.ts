import {AfterViewInit, Component, OnInit, ViewChild} from '@angular/core';
import {FormArray, FormBuilder, FormControl, Validators} from '@angular/forms';
import {HttpClient} from '@angular/common/http';
import {ActivatedRoute, Router} from '@angular/router';
import {InitialAPIService, SimulationPayload} from '../initial-api.service';
import {DomSanitizer} from "@angular/platform-browser";
import {PopulationComponent} from '../population/population.component';
import {MatSnackBar} from '@angular/material/snack-bar';
import {MatDialog} from '@angular/material/dialog';
import {ConfirmDialogComponent} from '../components/confirm-dialog/confirm-dialog.component';
import {HintService} from '../services/hint.service';

@Component({
    selector: 'app-addsimulation',
    templateUrl: './addsimulation.component.html',
    styleUrls: ['./addsimulation.component.css']
})
export class AddsimulationComponent implements OnInit, AfterViewInit {

    @ViewChild(PopulationComponent) populationComponent!: PopulationComponent;

    seuil_ep!: { [key: string]: number };
    prix_ep!: { [key: string]: number };
    seuil_r_ep!: { [key: string]: number };
    prix_r_ep!: { [key: string]: number };

    seuil_a!: { [key: string]: number };
    prix_a!: { [key: string]: number };
    seuil_r_a!: { [key: string]: number };
    disabled: boolean = false;
    loading: boolean = false;
    error: string = '';

    tab_pep: number[] = [];
    tab_sep: number[] = [];
    tab_pa: number[] = [];
    tab_sa: number[] = [];

    isEditMode = false;
    simulationId: number | null = null;

    constructor(
        private http: HttpClient,
        private fb: FormBuilder,
        private router: Router,
        private route: ActivatedRoute,
        private initialApiService: InitialAPIService,
        private sanitizer: DomSanitizer,
        private snackBar: MatSnackBar,
        private dialog: MatDialog,
        private hintService: HintService,
    ) {
    }

    /**
     * Shows a hint dialog with the specified title and message
     * @param title The title of the hint dialog
     * @param message The message to display in the hint dialog
     * @param isHtml Whether the message contains HTML content
     */
    showHint(title: string, message: string, isHtml: boolean = false) {
        this.hintService.showHint(title, message, isHtml);
    }


    demandeForm = this.fb.group({
        a0: new FormControl({value: -2.56, disabled: this.disabled}, {validators: [Validators.required]}),
        a1: new FormControl({value: 0.48, disabled: this.disabled}, {validators: [Validators.required]}),
        a2: new FormControl({value: 0.44, disabled: this.disabled}, {validators: [Validators.required]}),
        a3: new FormControl({value: 0.12, disabled: this.disabled}, {validators: [Validators.required]}),
        a4: new FormControl({value: 0.37, disabled: this.disabled}, {validators: [Validators.required]}),
        a5: new FormControl({value: -0.31, disabled: this.disabled}, {validators: [Validators.required]}),
        a6: new FormControl({value: 0.25, disabled: this.disabled}, {validators: [Validators.required]}),
        has_pool: new FormControl({value: false, disabled: this.disabled}, {validators: [Validators.required]}),
        has_garden: new FormControl({value: false, disabled: this.disabled}, {validators: [Validators.required]}),
        car: new FormControl({value: 3, disabled: this.disabled}, {validators: [Validators.required]}),
        par: new FormControl({value: 3, disabled: this.disabled}, {validators: [Validators.required]}),
        k: new FormControl({value: 0.99, disabled: this.disabled}, {validators: [Validators.required]}),
        periodes: new FormControl({value: 4, disabled: this.disabled}, {validators: [Validators.required]}),
        nom: new FormControl('', {validators: [Validators.required]}),
        pauvret: new FormControl({value: 800, disabled: this.disabled}, {validators: [Validators.required]}),
    });
    tarificationForm = this.fb.group({

        coutsFixe_ep: new FormControl({value: 9000000, disabled: this.disabled}, {validators: [Validators.required]}),
        coutsVariable_ep: new FormControl(0.9, {validators: [Validators.required]}),
        montantAbo_ep: new FormControl(18.69, {validators: [Validators.required]}),
        nombreAbonnes_ep: new FormControl(45800, {validators: [Validators.required]}),
        redevances_ep: new FormControl(0.12, {validators: [Validators.required]}),
        tva_ep: new FormControl(2.1, {validators: [Validators.required]}),
        seuils_ep: this.fb.array([]),
        seuils_r_ep: this.fb.array([]),

        coutsFixe_a: new FormControl(6000000, {validators: [Validators.required]}),
        coutsVariable_a: new FormControl(0.40, {validators: [Validators.required]}),
        nombreAbonnes_a: new FormControl(21000, {validators: [Validators.required]}),
        montantAbo_a: new FormControl(15.545, {validators: [Validators.required]}),
        redevances_a: new FormControl(0.04, {validators: [Validators.required]}),

        tva_a: new FormControl(10, {validators: [Validators.required]}),
        seuils_a: this.fb.array([]),
        seuils_r_a: this.fb.array([]),

        cenvU: new FormControl(1.3, {validators: [Validators.required]}),
        env_fixed_costs: new FormControl(0, {validators: [Validators.required]}),

    });
    isLinear = true;

    addSimulation() {
        console.log(this.demandeForm.value);
        const s_ep = this.tarificationForm.controls['seuils_ep'] as FormArray;
        const s_a = this.tarificationForm.controls['seuils_a'] as FormArray;
        const s_r_ep = this.tarificationForm.controls['seuils_r_ep'] as FormArray;
        const s_r_a = this.tarificationForm.controls['seuils_r_a'] as FormArray;
        let i: number = 0;
        let j: number = 0;
        let k: number = 0;
        let l: number = 0;
        for (let c of s_ep.value) {
            this.seuil_ep['K' + i] = c.seuil
            this.prix_ep['K' + i] = c.prix
            this.tab_pep.push(c.prix)
            this.tab_sep.push(c.seuil)
            i += 1;
        }
        for (let c of s_a.value) {
            this.seuil_a['aK' + j] = c.seuil
            this.prix_a['aK' + j] = c.prix
            this.tab_pa.push(c.prix)
            this.tab_sa.push(c.seuil)
            j += 1;
        }
        for (let c of s_r_ep.value) {
            this.seuil_r_ep['rK' + k] = c.seuil
            this.prix_r_ep['rK' + k] = c.prix
            k += 1;
        }
        for (let c of s_r_a.value) {
            this.seuil_r_a['rK' + l] = c.seuil
            this.prix_a['rK' + l] = c.prix
            l += 1;
        }

    }


    get seuils_ep() {
        return this.tarificationForm.controls['seuils_ep'] as FormArray;
    }

    get seuils_a() {
        return this.tarificationForm.controls['seuils_a'] as FormArray;
    }

    get seuils_r_a() {
        return this.tarificationForm.controls['seuils_r_a'] as FormArray;
    }

    get seuils_r_ep() {
        return this.tarificationForm.controls['seuils_r_ep'] as FormArray;
    }

    addInputControl() {
        console.log(this.seuils_ep.value.slice(-1).map((a: any) => a.prix)[0]);
        const trancheForm = this.fb.group({
            seuil: new FormControl(this.seuils_ep.value.slice(-1).map((a: any) => a.seuil)[0] + 1, {validators: [Validators.required]}),
            prix: new FormControl(this.seuils_ep.value.slice(-1).map((a: any) => a.prix)[0] + 0.0001, {validators: [Validators.required, Validators.minLength(4)]}),
        });
        this.seuils_ep.push(trancheForm);
    };

    removeInputControl(idx: number) {
        this.seuils_ep.removeAt(idx);
    }

    addInputControl_r_ep() {
        const trancheForm = this.fb.group({
            seuil: new FormControl(0, {validators: [Validators.required]}),
            prix: new FormControl('', {validators: [Validators.required, Validators.minLength(4)]}),
        });
        this.seuils_r_ep.push(trancheForm);
    };

    removeInputControl_r_ep(idx: number) {
        this.seuils_r_ep.removeAt(idx);
    }

    addInputControl_a() {
        const trancheForm = this.fb.group({
            seuil: new FormControl(0, {validators: [Validators.required]}),
            prix: new FormControl('', {validators: [Validators.required, Validators.minLength(4)]}),
        });
        this.seuils_a.push(trancheForm);
    };

    removeInputControl_a(idx: number) {
        this.seuils_a.removeAt(idx);
    }


    ngOnInit(): void {
        this.seuil_ep = {};
        this.prix_ep = {};
        this.seuil_r_ep = {};
        this.prix_r_ep = {};
        this.seuil_a = {};
        this.prix_a = {};
        this.seuil_r_a = {};

        // Check if we're in edit mode
        this.route.paramMap.subscribe(params => {
            const id = params.get('id');
            if (id) {
                this.isEditMode = true;
                this.simulationId = +id;
                this.loadSimulationData(this.simulationId);
            } else {
                this.initializeDefaultValues();
            }
        });
    }

    ngAfterViewInit(): void {
        // The population component might not be available immediately if it's in a tab
        // We'll handle this in the getPopulationData method
        console.log('AddsimulationComponent view initialized');
    }

    loadSimulationData(id: number): void {
        this.loading = true;
        this.error = '';

        this.initialApiService.getSimulationById(id).subscribe({
            next: (response) => {
                const data = response.data;

                // Clear existing form arrays
                while (this.seuils_ep.length) {
                    this.seuils_ep.removeAt(0);
                }
                while (this.seuils_a.length) {
                    this.seuils_a.removeAt(0);
                }
                while (this.seuils_r_ep.length) {
                    this.seuils_r_ep.removeAt(0);
                }
                while (this.seuils_r_a.length) {
                    this.seuils_r_a.removeAt(0);
                }

                // Update demand form
                this.demandeForm.patchValue({
                    a0: data.demande.coefficients.a0,
                    a1: data.demande.coefficients.a1,
                    a2: data.demande.coefficients.a2,
                    a3: data.demande.coefficients.a3,
                    a4: data.demande.coefficients.a4,
                    a5: data.demande.coefficients.a5,
                    a6: data.demande.coefficients.a6,
                    has_garden: data.demande.jardin,
                    has_pool: data.demande.piscine,
                    k: data.demande.k,
                    periodes: data.launch.periodes,
                    nom: data.launch.nom_simulation,
                    pauvret: data.primitives.donnees_sociales.pauvrete,
                    car: data.primitives.donnees_sociales.seuil_car,
                    par: data.primitives.donnees_sociales.seuil_par
                });

                // Update tarification form

                this.tarificationForm.patchValue({
                    coutsFixe_ep: data.primitives.ep.couts_fixes,
                    coutsVariable_ep: data.primitives.ep.couts_variables,
                    nombreAbonnes_ep: data.primitives.ep.nombre_abonnes,
                    montantAbo_ep: data.tarification.ep.abonnement,

                    coutsFixe_a: data.primitives.assainissement.couts_fixes,
                    coutsVariable_a: data.primitives.assainissement.couts_variables,
                    nombreAbonnes_a: data.primitives.assainissement.nombre_abonnes,
                    montantAbo_a: data.tarification.assainissement.abonnement,

                    cenvU: data.primitives.environnement.couts_variable_moyen,
                    env_fixed_costs: data.primitives.environnement.couts_fixes_par_an,

                    tva_ep: data.primitives.fiscalite.eau_potable.tva,
                    redevances_ep: data.primitives.fiscalite.eau_potable.redevances,

                    tva_a: data.primitives.fiscalite.assainissement.tva,
                    redevances_a: data.primitives.fiscalite.assainissement.redevances
                });

                // Add drinking water tiers
                data.tarification.ep.usage_tiers.forEach(tier => {
                    this.seuils_ep.push(this.fb.group({
                        seuil: new FormControl(tier.seuil, {validators: [Validators.required]}),
                        prix: new FormControl(tier.prix, {validators: [Validators.required, Validators.minLength(4)]})
                    }));
                });

                // Add sanitation tiers
                data.tarification.assainissement.usage_tiers.forEach(tier => {
                    this.seuils_a.push(this.fb.group({
                        seuil: new FormControl(tier.seuil, {validators: [Validators.required]}),
                        prix: new FormControl(tier.prix, {validators: [Validators.required, Validators.minLength(4)]})
                    }));
                });

                // Add redevances
                this.seuils_r_ep.push(this.fb.group({
                    seuil: new FormControl(0, {validators: [Validators.required]}),
                    prix: new FormControl(data.primitives.fiscalite.eau_potable.redevances, {validators: [Validators.required, Validators.minLength(4)]})
                }));

                this.seuils_r_a.push(this.fb.group({
                    seuil: new FormControl(0, {validators: [Validators.required]}),
                    prix: new FormControl(data.primitives.fiscalite.assainissement.redevances, {validators: [Validators.required, Validators.minLength(4)]})
                }));

                // Update population component if available
                if (this.populationComponent && data.population) {
                    // Set the useOriginalDatasource property if it exists in the API response
                    if (data.population.original_datasource !== undefined) {
                        this.populationComponent.useOriginalDatasource = data.population.original_datasource;
                    }

                    // Set other population properties
                    if (data.population.eps !== undefined) {
                        this.populationComponent.expectedPopulationSize = data.population.eps;
                    }

                    if (data.population.std !== undefined) {
                        this.populationComponent.standardDeviation = data.population.std;
                    }
                }

                this.loading = false;
            },
            error: (err) => {
                console.error('Error loading simulation:', err);
                this.loading = false;
                this.error = 'Failed to load simulation data. Please try again.';

                // Show error in snackbar
                this.snackBar.open(this.error, 'Close', {
                    duration: 5000,
                    horizontalPosition: 'center',
                    verticalPosition: 'top',
                    panelClass: ['error-snackbar']
                });

                // Initialize with default values if loading fails
                this.initializeDefaultValues();
            }
        });
    }

    initializeDefaultValues(): void {
        // Initialize with default values for new simulation
        this.seuils_r_ep.push(this.fb.group({
            seuil: new FormControl(0, {validators: [Validators.required]}),
            prix: new FormControl(0.12, {validators: [Validators.required, Validators.minLength(4)]}),
        }));
        this.seuils_ep.push(this.fb.group({
            seuil: new FormControl(0, {validators: [Validators.required]}),
            prix: new FormControl(0.878, {validators: [Validators.required, Validators.minLength(4)]}),
        }));
        this.seuils_ep.push(this.fb.group({
            seuil: new FormControl(15, {validators: [Validators.required]}),
            prix: new FormControl(1.839, {validators: [Validators.required, Validators.minLength(4)]}),
        }));
        this.seuils_ep.push(this.fb.group({
            seuil: new FormControl(30, {validators: [Validators.required]}),
            prix: new FormControl(2.768, {validators: [Validators.required, Validators.minLength(4)]}),
        }));
        this.seuils_ep.push(this.fb.group({
            seuil: new FormControl(60, {validators: [Validators.required]}),
            prix: new FormControl(4.38, {validators: [Validators.required, Validators.minLength(4)]}),
        }))

        this.seuils_a.push(this.fb.group({
            seuil: new FormControl(0, {validators: [Validators.required]}),
            prix: new FormControl(1.3, {validators: [Validators.required, Validators.minLength(4)]}),
        }));
        this.seuils_a.push(this.fb.group({
            seuil: new FormControl(15, {validators: [Validators.required]}),
            prix: new FormControl(2.12, {validators: [Validators.required, Validators.minLength(4)]}),
        }));

        this.seuils_a.push(this.fb.group({
            seuil: new FormControl(30, {validators: [Validators.required]}),
            prix: new FormControl(2.21, {validators: [Validators.required, Validators.minLength(4)]}),
        }));

        this.seuils_a.push(this.fb.group({
            seuil: new FormControl(60, {validators: [Validators.required]}),
            prix: new FormControl(2.5, {validators: [Validators.required, Validators.minLength(4)]}),
        }));

    }

    /**
     * Gets the population data from the population component
     * @returns Object containing expected population size, standard deviation, and useOriginalDatasource flag
     */
    getPopulationData(): { eps: number; std: number; useOriginalDatasource: boolean } {
        if (!this.populationComponent) {
            console.warn('Population component not available, using default values');
            return {eps: 10000, std: 0.5, useOriginalDatasource: false};
        }

        // Check if the population component has been properly initialized
        if (typeof this.populationComponent.expectedPopulationSize === 'undefined' ||
            typeof this.populationComponent.standardDeviation === 'undefined' ||
            typeof this.populationComponent.useOriginalDatasource === 'undefined') {
            console.warn('Population component values not initialized, using default values');
            return {eps: 10000, std: 0.5, useOriginalDatasource: false};
        }

        return {
            eps: this.populationComponent.expectedPopulationSize,
            std: this.populationComponent.standardDeviation,
            useOriginalDatasource: this.populationComponent.useOriginalDatasource
        };
    }


    addPreSimulation() {
        console.log(this.tarificationForm.value, this.tarificationForm.valid);
        console.log(this.demandeForm.value, this.demandeForm.valid);
        console.log(this.demandeForm.get('periodes')!.valid);
        Object.keys(this.demandeForm.controls).forEach(controlName => {
            const control = this.demandeForm.get(controlName);
            if (control && control.invalid) {
                console.log(`Control: ${controlName}`);
                console.log('Errors:', control.errors);
            }
        });
        if (!this.tarificationForm.valid || !this.demandeForm.valid) {
            this.error = 'Please fill in all required fields correctly.';
            this.snackBar.open(this.error, 'Close', {
                duration: 5000,
                horizontalPosition: 'center',
                verticalPosition: 'top',
                panelClass: ['error-snackbar']
            });
            return;
        }


        this.loading = true;
        this.error = '';

        // Process form data
        const s_ep = this.tarificationForm.controls['seuils_ep'] as FormArray;
        const s_a = this.tarificationForm.controls['seuils_a'] as FormArray;

        // Prepare drinking water usage tiers
        const drinkingWaterTiers = s_ep.value.map((tier: any) => ({
            price: tier.prix,
            threshold: tier.seuil
        }));

        // Prepare sanitation usage tiers
        const sanitationTiers = s_a.value.map((tier: any) => ({
            price: tier.prix,
            threshold: tier.seuil
        }));

        // Get population data from the population component
        const populationData = this.getPopulationData();

        console.log('Population data:', populationData);
        console.log('Population component available:', !!this.populationComponent);
        if (this.populationComponent) {
            console.log('Population component values:', {
                expectedPopulationSize: this.populationComponent.expectedPopulationSize,
                standardDeviation: this.populationComponent.standardDeviation,
                useOriginalDatasource: this.populationComponent.useOriginalDatasource
            });
        }

        // Create payload according to the required format
        const payload: SimulationPayload = {
            demand: {
                coefficients: {
                    a0: this.demandeForm.value.a0 || 0,
                    a1: this.demandeForm.value.a1 || 0,
                    a2: this.demandeForm.value.a2 || 0,
                    a3: this.demandeForm.value.a3 || 0,
                    a4: this.demandeForm.value.a4 || 0,
                    a5: this.demandeForm.value.a5 || 0,
                    a6: this.demandeForm.value.a6 || 0
                },
                has_garden: this.demandeForm.value.has_garden || false, // Default values, can be adjusted based on form data
                has_pool: this.demandeForm.value.has_pool || false,
                k: this.demandeForm.value.k || 1
            },
            launch: {
                periods: this.demandeForm.value.periodes || 10,
                simulation_name: this.demandeForm.value.nom || 'Unnamed Simulation'
            },
            population: {
                bd: 'Reunion 2010', // Default value
                original_datasource: populationData.useOriginalDatasource,
                eps: populationData.eps, // Get from population component
                std: populationData.std // Get from population component
            },
            primitives: {
                drinking_water: {
                    fixed_costs: this.tarificationForm.value.coutsFixe_ep || 0,
                    number_of_subscribers: this.tarificationForm.value.nombreAbonnes_ep || 0,
                    variable_costs: this.tarificationForm.value.coutsVariable_ep || 0
                },
                environment: {
                    average_variable_cost: this.tarificationForm.value.cenvU || 0,
                    fixed_costs_per_year: this.tarificationForm.value.env_fixed_costs || 0// Default value
                },
                sanitation: {
                    fixed_costs: this.tarificationForm.value.coutsFixe_a || 0,
                    number_of_subscribers: this.tarificationForm.value.nombreAbonnes_a || 0,
                    variable_costs: this.tarificationForm.value.coutsVariable_a || 0
                },
                social_data: {
                    poverty: this.demandeForm.value.pauvret || 0,
                    threshold_car: this.demandeForm.value.car || 0,
                    threshold_par: this.demandeForm.value.par || 0
                },
                taxation: {
                    drinking_water: {
                        fees: this.tarificationForm.value.redevances_ep || 0,
                        vat: this.tarificationForm.value.tva_ep || 0
                    },
                    sanitation: {
                        fees: this.tarificationForm.value.redevances_a || 0,
                        vat: this.tarificationForm.value.tva_a || 0
                    }
                }
            },
            tariff: {
                drinking_water: {
                    subscription: this.tarificationForm.value.montantAbo_ep || 0,
                    usage_tiers: drinkingWaterTiers
                },
                sanitation: {
                    subscription: this.tarificationForm.value.montantAbo_a || 0,
                    usage_tiers: sanitationTiers
                }
            }
        };

        // Send data to the API - either create or update based on mode
        if (this.isEditMode && this.simulationId) {
            // Update existing simulation
            this.initialApiService.updateSimulation(this.simulationId, payload).subscribe({
                next: (response) => {
                    console.log('Simulation updated successfully:', response);
                    this.loading = false;
                    // Navigate to the simulation details page or show success message
                    const successMessage = `Simulation "${response.data.name}" updated successfully with ID: ${response.data.simulation_id}`;
                    this.snackBar.open(successMessage, 'Close', {
                        duration: 5000,
                        horizontalPosition: 'center',
                        verticalPosition: 'top',
                        panelClass: ['success-snackbar']
                    });
                    this.router.navigateByUrl('/home');
                },
                error: (error) => {
                    console.error('Error updating simulation:', error);
                    this.loading = false;
                    this.error = error.error?.detail || 'Failed to update simulation. Please try again.';
                    this.snackBar.open(this.error, 'Close', {
                        duration: 5000,
                        horizontalPosition: 'center',
                        verticalPosition: 'top',
                        panelClass: ['error-snackbar']
                    });
                }
            });
        } else {
            // Create new simulation
            this.initialApiService.createSimulation(payload).subscribe({
                next: (response) => {
                    console.log('Simulation created successfully:', response);
                    this.loading = false;
                    // Navigate to the simulation details page or show success message
                    const successMessage = `Simulation "${response.data.name}" created successfully with ID: ${response.data.simulation_id}`;
                    this.snackBar.open(successMessage, 'Close', {
                        duration: 5000,
                        horizontalPosition: 'center',
                        verticalPosition: 'top',
                        panelClass: ['success-snackbar']
                    });
                    this.router.navigateByUrl('/home');
                },
                error: (error) => {
                    console.error('Error creating simulation:', error);
                    this.loading = false;
                    this.error = error.error?.detail[0].msg || 'Failed to create simulation. Please try again.';
                    this.snackBar.open(this.error, 'Close', {
                        duration: 5000,
                        horizontalPosition: 'center',
                        verticalPosition: 'top',
                        panelClass: ['error-snackbar']
                    });
                }
            });
        }
    }

    loadSmimulationStep() {

    }

}
