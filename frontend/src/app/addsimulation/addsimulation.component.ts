import { Component,OnInit } from '@angular/core';
import { FormArray, FormControl, FormBuilder, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
@Component({
  selector: 'app-addsimulation',
  templateUrl: './addsimulation.component.html',
  styleUrls: ['./addsimulation.component.css']
})
export class AddsimulationComponent implements OnInit{
  seuil_ep!: { [key: string]: number };
  prix_ep!: { [key: string]: number };
  seuil_r_ep!: { [key: string]: number };
  prix_r_ep!: { [key: string]: number };

  seuil_a!: { [key: string]: number };
  prix_a!: { [key: string]: number };
  seuil_r_a!: { [key: string]: number };
  prix_r_a!: { [key: string]: number };
  disabled: boolean = false;

  tab_pep:number[]=[];
  tab_sep:number[]=[];
  tab_pa:number[]=[];
  tab_sa:number[]=[];
  constructor( private http : HttpClient,private fb:FormBuilder,private router: Router){}

  demandeForm = this.fb.group({
    a0 : new FormControl({value:-2.56,disabled: this.disabled},{validators: [Validators.required]}),
    a1 : new FormControl({value:0.48,disabled: this.disabled},{validators: [Validators.required]}),
    a2 : new FormControl({value:0.44,disabled: this.disabled},{validators: [Validators.required]}),
    a3 : new FormControl({value:0.12,disabled: this.disabled},{validators: [Validators.required]}),
    a4 : new FormControl({value:0.37,disabled: this.disabled},{validators: [Validators.required]}),
    a5 : new FormControl({value:-0.31,disabled: this.disabled},{validators: [Validators.required]}),
    a6 : new FormControl({value:0.25,disabled: this.disabled},{validators: [Validators.required]}),
    car : new FormControl({value:3,disabled: this.disabled},{validators: [Validators.required]}),
    par : new FormControl({value:3,disabled: this.disabled},{validators: [Validators.required]}),
    k : new FormControl({value:0,disabled: this.disabled},{validators: [Validators.required]}),
    periodes : new FormControl({value:4,disabled: this.disabled},{validators: [Validators.required]}),
    nom:new FormControl('',{validators: [Validators.required]}),
    pauvret : new FormControl({value:800,disabled: this.disabled},{validators: [Validators.required]}),
    pauvretE : new FormControl({value:500,disabled: this.disabled},{validators: [Validators.required]}),
  });
  tarificationForm= this.fb.group({

    coutsFixe_ep : new FormControl({value:1250000,disabled: this.disabled},{validators: [Validators.required]}),
    coutsVariable_ep : new FormControl(0.7,{validators: [Validators.required]}),
    montantAbo_ep : new FormControl(15,{validators: [Validators.required]}),
    nombreAbonnes_ep : new FormControl(48000,{validators: [Validators.required]}),
    redevances_ep : new FormControl(0.01,{validators: [Validators.required]}),
    tva_ep : new FormControl(2.1,{validators: [Validators.required]}),
    seuils_ep : this.fb.array([]),
    seuils_r_ep : this.fb.array([]),
  
    coutsFixe_a : new FormControl(720000,{validators: [Validators.required]}),
    coutsVariable_a : new FormControl(0.6,{validators: [Validators.required]}),
    nombreAbonnes_a : new FormControl(22000,{validators: [Validators.required]}),
    montantAbo_a : new FormControl(15,{validators: [Validators.required]}),
    redevances_a : new FormControl(0.06,{validators: [Validators.required]}),
    tva_a : new FormControl(0,{validators: [Validators.required]}),
    seuils_a : this.fb.array([]),
    seuils_r_a : this.fb.array([]),

    cenvU:new FormControl(1.3,{validators: [Validators.required]}),
  
    });
    isLinear = true;
    addSimulation(){
      console.log(this.demandeForm.value);
      const s_ep = this.tarificationForm.controls['seuils_ep'] as FormArray;
    const s_a = this.tarificationForm.controls['seuils_a'] as FormArray;
    const s_r_ep = this.tarificationForm.controls['seuils_r_ep'] as FormArray;
    const s_r_a = this.tarificationForm.controls['seuils_r_a'] as FormArray;
    let i:number =0;
    let j:number =0;
    let k:number=0;
    let l:number=0;
    for (let c of s_ep.value){
      this.seuil_ep['K'+i]=c.seuil
      this.prix_ep['K'+i]=c.prix
      this.tab_pep.push(c.prix)
      this.tab_sep.push(c.seuil)
      i+=1;
    }
    for (let c of s_a.value){
      this.seuil_a['aK'+j]=c.seuil
      this.prix_a['aK'+j]=c.prix
      this.tab_pa.push(c.prix)
      this.tab_sa.push(c.seuil)
      j+=1;
    }
    for (let c of s_r_ep.value){
      this.seuil_r_ep['rK'+k]=c.seuil
      this.prix_r_ep['rK'+k]=c.prix
      k+=1;
    }
    for (let c of s_r_a.value){
      this.seuil_r_a['rK'+l]=c.seuil
      this.prix_r_a['rK'+l]=c.prix
      l+=1;
    }
    this.http.post('http://localhost:5001/api/postSim', 
    { //Raw : this.tarificationForm.value,
      coeff : this.demandeForm.value,
      seuil_ep : this.seuil_ep,
      prix_ep : this.prix_ep,
      seuil_r_ep : this.seuil_r_ep,
      prix_r_ep : this.prix_r_ep,
      cenvU : this.tarificationForm.value.cenvU,
      tva_ep : this.tarificationForm.value.tva_ep,
      abo_ep : this.tarificationForm.value.montantAbo_ep,
      couts_fixe_ep: this.tarificationForm.value.coutsFixe_ep,
      couts_unitaire_ep: this.tarificationForm.value.coutsVariable_ep,
      nombre_abonn_ep: this.tarificationForm.value.nombreAbonnes_ep,

      seuil_a : this.seuil_a,
      prix_a : this.prix_a,
      seuil_r_a : this.seuil_r_a,
      prix_r_a : this.prix_r_a,
      tva_a : this.tarificationForm.value.tva_a,
      abo_a : this.tarificationForm.value.montantAbo_a,
      couts_fixe_a: this.tarificationForm.value.coutsFixe_a,
      couts_unitaire_a: this.tarificationForm.value.coutsVariable_a,
      nombre_abonn_a: this.tarificationForm.value.nombreAbonnes_a,

      redevances_ep: this.tarificationForm.value.redevances_ep,
      redevances_a: this.tarificationForm.value.redevances_a,

      tabpep:this.tab_pep,
      tabsep: this.tab_sep,

      tabpa:this.tab_pa,
      tabsa: this.tab_sa,
      
      userid:localStorage.getItem('userid'),

    }  ).subscribe({next:data=>{console.log(data);this.router.navigateByUrl('/last');},
    error:error =>{console.log(error);
      alert('erreur');
    }});
    }


    get seuils_ep(){
      return this.tarificationForm.controls['seuils_ep'] as FormArray;
      }
      get seuils_a(){
      return this.tarificationForm.controls['seuils_a'] as FormArray;
      }
      get seuils_r_a(){
      return this.tarificationForm.controls['seuils_r_a'] as FormArray;
      }
      get seuils_r_ep(){
      return this.tarificationForm.controls['seuils_r_ep'] as FormArray;
      }
    
      addInputControl(){
        console.log(this.seuils_ep.value.slice(-1).map((a:any) => a.prix)[0]);
      const   trancheForm = this.fb.group({
        seuil: new FormControl(this.seuils_ep.value.slice(-1).map((a:any) => a.seuil)[0]+1, {validators: [Validators.required]}),
        prix: new FormControl(this.seuils_ep.value.slice(-1).map((a:any) => a.prix)[0]+0.0001, {validators: [Validators.required,Validators.minLength(4)]}),
      });
      this.seuils_ep.push(trancheForm);
      };
      removeInputControl(idx: number) {
      this.seuils_ep.removeAt(idx);
      }
      addInputControl_r_ep(){
        const   trancheForm = this.fb.group({
          seuil: new FormControl(0, {validators: [Validators.required]}),
          prix: new FormControl('', {validators: [Validators.required,Validators.minLength(4)]}),
        });
        this.seuils_r_ep.push(trancheForm);
        };
        removeInputControl_r_ep(idx: number) {
        this.seuils_r_ep.removeAt(idx);
        }
    
      addInputControl_a(){
        const   trancheForm = this.fb.group({
          seuil: new FormControl(0, {validators: [Validators.required]}),
          prix: new FormControl('', {validators: [Validators.required,Validators.minLength(4)]}),
        });
        this.seuils_a.push(trancheForm);
        };
        removeInputControl_a(idx: number) {
        this.seuils_a.removeAt(idx);
        }
        addInputControl_r_a(){
          const   trancheForm = this.fb.group({
            seuil: new FormControl(0, {validators: [Validators.required]}),
            prix: new FormControl('', {validators: [Validators.required,Validators.minLength(4)]}),
          });
          this.seuils_r_a.push(trancheForm);
          };
          removeInputControl_r_a(idx: number) {
          this.seuils_r_a.removeAt(idx);
          }
    
    ngOnInit(): void {
      this.seuil_ep={};
      this.prix_ep={};
      this.seuil_r_ep={};
      this.prix_r_ep={};
      this.seuil_a={};
      this.prix_a={};
      this.seuil_r_a={};
      this.prix_r_a={};
      /*
      this.seuils_r_ep.push(this.fb.group({
        seuil: new FormControl(0, {validators: [Validators.required]}),
        prix: new FormControl(0.12, {validators: [Validators.required,Validators.minLength(4)]}),
      }));

      
      this.seuils_ep.push(this.fb.group({
        seuil: new FormControl(0, {validators: [Validators.required]}),
        prix: new FormControl('', {validators: [Validators.required,Validators.minLength(4)]}),
      }));
      this.seuils_ep.push(this.fb.group({
        seuil: new FormControl('', {validators: [Validators.required]}),
        prix: new FormControl('', {validators: [Validators.required,Validators.minLength(4)]}),
      }));
      this.seuils_a.push(this.fb.group({
        seuil: new FormControl(0, {validators: [Validators.required]}),
        prix: new FormControl('', {validators: [Validators.required,Validators.minLength(4)]}),
      }));
      this.seuils_r_a.push(this.fb.group({
        seuil: new FormControl(0, {validators: [Validators.required]}),
        prix: new FormControl(0.04, {validators: [Validators.required,Validators.minLength(4)]}),
      }));
      */
      
      
      this.seuils_r_ep.push(this.fb.group({
        seuil: new FormControl(0, {validators: [Validators.required]}),
        prix: new FormControl(0.12, {validators: [Validators.required,Validators.minLength(4)]}),
      }));
      this.seuils_ep.push(this.fb.group({
        seuil: new FormControl(0, {validators: [Validators.required]}),
        prix: new FormControl(0.5, {validators: [Validators.required,Validators.minLength(4)]}),
      }));
      this.seuils_ep.push(this.fb.group({
        seuil: new FormControl(30, {validators: [Validators.required]}),
        prix: new FormControl(2.05, {validators: [Validators.required,Validators.minLength(4)]}),
      }));
      this.seuils_ep.push(this.fb.group({
        seuil: new FormControl(60, {validators: [Validators.required]}),
        prix: new FormControl(2.2680, {validators: [Validators.required,Validators.minLength(4)]}),
      }));
     
      this.seuils_a.push(this.fb.group({
        seuil: new FormControl(0, {validators: [Validators.required]}),
        prix: new FormControl(0.6, {validators: [Validators.required,Validators.minLength(4)]}),
      }));
      this.seuils_a.push(this.fb.group({
        seuil: new FormControl(40, {validators: [Validators.required]}),
        prix: new FormControl(2.5, {validators: [Validators.required,Validators.minLength(4)]}),
      }));
      
      this.seuils_r_a.push(this.fb.group({
        seuil: new FormControl(0, {validators: [Validators.required]}),
        prix: new FormControl(0.04, {validators: [Validators.required,Validators.minLength(4)]}),
      }));
      

      

}

addPreSimulation() {
  this.router.navigateByUrl('/table'); // 🔄 Redirection vers app-table
}

loadSmimulationStep(){
  
}

}