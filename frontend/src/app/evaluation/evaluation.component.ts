import { HttpClient } from '@angular/common/http';
import { Component,OnInit } from '@angular/core';

@Component({
  selector: 'app-evaluation',
  templateUrl: './evaluation.component.html',
  styleUrls: ['./evaluation.component.css']
})
export class EvaluationComponent implements OnInit {
  panelOpenState = false;
  dat:any;
  constructor(private http: HttpClient){
  }



  ngOnInit(): void{

  }

}
