import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AbordabiliteComponent } from './abordabilite/abordabilite.component';
import { AddsimulationComponent } from './addsimulation/addsimulation.component';
import { ConsomationComponent } from './consomation/consomation.component';
import { EvaluationComponent } from './evaluation/evaluation.component';
import { FactureComponent } from './facture/facture.component';
import { IncitatifComponent } from './incitatif/incitatif.component';
import { LoginComponent } from './login/login.component';
import { AboutComponent } from './pages/about/about.component';
import { AccountComponent } from './pages/account/account.component';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { HomeComponent } from './pages/home/home.component';
import { NotFoundComponent } from './pages/not-found/not-found.component';
import { SignupComponent } from './pages/signup/signup.component';
import { PopulationComponent } from './population/population.component';
import { TarificationComponent } from './tarification/tarification.component';
import { LastSimComponent } from './last-sim/last-sim.component';
import { ListSimulationComponent } from './list-simulation/list-simulation.component';
import { TestTComponent } from './test-t/test-t.component';
import { RegistComponent } from './regist/regist.component';
import { WaitComponent } from './wait/wait.component';
import { GemaComponent } from './gema/gema.component';
import { TableComponent } from './components/table/table.component';
import { DataDisplayComponent } from './data-display/data-display.component';
import { ResultatAffichageComponent } from './resultat-affichage/resultat-affichage.component';
import { ScatterPlotComponent } from './scatter-plot/scatter-plot.component';
import { EtapesProcessusComponent } from './etapes-processus/etapes-processus.component';
import { PenParadeChartComponent } from './pen-parade-chart/pen-parade-chart.component';
import {AbordabiliteGeneralComponent} from "./abordabilite-general/abordabilite-general.component";
import {AffordabilityComponent} from "./evaluation/affordability/affordability.component";
import { SimulationDetailsComponent } from './simulation-details/simulation-details.component';
const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    redirectTo: 'home',
  },
  {
    path: 'EtapesProcessus',
    component: EtapesProcessusComponent,
  },
  {
    path: 'PenParadeChart',
    component: PenParadeChartComponent,
  },
  {
    path: 'scatterPlotComponent',
    component: ScatterPlotComponent,
  },
  {
    path: 'home',
    component: HomeComponent,
  },
  {
    path: 'consommation',
    component: ConsomationComponent,
  },
  {
    path: 'account',
    component: AccountComponent,
  },
  {
    path: 'about',
    component: AboutComponent,
  },
  {
    path: 'signup',
    component: SignupComponent,
  },
  {
    path: 'tarification',
    component: TarificationComponent,
  },
  {
    path: 'dashboard',
    component: DashboardComponent,
  },
  {
    path: 'login',
    component: LoginComponent,
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
    path: 'table',
    component: TableComponent,
  },
  { path: 'data-display', 
    component: DataDisplayComponent },
    {
      path: 'resultats',
      component: ResultatAffichageComponent,
    },
  {
    path: 'affordability',
    component: AffordabilityComponent,
  },
  {
    path: 'population',
    component: PopulationComponent,
  },
  {
    path: 'evaluation',
    component: EvaluationComponent,
  },
  {
  path: 'incitatif',
  component: IncitatifComponent,
  },
  {
    path: 'last',
    component: LastSimComponent,
    },
    {
      path: 'list',
      component: ListSimulationComponent,
      },
      {
        path: 'ttr',
        component: TestTComponent,
        },
        {
          path: 'regist',
          component: RegistComponent,
          },
          {
            path: 'wait',
            component: WaitComponent,
            },
            {
              path: 'gema',
              component: GemaComponent,
              },
            {
              path: 'simulation/:id',
              component: SimulationDetailsComponent,
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
export class AppRoutingModule { }
