import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-gema',
  templateUrl: './gema.component.html',
  styleUrls: ['./gema.component.css']
})
export class GemaComponent implements OnInit {
  dat:any; 
  constructor(private http : HttpClient){}
  ngOnInit(): void {
    this.http.get('http://api.t2po.re/api/getAllgema').subscribe((data)=>{this.dat=data;});
  }

}
