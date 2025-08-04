import { Component, OnInit } from '@angular/core';

export interface StateData {
  category: string;
  totalAnnuel: string;
}

@Component({
  selector: 'app-state-table',
  templateUrl: './state-table.component.html',
  styleUrls: ['./state-table.component.css']
})
export class StateTableComponent implements OnInit {
  displayedColumns: string[] = ['category', 'totalAnnuel'];
  dataSource: StateData[] = [
    { category: 'VAT', totalAnnuel: '1,076,968 €' }
  ];

  constructor() { }

  ngOnInit(): void {
  }
} 