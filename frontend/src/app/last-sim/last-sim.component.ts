import { HttpClient } from '@angular/common/http';
import { Component,OnInit } from '@angular/core';
import {Chart,} from 'chart.js/auto';
@Component({
  selector: 'app-last-sim',
  templateUrl: './last-sim.component.html',
  styleUrls: ['./last-sim.component.css']
})
export class LastSimComponent implements OnInit{
  dat:any;
  tap:number[]=[];
  tas:number[]=[];
  chart: any = [];
 

  constructor(private http : HttpClient){}
  alert(){
    this.http.post('http://localhost:5001/api/registered/'+this.dat.id, 
    { 
  
      
      userid:localStorage.getItem('userid'),

    }  ).subscribe({next:data=>{console.log(data);alert('enregistrement OK');},
    error:error =>{console.log(error);
      alert('erreur');
    }});
  }
  
  
  ngOnInit(): void {
    this.http.get('http://localhost:5001/api/getSim/'+localStorage.getItem('userid')).subscribe((data)=>{this.dat=data;
    this.tap=this.dat.saisie.user.tabpep.map((coins: any) => coins);
    this.tas=this.dat.saisie.user.tabsep;
    console.log(this.tap,this.tas);
    this.chart = new Chart('MyChart',{
      type: 'line', 

      data: {// values on X-Axis
        labels: this.tas ,
	       datasets: [
          {
            label: "",
            data: [this.dat.saisie.tbse.pi_ep],
            stepped: false,
          },
          {
            label: "",
            data: this.tap,
            backgroundColor: 'blue',
            stepped: true,
          },
          
         

        ]
      },
      options: {
        aspectRatio:3.5
      },
      
    });
  });
    
    
    
    
    



  }

  
  
}
