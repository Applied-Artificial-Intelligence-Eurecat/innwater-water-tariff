import {Component, Input, OnInit} from '@angular/core';
import {ActivatedRoute} from "@angular/router";

@Component({
    selector: 'app-aggregated-dashboard',
    templateUrl: './aggregated-dashboard.component.html',
    styleUrls: ['./aggregated-dashboard.component.css']
})
export class AggregatedDashboardComponent implements OnInit {
    @Input() simulationId: number | null = null;

    constructor(private route: ActivatedRoute) {
    }

    ngOnInit(): void {
        console.log('AggregatedDashboard initialized with simulation ID:', this.simulationId);
        this.route.paramMap.subscribe(params => {
            let idParam = params.get('id');
            this.simulationId = idParam !== null ? Number(idParam) : this.simulationId;
        });
    }
}
