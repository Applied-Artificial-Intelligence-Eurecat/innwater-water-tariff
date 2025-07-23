import { HttpClient } from '@angular/common/http';
import { Component,OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-regist',
  templateUrl: './regist.component.html',
  styleUrls: ['./regist.component.css']
})
export class RegistComponent implements OnInit {
  dat:any;
  constructor(private http: HttpClient,private router: Router){}
  goodbye(){
    this.http.post('http://api.t2po.re/api/gema/'+this.dat.id,{
      id : this.dat.id,
    }).subscribe();

    localStorage.clear();
    this.router.navigateByUrl('/');

  }
  
  
  ngOnInit(): void{
    
    this.http.get('http://api.t2po.re/api/getSimr/'+localStorage.getItem('userid')).subscribe(data=>{console.log(data); this.dat=data;});
    

}
}
