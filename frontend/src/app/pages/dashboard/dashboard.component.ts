import { HttpClient } from '@angular/common/http';
import { Component,OnInit } from '@angular/core';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  constructor(private http: HttpClient){}
last:any;
dater! :any;
isLoggedin(){
  let stat=false;
  if(localStorage.getItem('token')!=null){
    stat=true;
  }
  return stat

}
ngOnInit(): void{

this.last=localStorage.getItem('token');

this.http.get('http://localhost:5001/api/getSim/'+localStorage.getItem('userid')).subscribe(data=>{console.log(data);
this.dater=JSON.stringify(data);
});
}
}
