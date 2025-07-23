import { HttpClient } from '@angular/common/http';
import { Component,OnInit } from '@angular/core';
@Component({
  selector: 'app-incitatif',
  templateUrl: './incitatif.component.html',
  styleUrls: ['./incitatif.component.css']
})
export class IncitatifComponent implements OnInit{
  panelOpenState = false;
  dat:any;
  constructor(private http: HttpClient){}
  
  
  
  ngOnInit(): void{
    
    this.http.get('http://localhost:5001/api/getSim/'+localStorage.getItem('userid')).subscribe(data=>{console.log(data); this.dat=data;});
    
  }

}
