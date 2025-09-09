import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { map } from 'rxjs';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent {
  constructor(private http : HttpClient,private router: Router,private fb:FormBuilder){}

  sigupForm=this.fb.group({
    name : new FormControl('', {validators: [Validators.required]}),
    emailControl :new FormControl('',{validators: [Validators.required, Validators.email]}),
    password : new FormControl('',{validators: [Validators.required]}),
  });
  
  test:any='';

  submit(){
    console.log(this.sigupForm.value.password,this.sigupForm.value.emailControl,this.sigupForm.value.name);
    console.log('1',this.test);
    
    console.log(this.test);
  }
}
