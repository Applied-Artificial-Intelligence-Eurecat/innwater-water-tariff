import { Component, OnInit } from '@angular/core';

export interface WaterAgencyData {
  category: string;
  totalAnnuel: string;
}

@Component({
  selector: 'app-water-agency-table',
  templateUrl: './water-agency-table.component.html',
  styleUrls: ['./water-agency-table.component.css']
})
export class WaterAgencyTableComponent implements OnInit {
  displayedColumns: string[] = ['category', 'totalAnnuel'];
  dataSource: WaterAgencyData[] = [
    { category: 'Excise duty', totalAnnuel: '957,154 €' }
  ];

  constructor() { }

  ngOnInit(): void {
  }
} 