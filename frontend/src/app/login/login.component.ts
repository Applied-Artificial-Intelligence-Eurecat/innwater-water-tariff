import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  constructor(private http : HttpClient,private router: Router,private fb:FormBuilder){}

  loginForm=this.fb.group({
    emailControl :new FormControl('',{validators: [Validators.required, Validators.email]}),
    password : new FormControl('',{validators: [Validators.required]}),
  });
  
  test:any;

  submit(){
    
    //console.log(this.loginForm.value.password,this.emailControl.value);
    this.http.post('http://localhost:5001/api/login',{
      email : this.loginForm.value.emailControl,
      password : this.loginForm.value.password,
    }).subscribe({next:data => {
    this.test=data;
    localStorage.setItem('token',this.test.token);
    localStorage.setItem('userid',this.test.userid);
    console.log(localStorage.getItem('userid'));
    this.router.navigateByUrl('/dashboard');
    if (JSON.stringify(data)!=null){console.log("User is logged in");}
    
  },
  error:error =>{console.log(error);
    alert('identifiant pas reconnu');
    this.router.navigateByUrl('/dashboard');
  }
});
  }
}
