import {Component, OnInit} from '@angular/core';
import {FormArray, FormBuilder, FormControl, Validators} from "@angular/forms";
import {ActivatedRoute, Router} from "@angular/router";
import {SmallAssessmentService, SmallAssessmentUpdatePayload} from "../small-assessment.service";

@Component({
    selector: 'app-first-round-assessment',
    templateUrl: './first-round-assessment.component.html',
    styleUrls: ['./first-round-assessment.component.css']
})
export class FirstRoundAssessmentComponent implements OnInit {
    tarificationForm = this.fb.group({

        montantAbo_ep: new FormControl(15, {validators: [Validators.required]}),
        seuils_ep: this.fb.array([]),
        seuils_r_ep: this.fb.array([]),

        nombreAbonnes_a: new FormControl(22000, {validators: [Validators.required]}),
        montantAbo_a: new FormControl(15, {validators: [Validators.required]}),
        seuils_a: this.fb.array([]),
        seuils_r_a: this.fb.array([]),


    });
    simulationId: number | null = null;

    constructor(
        private fb: FormBuilder,
        private router: Router,
        private route: ActivatedRoute,
        private smallAssessmentService: SmallAssessmentService
    ) {
    }

    ngOnInit(): void {
        this.route.paramMap.subscribe(params => {
            const id = params.get('id');
            this.simulationId = id ? +id : null;

            if (this.simulationId) {
                this.loadSmallAssessmentData(this.simulationId);
            }
        })
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

    removeInputControl_a(idx: number) {
        this.seuils_a.removeAt(idx);
    }


    addInputControl_a() {
        const trancheForm = this.fb.group({
            seuil: new FormControl(0, {validators: [Validators.required]}),
            prix: new FormControl('', {validators: [Validators.required, Validators.minLength(4)]}),
        });
        this.seuils_a.push(trancheForm);
    };

    /**
     * Loads small assessment data from the API and updates the form
     * @param id The simulation ID
     */
    loadSmallAssessmentData(id: number): void {
        this.smallAssessmentService.getSmallAssessment(id).subscribe(
            (data) => {
                // Update EP subscription
                this.tarificationForm.get('montantAbo_ep')?.setValue(data.ep.abonnement);

                // Update EP usage tiers
                this.seuils_ep.clear();
                data.ep.usage_tiers.forEach(tier => {
                    const tierGroup = this.fb.group({
                        seuil: new FormControl(tier.seuil, {validators: [Validators.required]}),
                        prix: new FormControl(tier.prix, {validators: [Validators.required]}),
                    });
                    this.seuils_ep.push(tierGroup);
                });

                // Update Assainissement subscription
                this.tarificationForm.get('montantAbo_a')?.setValue(data.assainissement.abonnement);

                // Update Assainissement usage tiers
                this.seuils_a.clear();
                data.assainissement.usage_tiers.forEach(tier => {
                    const tierGroup = this.fb.group({
                        seuil: new FormControl(tier.seuil, {validators: [Validators.required]}),
                        prix: new FormControl(tier.prix, {validators: [Validators.required]}),
                    });
                    this.seuils_a.push(tierGroup);
                });
            },
            (error) => {
                console.error('Error loading small assessment data:', error);
            }
        );
    }

    /**
     * Updates the small assessment data via the API
     */
    updateSmallAssessmentData(): void {
        if (!this.simulationId) {
            console.error('No simulation ID available');
            return;
        }

        // Create the payload from the form data
        const payload: SmallAssessmentUpdatePayload = {
            ep: {
                subscription: this.tarificationForm.get('montantAbo_ep')!.value as number,
                usage_tiers: this.seuils_ep.value.map((tier: any) => {
                    return {
                        seuil: tier.seuil,
                        prix: tier.prix
                    }
                })
            },
            assainissement: {
                subscription: this.tarificationForm.get('montantAbo_a')!.value as number,
                usage_tiers: this.seuils_a.value.map((tier: any) => {
                    return {
                        seuil: tier.seuil,
                        prix: tier.prix
                    }
                })
            }
        };

        this.smallAssessmentService.updateSmallAssessment(this.simulationId, payload).subscribe({
                next: (data) => {
                    console.log('Small assessment updated successfully');
                    this.loadSmallAssessmentData(this.simulationId!)
                },
                error: (error) => {
                    console.error('Error updating small assessment:', error);
                }
            }
        );
    }

    validateAndSimulate() {
        if (!this.simulationId) {
            console.error('No simulation ID available');
            return;
        }
        const payload: SmallAssessmentUpdatePayload = {
            ep: {
                subscription: this.tarificationForm.get('montantAbo_ep')!.value as number,
                usage_tiers: this.seuils_ep.value.map((tier: any) => {
                    return {
                        seuil: tier.seuil,
                        prix: tier.prix
                    }
                })
            },
            assainissement: {
                subscription: this.tarificationForm.get('montantAbo_a')!.value as number,
                usage_tiers: this.seuils_a.value.map((tier: any) => {
                    return {
                        seuil: tier.seuil,
                        prix: tier.prix
                    }
                })
            }
        };

        this.smallAssessmentService.validateAndSimulate(this.simulationId, payload).subscribe({
            next: (data) => {
                if (data.status === 'success') {
                    this.router.navigate(['/simulation/details/', this.simulationId]);
                } else {
                    alert(data.message)
                }
            },
            error: (error) => {
                console.error('Error starting simulation:', error);
            }
        })

    }
}
