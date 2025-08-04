import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';
import {MatExpansionModule} from '@angular/material/expansion';
import {InitialAPIService} from './initial-api.service';
import {AuthService} from './auth.service';
import {AuthGuard} from './auth.guard';
import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatButtonModule} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';
import {MatDividerModule} from '@angular/material/divider';
import {MatRippleModule} from '@angular/material/core';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {MatTabsModule} from '@angular/material/tabs';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import {MatGridListModule} from '@angular/material/grid-list';
import {MatDialogModule} from '@angular/material/dialog';
import {MarkdownModule, MarkedOptions} from 'ngx-markdown';

import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {HomeComponent} from './pages/home/home.component';
import {AboutComponent} from './pages/about/about.component';
import {NotFoundComponent} from './pages/not-found/not-found.component';
import {SignupComponent} from './pages/signup/signup.component';
import {TarificationComponent} from './tarification/tarification.component';
import {LoginComponent} from './login/login.component';
import {CommonModule} from '@angular/common';
import {AccountComponent} from './pages/account/account.component';
import {HttpClientModule} from '@angular/common/http';
import {DashboardComponent} from './pages/dashboard/dashboard.component';
import {ConsomationComponent} from './consomation/consomation.component';
import {FactureComponent} from './facture/facture.component';
import {MatTableModule} from '@angular/material/table';
import {MatCardModule} from '@angular/material/card';
import {AddsimulationComponent} from './addsimulation/addsimulation.component';
import {AbordabiliteComponent} from './abordabilite/abordabilite.component';
import {PopulationComponent} from './population/population.component';
import {EvaluationComponent} from './evaluation/evaluation.component';
import {IncitatifComponent} from './incitatif/incitatif.component';
import {ListSimulationComponent} from './list-simulation/list-simulation.component';
import {LastSimComponent} from './last-sim/last-sim.component';
import {TestTComponent} from './test-t/test-t.component';
import {MatStepperModule} from '@angular/material/stepper';
import {RegistComponent} from './regist/regist.component';
import {WaitComponent} from './wait/wait.component';
import {GemaComponent} from './gema/gema.component';
import {TableComponent} from './components/table/table.component';
import {DataDisplayComponent} from './data-display/data-display.component';
import {ResultatAffichageComponent} from './resultat-affichage/resultat-affichage.component';
import {ScatterPlotComponent} from './scatter-plot/scatter-plot.component';
import {EtapesProcessusComponent} from './etapes-processus/etapes-processus.component';
import {PenParadeChartComponent} from './pen-parade-chart/pen-parade-chart.component';
import {ChatComponent} from './components/chat/chat.component'
import {ChatButtonComponent} from './components/chat-button/chat-button.component';
import {AffordabilityComponent} from './evaluation/affordability/affordability.component';
import {IncentiveComponent} from './evaluation/incentive/incentive.component';
import {EfficiencyComponent} from './evaluation/efficiency/efficiency.component'
import {EquityComponent} from "./evaluation/equity/equity.component";
import {FinancingComponent} from "./evaluation/financing/financing.component";
import {AbordabiliteGeneralComponent} from './abordabilite-general/abordabilite-general.component';
import {SimulationDetailsComponent} from './simulation-details/simulation-details.component';
import {UsageTarificationComponent} from './addsimulation/usage-tarification/usage-tarification.component';
import {SimplifiedDashboardComponent} from './simplified-dashboard/simplified-dashboard.component';
import {FirstRoundAssessmentComponent} from './first-round-assessment/first-round-assessment.component';
import {AggregatedDashboardComponent} from './aggregated-dashboard/aggregated-dashboard.component';
import {AffordabilityTableComponent} from './aggregated-dashboard/affordability-table/affordability-table.component';
import {
    IncentiveEffectTableComponent
} from './aggregated-dashboard/incentive-effect-table/incentive-effect-table.component';
import {
    EconomicEfficiencyTableComponent
} from './aggregated-dashboard/economic-efficiency-table/economic-efficiency-table.component';
import {EquityTableComponent} from './aggregated-dashboard/equity-table/equity-table.component';
import {FundingTableComponent} from './aggregated-dashboard/funding-table/funding-table.component';
import {
    EnvironmentalCostsTableComponent
} from './aggregated-dashboard/environmental-costs-table/environmental-costs-table.component';
import {WaterAgencyTableComponent} from './aggregated-dashboard/water-agency-table/water-agency-table.component';
import {StateTableComponent} from './aggregated-dashboard/state-table/state-table.component';
import {ConfirmDialogComponent} from './components/confirm-dialog/confirm-dialog.component';
import {MatSnackBarModule} from "@angular/material/snack-bar";

@NgModule({
    declarations: [
        AppComponent,
        HomeComponent,
        AboutComponent,
        NotFoundComponent,
        SignupComponent,
        TarificationComponent,
        LoginComponent,
        AccountComponent,
        DashboardComponent,
        ConsomationComponent,
        FactureComponent,
        AddsimulationComponent,
        AbordabiliteComponent,
        PopulationComponent,
        EvaluationComponent,
        IncitatifComponent,
        ListSimulationComponent,
        LastSimComponent,
        TestTComponent,
        RegistComponent,
        WaitComponent,
        GemaComponent,
        TableComponent,
        DataDisplayComponent,
        ResultatAffichageComponent,
        ScatterPlotComponent,
        EtapesProcessusComponent,
        PenParadeChartComponent,
        AffordabilityComponent,
        IncentiveComponent,
        EfficiencyComponent,
        EquityComponent,
        FinancingComponent,
        AbordabiliteGeneralComponent,
        SimulationDetailsComponent,
        ChatComponent,
        ChatButtonComponent,
        UsageTarificationComponent,
        SimplifiedDashboardComponent,
        FirstRoundAssessmentComponent,
        AggregatedDashboardComponent,
        AffordabilityTableComponent,
        IncentiveEffectTableComponent,
        EconomicEfficiencyTableComponent,
        EquityTableComponent,
        FundingTableComponent,
        EnvironmentalCostsTableComponent,
        WaterAgencyTableComponent,
        StateTableComponent,
        ConfirmDialogComponent,
    ],
    imports: [
        CommonModule,
        BrowserModule,
        AppRoutingModule,
        ReactiveFormsModule,
        FormsModule,
        BrowserAnimationsModule,
        MatToolbarModule,
        MatSidenavModule,
        MatButtonModule,
        MatIconModule,
        MatDividerModule,
        MatRippleModule,
        MatFormFieldModule,
        MatInputModule,
        MatProgressSpinnerModule,
        MatGridListModule,
        MatTabsModule,
        HttpClientModule,
        MatTableModule,
        MatCardModule,
        MatExpansionModule,
        MatDialogModule,
        MatSnackBarModule,
        MarkdownModule.forRoot({
            markedOptions: {
                provide: MarkedOptions,
                useValue: {
                    gfm: true,
                    breaks: true,
                    tables: true,
                    smartLists: true,
                    smartypants: true
                }
            }
        }),
        MatStepperModule,
    ],
    providers: [
        InitialAPIService,
        AuthService,
        AuthGuard,
    ],
    bootstrap: [AppComponent]
})
export class AppModule {
}
