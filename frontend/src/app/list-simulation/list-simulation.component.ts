import { Component, OnInit } from '@angular/core';
import { InitialAPIService, Simulation } from '../initial-api.service';
import {Router} from "@angular/router";

@Component({
  selector: 'app-list-simulation',
  templateUrl: './list-simulation.component.html',
  styleUrls: ['./list-simulation.component.css']
})
export class ListSimulationComponent implements OnInit {
  simulations: Simulation[] = [];
  loading = false;
  error = '';

  constructor(private initialApiService: InitialAPIService,
              private router: Router) {}

  ngOnInit(): void {
    this.loading = true;
    this.initialApiService.getSimulations().subscribe({
      next: (response) => {
        this.simulations = response.data;
        this.loading = false;
      },
      error: (err) => {
        if (err.status === 401) {
          this.initialApiService.logout();

          return;
        }
        this.error = 'Failed to load simulations. Please try again later.';
        this.loading = false;
        console.error('Error loading simulations:', err);
      }
    });
  }
}
