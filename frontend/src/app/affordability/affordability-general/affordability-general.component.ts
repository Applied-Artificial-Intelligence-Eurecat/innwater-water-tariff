import {Component, Input, OnInit} from '@angular/core';
import {AffordabilityApiService, AffordabilityGeneralRow} from '../../affordability-api.service';
import {ActivatedRoute} from "@angular/router";

@Component({
    selector: 'app-resultat-affichage',
    templateUrl: './affordability-general.component.html',
    styleUrls: ['./affordability-general.component.css']
})
export class AffordabilityGeneralComponent implements OnInit {
    tableData: AffordabilityGeneralRow[] = [];
    errorMessage = '';
    @Input() simulationId: number | null = null;

    constructor(private affordabilityService: AffordabilityApiService, private route: ActivatedRoute) {
    }

    ngOnInit(): void {
        this.fetchAffordabilityGeneral();
    }

    fetchAffordabilityGeneral(): void {

        this.affordabilityService.getGeneralInfo(this.simulationId!).subscribe({
            next: (data) => {
                this.tableData = data;
            },
            error: (error) => {
                this.errorMessage = 'Une erreur est survenue lors du chargement des données.';
                console.error(error);
            }
        });
    }
}
