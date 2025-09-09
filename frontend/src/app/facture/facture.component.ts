import { HttpClient } from '@angular/common/http';
import { Component,OnInit } from '@angular/core';
const dataa=[{K0:30.2205122307,K1:30.2205122307,id:1},
{K0:30.8417998152,K1:30.8417998152,K3:3,id:2},
{K0:33.1063764809,K1:33.1063764809,id:3},
{K0:35.4158586037,K1:35.4158586037,id:4},
{K0:35.4158537,K1:34158586037,id:5}]
@Component({
  selector: 'app-facture',
  templateUrl: './facture.component.html',
  styleUrls: ['./facture.component.css']
})


export class FactureComponent implements OnInit {
  dat:any;
  constructor(private http: HttpClient){}
  
  displayedColumns: string[] = ['K0'];
  dataSour = dataa;
  
  ngOnInit(): void{
    

  }
}
