import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {AddsimulationComponent} from './addsimulation/addsimulation.component';
import {EvaluationComponent} from './evaluation/evaluation.component';
import {FactureComponent} from './facture/facture.component';
import {AboutComponent} from './pages/about/about.component';
import {AccountComponent} from './pages/account/account.component';
import {DashboardComponent} from './pages/dashboard/dashboard.component';
import {HomeComponent} from './pages/home/home.component';
import {NotFoundComponent} from './pages/not-found/not-found.component';
import {LastSimComponent} from './last-sim/last-sim.component';
import {DataDisplayComponent} from './data-display/data-display.component';
import {SimulationDetailsComponent} from './simulation-details/simulation-details.component';
import {AuthGuard} from './auth.guard';
import {SimplifiedDashboardComponent} from "./simplified-dashboard/simplified-dashboard.component";
import {FirstRoundAssessmentComponent} from "./first-round-assessment/first-round-assessment.component";
import {AggregatedDashboardComponent} from "./aggregated-dashboard/aggregated-dashboard.component";
import {IncentiveEffectComponent} from "./incentive-effect/incentive-effect.component";
import {RoundDetailComponent} from "./round-detail/round-detail.component";
import {GameDetailComponent} from "./game-detail/game-detail.component";
import {AffordabilityDetailsComponent} from "./affordability-details/affordability-details.component";
import {EconomicEfficiencyDetailsComponent} from "./economic-efficiency-details/economic-efficiency-details.component";

const routes: Routes = [
    {
        path: '',
        pathMatch: 'full',
        redirectTo: 'home',
    },
    {
        path: 'home',
        component: HomeComponent,
        canActivate: []
    },
    {
        path: 'account',
        component: AccountComponent,
        canActivate: [AuthGuard]
    },
    {
        path: 'about',
        component: AboutComponent,
    },
    {
        path: 'dashboard',
        component: DashboardComponent,
    },
    {
        path: 'facture',
        component: FactureComponent,
    },
    {
        path: 'addsimulation',
        component: AddsimulationComponent,
    },
    {
        path: 'data-display', // This is in fact Affordability Groups
        component: DataDisplayComponent
    },
    {
        path: 'evaluation',
        component: EvaluationComponent,
    },
    {
        path: 'last',
        component: LastSimComponent,
    },
    {
        path: 'simulation/details/:id',
        component: SimulationDetailsComponent,
    },
    {
        path: 'simulation/dashboard/:id',
        component: AggregatedDashboardComponent,
    },
    {
        path: 'simulation/:id/first-round-assessment',
        component: FirstRoundAssessmentComponent,
    },
    {
        path: 'simulation/simplified-dashboard/:id',
        component: SimplifiedDashboardComponent,
    },
    {
        path: 'edit-simulation/:id',
        component: AddsimulationComponent,
    },
    {
        path: 'incentive-effect/:id',
        component: IncentiveEffectComponent,
    },
    {
        path: 'affordability-details/:id',
        component: AffordabilityDetailsComponent,
    },
    {
        path: 'economic-efficiency-details/:id',
        component: EconomicEfficiencyDetailsComponent,
    },
    {
        path: 'round-detail/:id',
        component: RoundDetailComponent,
    },
    {
        path: 'game-detail/:id',
        component: GameDetailComponent,
    },
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule {
}
