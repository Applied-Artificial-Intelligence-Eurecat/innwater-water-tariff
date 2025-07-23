import { Component, OnInit } from '@angular/core';
import {FormArray, FormBuilder, Validators,FormControl} from '@angular/forms';
@Component({
  selector: 'app-test-t',
  templateUrl: './test-t.component.html',
  styleUrls: ['./test-t.component.css']
})
export class TestTComponent implements OnInit {
  isLinear = true;
  constructor(private _formBuilder: FormBuilder) {}
  ngOnInit(): void {
    this.firstFormGroup.value.firstCtrl=2;
    const   trancheForm = this._formBuilder.group({
      seuil: new FormControl(0, {validators: [Validators.required]}),
    });
    this.s_ep.push(trancheForm);
  }
  firstFormGroup = this._formBuilder.group({
    firstCtrl: [2, Validators.required],
  });
  secondFormGroup = this._formBuilder.group({
    secondCtrl: ['', Validators.required],
    s_ep: this._formBuilder.array([])
  });

  get s_ep() {
    return this.secondFormGroup.controls["s_ep"] as FormArray;
  }


  seuilp(){
    let x = this.firstFormGroup.value.firstCtrl!;
    for (let i = 0; i < x; i++) {
      const   trancheForm = this._formBuilder.group({
        seuil: new FormControl('', {validators: [Validators.required]}),
      });
      this.s_ep.push(trancheForm);
      console.log(this.secondFormGroup.value.s_ep)
      
    }

}
}
