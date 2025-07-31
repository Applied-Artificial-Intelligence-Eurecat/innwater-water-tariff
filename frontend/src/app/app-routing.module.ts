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
import {ListSimulationComponent} from './list-simulation/list-simulation.component';
import {TestTComponent} from './test-t/test-t.component';
import {RegistComponent} from './regist/regist.component';
import {WaitComponent} from './wait/wait.component';
import {GemaComponent} from './gema/gema.component';
import {DataDisplayComponent} from './data-display/data-display.component';
import {ResultatAffichageComponent} from './resultat-affichage/resultat-affichage.component';
import {AffordabilityComponent} from "./evaluation/affordability/affordability.component";
import {SimulationDetailsComponent} from './simulation-details/simulation-details.component';
import {AuthGuard} from './auth.guard';

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
        path: 'resultats', // This is in fact Affordability General
        component: ResultatAffichageComponent,
    },
    {
        path: 'affordability',
        component: AffordabilityComponent,
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
        path: 'simulation/:id',
        component: SimulationDetailsComponent,
    },
    {
        path: 'edit-simulation/:id',
        component: AddsimulationComponent,
    },
    {
        path: '**',
        component: NotFoundComponent,
    },
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule {
}
