import {Component, OnInit} from '@angular/core';
import {FormArray, FormBuilder, FormControl, Validators} from "@angular/forms";
import {Router} from "@angular/router";

@Component({
    selector: 'app-first-round-assessment',
    templateUrl: './first-round-assessment.component.html',
    styleUrls: ['./first-round-assessment.component.css']
})
export class FirstRoundAssessmentComponent implements OnInit {
    seuil_ep!: { [key: string]: number };
    prix_ep!: { [key: string]: number };
    seuil_r_ep!: { [key: string]: number };
    prix_r_ep!: { [key: string]: number };
    disabled: boolean = false;
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

    constructor(private fb: FormBuilder, private router: Router) {
    }

    ngOnInit(): void {
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
}
