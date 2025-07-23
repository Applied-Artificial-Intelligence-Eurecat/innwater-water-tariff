import { Component, OnInit } from '@angular/core';
import { FormArray, FormControl, FormBuilder, Validators } from '@angular/forms';
@Component({
  selector: 'app-consomation',
  templateUrl: './consomation.component.html',
  styleUrls: ['./consomation.component.css']
})
export class ConsomationComponent implements OnInit {
  constructor( private fb:FormBuilder){}
  demandeForm = this.fb.group({
    a0 : new FormControl(-2.56,{validators: [Validators.required]}),
    a1 : new FormControl(0.48,{validators: [Validators.required]}),
    a2 : new FormControl(0.44,{validators: [Validators.required]}),
    a3 : new FormControl(0.12,{validators: [Validators.required]}),
    a4 : new FormControl(0.37,{validators: [Validators.required]}),
    a5 : new FormControl(0.31,{validators: [Validators.required]}),
    a6 : new FormControl(0.25,{validators: [Validators.required]}),
    car : new FormControl('',{validators: [Validators.required]}),
    par : new FormControl('',{validators: [Validators.required]}),
    k : new FormControl('',{validators: [Validators.required]}),
  })

  ngOnInit(): void {
    console.log(this.demandeForm.value);
  }

}
