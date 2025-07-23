import { HttpClient } from '@angular/common/http';
import { Component,OnInit } from '@angular/core';
import { AffordabilityParApiService } from '../affordability-par-api.service';


@Component({
  selector: 'app-abordabilite',
  templateUrl: './abordabilite.component.html',
  styleUrls: ['./abordabilite.component.css']
})
export class AbordabiliteComponent implements OnInit {
  panelOpenState = false;
  dat:any;

  fre: string[]=['Headcount ratio','mean','var','std','median','gini'];
  constructor(private http: HttpClient, private apiService: AffordabilityParApiService){
  }



  ngOnInit(): void{

    //this.http.get('http://localhost:5001/api/getSim/'+localStorage.getItem('userid')).subscribe(data=>{console.log(data); this.dat=data;});
    console.log("abordabilite");
    this.apiService.getAffordabilityDeficitEffectif();
  }
}
