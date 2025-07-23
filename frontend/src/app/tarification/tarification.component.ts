import { HttpClient } from '@angular/common/http';
import { Component,OnInit } from '@angular/core';
import { FormArray, FormControl, FormBuilder, Validators } from '@angular/forms';
import {Chart,} from 'chart.js/auto';
import { map, catchError, of } from 'rxjs';
import { ajax } from "rxjs/ajax";

@Component({
  selector: 'app-tarification',
  templateUrl: './tarification.component.html',
  styleUrls: ['./tarification.component.css']
})

export class TarificationComponent implements OnInit {
  constructor(private http : HttpClient,private fb:FormBuilder){}

  seuil_ep!: { [key: string]: number };
  prix_ep!: { [key: string]: number };
  seuil_r_ep!: { [key: string]: number };
  prix_r_ep!: { [key: string]: number };

  seuil_a!: { [key: string]: number };
  prix_a!: { [key: string]: number };
  seuil_r_a!: { [key: string]: number };
  prix_r_a!: { [key: string]: number };

  tarificationForm= this.fb.group({

  coutsFixe_ep : new FormControl('',{validators: [Validators.required]}),
  coutsVariable_ep : new FormControl('',{validators: [Validators.required]}),
  montantAbo_ep : new FormControl('',{validators: [Validators.required]}),
  nombreAbonnes_ep : new FormControl('',{validators: [Validators.required]}),
  tva_ep : new FormControl('',{validators: [Validators.required]}),
  seuils_ep : this.fb.array([]),
  seuils_r_ep : this.fb.array([]),

  coutsFixe_a : new FormControl('',{validators: [Validators.required]}),
  coutsVariable_a : new FormControl('',{validators: [Validators.required]}),
  nombreAbonnes_a : new FormControl('',{validators: [Validators.required]}),
  montantAbo_a : new FormControl('',{validators: [Validators.required]}),
  tva_a : new FormControl('',{validators: [Validators.required]}),
  seuils_a : this.fb.array([]),
  seuils_r_a : this.fb.array([]),

  });

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

  submitTarification(){

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
      i+=1;
    }
    for (let c of s_a.value){
      this.seuil_a['aK'+j]=c.seuil
      this.prix_a['aK'+j]=c.prix
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
    console.log(this.seuil_ep,this.prix_ep);
    console.log(this.seuil_a,this.prix_a);
    this.http.post('http://localhost:5001/api/post', 
    { //Raw : this.tarificationForm.value,
      
      seuil_ep : this.seuil_ep,
      prix_ep : this.prix_ep,
      seuil_r_ep : this.seuil_r_ep,
      prix_r_ep : this.prix_r_ep,
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

    }  ).subscribe();

    //seuils_r_ep : this.fb.array([]),
    //seuils_r_a : this.fb.array([]),
    /*
        const users = ajax({
      url: 'http://localhost:5001/api/post',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: {
        rxjs: 'Hello World!'
      }
    }).pipe(
      map(response => console.log('response: ', response)),
      catchError(error => {
        console.log('error: ', error);
        return of(error);
      })
    );
    ajax({
      url: 'http://localhost:5001/api/post',
      method: 'POST',
      headers: { 'Content-Type': 'application/json'},
      body: JSON.stringify({
        "CV": this.coutsVariable.value,
        "CF": this.coutsFixe.value,
      })
    }).pipe(map((data:any)=>console.log(data.response )))
    */
  }
  /*
  addInputControl(){
    this.seuils.push(new FormControl(0,Validators.required) );
    this.prix.push(new FormControl(0,Validators.required) );
  }
  removeInputControl(idx: number) {
    this.seuils.removeAt(idx);
    this.prix.removeAt(idx);
  }
  */
  ngOnInit(): void {
    this.seuil_ep={};
    this.prix_ep={};
    this.seuil_r_ep={};
    this.prix_r_ep={};
    this.seuil_a={};
    this.prix_a={};
    this.seuil_r_a={};
    this.prix_r_a={};
    this.chart;
    this.createChart();
    this.seuils_ep.push(this.fb.group({
      seuil: new FormControl(0, {validators: [Validators.required]}),
      prix: new FormControl('', {validators: [Validators.required,Validators.minLength(4)]}),
    }));
    this.seuils_a.push(this.fb.group({
      seuil: new FormControl(0, {validators: [Validators.required]}),
      prix: new FormControl('', {validators: [Validators.required,Validators.minLength(4)]}),
    }));
    this.seuils_r_a.push(this.fb.group({
      seuil: new FormControl(0, {validators: [Validators.required]}),
      prix: new FormControl('', {validators: [Validators.required,Validators.minLength(4)]}),
    }));
    this.seuils_r_ep.push(this.fb.group({
      seuil: new FormControl(0, {validators: [Validators.required]}),
      prix: new FormControl('', {validators: [Validators.required,Validators.minLength(4)]}),
    }));
    /*
    ajax({
      url: 'localhost:5001/api/post',
      method: 'POST',
      headers: { 'Content-Type': 'application/json'},
      body: JSON.stringify({
        "CV": this.coutsVariable.value,
        "CF": this.coutsFixe.value,
      })
    })*/
  }
  public chart: any;
  createChart(){
    const hori={
      id:'hori',

    }
  
    this.chart = new Chart("MyChart", {
      type: 'line', 

      data: {// values on X-Axis
        labels: [0, 45, 60,80,
								 ], 
	       datasets: [
          {
            label: "Escalier des prix marginaux",
            data: [1.22,1.45,2.3,2.5,],
            backgroundColor: 'blue',
            stepped: true,
          },
          {
            label: "prix",
            data: [1.8,1.8,1.8,1.8,],
            pointStyle:false,
            
            stepped: true,
          },

        ]
      },
      options: {
        aspectRatio:1
      },
      plugins: [hori]
      
    });
  }
}
