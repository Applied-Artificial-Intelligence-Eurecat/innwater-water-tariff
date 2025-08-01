import {Component, OnInit} from '@angular/core';
import {FormArray, FormBuilder, FormControl, Validators} from '@angular/forms';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {ActivatedRoute, Router} from '@angular/router';
import {InitialAPIService, SimulationPayload} from '../initial-api.service';
import {DomSanitizer, SafeResourceUrl} from "@angular/platform-browser";

@Component({
    selector: 'app-addsimulation',
    templateUrl: './addsimulation.component.html',
    styleUrls: ['./addsimulation.component.css']
})
export class AddsimulationComponent implements OnInit {
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
    ) {
    }

    demandeForm = this.fb.group({
        a0: new FormControl({value: -2.56, disabled: this.disabled}, {validators: [Validators.required]}),
        a1: new FormControl({value: 0.48, disabled: this.disabled}, {validators: [Validators.required]}),
        a2: new FormControl({value: 0.44, disabled: this.disabled}, {validators: [Validators.required]}),
        a3: new FormControl({value: 0.12, disabled: this.disabled}, {validators: [Validators.required]}),
        a4: new FormControl({value: 0.37, disabled: this.disabled}, {validators: [Validators.required]}),
        a5: new FormControl({value: -0.31, disabled: this.disabled}, {validators: [Validators.required]}),
        a6: new FormControl({value: 0.25, disabled: this.disabled}, {validators: [Validators.required]}),
        car: new FormControl({value: 3, disabled: this.disabled}, {validators: [Validators.required]}),
        par: new FormControl({value: 3, disabled: this.disabled}, {validators: [Validators.required]}),
        k: new FormControl({value: 0, disabled: this.disabled}, {validators: [Validators.required]}),
        periodes: new FormControl({value: 4, disabled: this.disabled}, {validators: [Validators.required]}),
        nom: new FormControl('', {validators: [Validators.required]}),
        pauvret: new FormControl({value: 800, disabled: this.disabled}, {validators: [Validators.required]}),
        pauvretE: new FormControl({value: 500, disabled: this.disabled}, {validators: [Validators.required]}),
    });
    tarificationForm = this.fb.group({

        coutsFixe_ep: new FormControl({value: 1250000, disabled: this.disabled}, {validators: [Validators.required]}),
        coutsVariable_ep: new FormControl(0.7, {validators: [Validators.required]}),
        montantAbo_ep: new FormControl(15, {validators: [Validators.required]}),
        nombreAbonnes_ep: new FormControl(48000, {validators: [Validators.required]}),
        redevances_ep: new FormControl(0.01, {validators: [Validators.required]}),
        tva_ep: new FormControl(2.1, {validators: [Validators.required]}),
        seuils_ep: this.fb.array([]),
        seuils_r_ep: this.fb.array([]),

        coutsFixe_a: new FormControl(720000, {validators: [Validators.required]}),
        coutsVariable_a: new FormControl(0.6, {validators: [Validators.required]}),
        nombreAbonnes_a: new FormControl(22000, {validators: [Validators.required]}),
        montantAbo_a: new FormControl(15, {validators: [Validators.required]}),
        redevances_a: new FormControl(0.06, {validators: [Validators.required]}),
        tva_a: new FormControl(0, {validators: [Validators.required]}),
        seuils_a: this.fb.array([]),
        seuils_r_a: this.fb.array([]),

        cenvU: new FormControl(1.3, {validators: [Validators.required]}),
        env_fixed_costs: new FormControl(25000, {validators: [Validators.required]}),

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

    addInputControl_r_a() {
        const trancheForm = this.fb.group({
            seuil: new FormControl(0, {validators: [Validators.required]}),
            prix: new FormControl('', {validators: [Validators.required, Validators.minLength(4)]}),
        });
        this.seuils_r_a.push(trancheForm);
    };

    removeInputControl_r_a(idx: number) {
        this.seuils_r_a.removeAt(idx);
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
                    a0: data.demand.coefficients.a0,
                    a1: data.demand.coefficients.a1,
                    a2: data.demand.coefficients.a2,
                    a3: data.demand.coefficients.a3,
                    a4: data.demand.coefficients.a4,
                    a5: data.demand.coefficients.a5,
                    a6: data.demand.coefficients.a6,
                    k: data.demand.k,
                    periodes: data.launch.periods,
                    nom: data.launch.simulation_name,
                    pauvret: data.primitives.donnees_sociales.pauvrete,
                    pauvretE: data.primitives.donnees_sociales.grande_pauvrete,
                    car: data.primitives.donnees_sociales.seuil_car,
                    par: data.primitives.donnees_sociales.seuil_par
                });

                // Update tarification form
                this.tarificationForm.patchValue({
                    coutsFixe_ep: data.primitives.ep.couts_fixes,
                    coutsVariable_ep: data.primitives.ep.couts_variables,
                    nombreAbonnes_ep: data.primitives.ep.nombre_abonnes,
                    montantAbo_ep: data.tariff.ep.abonnement,

                    coutsFixe_a: data.primitives.assainissement.couts_fixes,
                    coutsVariable_a: data.primitives.assainissement.couts_variables,
                    nombreAbonnes_a: data.primitives.assainissement.nombre_abonnes,
                    montantAbo_a: data.tariff.assainissement.abonnement,

                    cenvU: data.primitives.environnement.couts_variable_moyen,
                    env_fixed_costs: data.primitives.environnement.couts_fixes_par_an,

                    tva_ep: data.primitives.fiscalite.eau_potable.tva,
                    redevances_ep: data.primitives.fiscalite.eau_potable.redevances,

                    tva_a: data.primitives.fiscalite.assainissement.tva,
                    redevances_a: data.primitives.fiscalite.assainissement.redevances
                });

                // Add drinking water tiers
                data.tariff.ep.usage_tiers.forEach(tier => {
                    this.seuils_ep.push(this.fb.group({
                        seuil: new FormControl(tier.seuil, {validators: [Validators.required]}),
                        prix: new FormControl(tier.prix, {validators: [Validators.required, Validators.minLength(4)]})
                    }));
                });

                // Add sanitation tiers
                data.tariff.assainissement.usage_tiers.forEach(tier => {
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

                this.loading = false;
            },
            error: (err) => {
                console.error('Error loading simulation:', err);
                this.loading = false;
                this.error = 'Failed to load simulation data. Please try again.';

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
            prix: new FormControl(0.5, {validators: [Validators.required, Validators.minLength(4)]}),
        }));
        this.seuils_ep.push(this.fb.group({
            seuil: new FormControl(30, {validators: [Validators.required]}),
            prix: new FormControl(2.05, {validators: [Validators.required, Validators.minLength(4)]}),
        }));
        this.seuils_ep.push(this.fb.group({
            seuil: new FormControl(60, {validators: [Validators.required]}),
            prix: new FormControl(2.2680, {validators: [Validators.required, Validators.minLength(4)]}),
        }));

        this.seuils_a.push(this.fb.group({
            seuil: new FormControl(0, {validators: [Validators.required]}),
            prix: new FormControl(0.6, {validators: [Validators.required, Validators.minLength(4)]}),
        }));
        this.seuils_a.push(this.fb.group({
            seuil: new FormControl(40, {validators: [Validators.required]}),
            prix: new FormControl(2.5, {validators: [Validators.required, Validators.minLength(4)]}),
        }));

        this.seuils_r_a.push(this.fb.group({
            seuil: new FormControl(0, {validators: [Validators.required]}),
            prix: new FormControl(0.04, {validators: [Validators.required, Validators.minLength(4)]}),
        }));
    }


    addPreSimulation() {
        if (!this.tarificationForm.valid || !this.demandeForm.valid) {
            this.error = 'Please fill in all required fields correctly.';
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
                has_garden: true, // Default values, can be adjusted based on form data
                has_pool: false,
                k: this.demandeForm.value.k || 1
            },
            launch: {
                periods: this.demandeForm.value.periodes || 10,
                simulation_name: this.demandeForm.value.nom || 'Unnamed Simulation'
            },
            population: {
                bd: 'lognormal', // Default value
                eps: 10000, // Default value
                std: 0.5 // Default value
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
                    extreme_poverty: this.demandeForm.value.pauvretE || 0,
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
                    alert(`Simulation "${response.data.name}" updated successfully with ID: ${response.data.simulation_id}`);
                    this.router.navigateByUrl('/home');
                },
                error: (error) => {
                    console.error('Error updating simulation:', error);
                    this.loading = false;
                    this.error = error.error?.detail || 'Failed to update simulation. Please try again.';
                    alert(this.error);
                }
            });
        } else {
            // Create new simulation
            this.initialApiService.createSimulation(payload).subscribe({
                next: (response) => {
                    console.log('Simulation created successfully:', response);
                    this.loading = false;
                    // Navigate to the simulation details page or show success message
                    alert(`Simulation "${response.data.name}" created successfully with ID: ${response.data.simulation_id}`);
                    this.router.navigateByUrl('/home');
                },
                error: (error) => {
                    console.error('Error creating simulation:', error);
                    this.loading = false;
                    this.error = error.error?.detail || 'Failed to create simulation. Please try again.';
                    alert(this.error);
                }
            });
        }
    }

    loadSmimulationStep() {

    }

}
