import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-simulation-details',
  templateUrl: './simulation-details.component.html',
  styleUrls: ['./simulation-details.component.css']
})
export class SimulationDetailsComponent implements OnInit {
  simulationId: string | null = null;
  simulationData: any = null;
  loading: boolean = true;
  error: string | null = null;

  constructor(
    private http: HttpClient,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    // Get the simulation ID from the route parameter
    this.route.paramMap.subscribe(params => {
      this.simulationId = params.get('id');
      if (this.simulationId) {
        this.loadSimulationData();
      } else {
        this.error = 'No simulation ID provided';
        this.loading = false;
      }
    });
  }

  loadSimulationData(): void {
    this.loading = true;
    this.error = null;
    
    // Fetch the simulation data from the API
    this.http.get(`http://localhost:5001/api/getSim/${this.simulationId}`)
      .subscribe({
        next: (data: any) => {
          this.simulationData = data;
          this.loading = false;
        },
        error: (err) => {
          console.error('Error fetching simulation data:', err);
          this.error = 'Failed to load simulation data. Please try again later.';
          this.loading = false;
        }
      });
  }
}