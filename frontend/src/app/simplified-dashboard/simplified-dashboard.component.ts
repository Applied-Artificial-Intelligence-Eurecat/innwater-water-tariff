import {Component, OnInit} from '@angular/core';

@Component({
    selector: 'app-simplified-dashboard',
    templateUrl: './simplified-dashboard.component.html',
    styleUrls: ['./simplified-dashboard.component.css']
})
export class SimplifiedDashboardComponent implements OnInit {

    tbseBarPlotUrl: string | null = null;
    tbseConsumptionUrl: string | null = null;
    pensParadeConsumptionPlotUrl: string | null = null;
    consumptionDeviationLosesCostRecoveryPlotUrl: string | null = null;

    ngOnInit() {

    }


}
