import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-list-simulation',
  templateUrl: './list-simulation.component.html',
  styleUrls: ['./list-simulation.component.css']
})
export class ListSimulationComponent implements OnInit {
  dat:any; 
  constructor(private http : HttpClient){}
  ngOnInit(): void {
    this.http.get('http://api.t2po.re/api/getAllSim/'+localStorage.getItem('userid')).subscribe((data)=>{this.dat=data;});
  }

}
