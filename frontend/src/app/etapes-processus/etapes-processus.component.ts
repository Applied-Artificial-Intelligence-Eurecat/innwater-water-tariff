import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-etapes-processus',
  templateUrl: './etapes-processus.component.html',
  styleUrls: ['./etapes-processus.component.css']
})
export class EtapesProcessusComponent implements OnInit {
  etapes: { nom: string, couleur: string }[] = [
    { nom: 'Description Tarif IBT4', couleur: 'red' },
    { nom: 'Couts du Service', couleur: 'red' },
    { nom: 'Social Data', couleur: 'red' },         
    { nom: 'Partie Captive C et Fact', couleur: 'red' },
    { nom: 'Partie Base C et Fact', couleur: 'red' },
    { nom: 'C_PP', couleur: 'red' },
    { nom: 'Facture_IBT_C_PP', couleur: 'red' },
    { nom: 'C_Taylor', couleur: 'red' },
    { nom: 'Facture IBT C Taylor', couleur: 'red' },
    { nom: 'C_EP_BCP', couleur: 'red' },
    { nom: 'Facture_IBT_C_BCP', couleur: 'red' },
    { nom: 'C_et F_TBSE', couleur: 'red' },
    { nom: 'Var_PAR Ménages', couleur: 'red' },
    { nom: 'VAR_CAR-Ménages', couleur: 'red' },
    { nom: 'Tableau Stat Abordabilité', couleur: 'red' },
    { nom: 'Focus_1_CAR', couleur: 'red' },
    { nom: 'Transition_Focus', couleur: 'red' },
    { nom: 'Tableaux-Focus_1', couleur: 'red' },
    { nom: 'Récap_Ménage', couleur: 'red' }
  ];

  constructor(private router: Router) {}

  ngOnInit(): void {
    this.changerCouleurEtapes();
  }

  changerCouleurEtapes(): void {
    let etapesTerminees = 0; // Compteur pour suivre le nombre d'étapes terminées

    this.etapes.forEach((etape, index) => {
      setTimeout(() => {
        etape.couleur = 'green';
        etapesTerminees++;

        // Vérifier si toutes les étapes sont terminées
        if (etapesTerminees === this.etapes.length) {
          this.redirectToDataDisplay(); // Rediriger vers la page des résultats
        }
      }, 10000 * (index + 1)); // 10 secondes * (index + 1) pour chaque étape
    });
  }

  redirectToDataDisplay(): void {
    this.router.navigateByUrl('/resultats');
  }
}