import { Component } from '@angular/core';

@Component({
  selector: 'app-data-display',
  templateUrl: './data-display.component.html',
  styleUrls: ['./data-display.component.css']
})
export class DataDisplayComponent {

// Gini
tablesGini = [
  {
    title: "Gini PAR IBT",
    data: [
      { label: "Between", value: "0" },
      { label: "Within", value: "0" },
      { label: "Transvariation", value: "0" },
      { label: "Ensemble", value: "0" }
    ]
  },
  {
    title: "Gini PAR TBSE",
    data: [
      { label: "Between", value: "0" },
      { label: "Within", value: "0" },
      { label: "Transvariation", value: "0" },
      { label: "Ensemble", value: "0" }
    ]
  },
  {
    title: "Gini CAR IBT",
    data: [
      { label: "Between", value: "37.0" },
      { label: "Within", value: "35.6" },
      { label: "Transvariation", value: "10.1" },
      { label: "Ensemble", value: "82.7" }
    ]
  },
  {
    title: "Gini CAR TBSE",
    data: [
      { label: "Between", value: "0" },
      { label: "Within", value: "0" },
      { label: "Transvariation", value: "0" },
      { label: "Ensemble", value: "0" }
    ]
  }
];
  // Problémes 
  tables = [
    {
      title: 'Effectifs "Problèmes" au sens du CAR pour l\'IBT',
      data: [
        { label: 'EP (Non assaini)', value: '3' },
        { label: 'EPA (Assaini)', value: '33' },
        { label: 'Ensemble', value: '36' }
      ]
    },
    {
      title: 'Effectifs "Problèmes" au sens du PAR pour la TBSE',
      data: [
        { label: 'EP (Non assaini)', value: '45' },
        { label: 'EPA (Assaini)', value: '105' },
        { label: 'Ensemble', value: '150' }
      ]
    },
    {
      title: 'Effectifs "Problèmes" au sens du CAR pour l\'IBT',
      data: [
        { label: 'EP (Non assaini)', value: '41' },
        { label: 'EPA (Assaini)', value: '91' },
        { label: 'Ensemble', value: '132' }
      ]
    },
    {
      title: 'Effectifs "Problèmes" au sens du CAR pour la TBSE',
      data: [
        { label: 'EP (Non assaini)', value: '87' },
        { label: 'EPA (Assaini)', value: '134' },
        { label: 'Ensemble', value: '221' }
      ]
    }
  ];

  data = {
    nb_menages: {
      nonAssaini: 248,
      assaini: 210,
      total: 458
    },

    moyenne: {
      parIBT: { g1: 0.6, g2: 1.7 },
      parTBSE: { g1: 2, g2: 4.6 },
      deltaPAR: { g1: -1.3, g2: -2.9 },
      carIBT: { g1: 1.8, g2: 3.3 },
      carTBSE: { g1: 2.8, g2: 5.59 },
      deltaCAR: { g1: -0.5, g2: -1.2 }
    },
    mediane: {
      parIBT: { g1: 0.4, g2: 1.2 },
      parTBSE: { g1: 1.2, g2: 3 },
      deltaPAR: { g1: null, g2: null },
      carIBT: { g1: 1.4, g2: 2.6 },
      carTBSE: { g1: 1.9, g2: 3.82 },
      deltaCAR: { g1: -0.5, g2: -1.2 }
    },

    min: {
      parIBT: { g1: 0, g2: 0.1 },
      parTBSE: { g1: 0.1, g2: 0.2 },
      deltaPAR: { g1: null, g2: null }, // Valeurs vides
      carIBT: { g1: 0.3, g2: 0.3 },
      carTBSE: { g1: 0.3, g2: 0.3 },
      deltaCAR: { g1: null, g2: null } // Valeurs vides
    },
    // Ajoutez les autres données de la même manière...

    max: {
      parIBT: { g1: 3.8, g2: 10.9 },
      parTBSE: { g1: 9.9, g2: 21.9 },
      deltaPAR: { g1: null, g2: null }, // Valeurs vides
      carIBT: { g1: 8.6, g2: 12.6 },
      carTBSE: { g1: 12.8, g2: 23.6 },
      deltaCAR: { g1: null, g2: null } // Valeurs vides
    },
    q1: {
      parIBT: { g1: 0.7, g2: 0.6},
      parTBSE: { g1: 0.6, g2: 1.7 },
      deltaPAR: { g1: null, g2: null }, // Valeurs vides
      carIBT: { g1: 0.7, g2: 1.5 },
      carTBSE: { g1: 1.0, g2: 2.4 },
      deltaCAR: { g1: null, g2: null } // Valeurs vides
    },

    q3: {
      parIBT: { g1: 0.8, g2: 2.3 },
      parTBSE: { g1: 2.3, g2: 6.3 },
      deltaPAR: { g1: null, g2: null }, // Valeurs vides
      carIBT: { g1: 2.5, g2: 4.5 },
      carTBSE: { g1: 3.5, g2: 7.6 },
      deltaCAR: { g1: null, g2: null } // Valeurs vides
    },
    			

    D1: {
      parIBT: { g1: 0.1, g2: 4.2},
      parTBSE: { g1: 0.4, g2: 9.9 },
      deltaPAR: { g1: null, g2: null }, // Valeurs vides
      carIBT: { g1: 0.5, g2: 1.5 },
      carTBSE: { g1: 0.7, g2: 1.3 },
      deltaCAR: { g1: null, g2: null } // Valeurs vides
    }, 

    D9: {
      parIBT: { g1: 1.5, g2: 4.2 },
      parTBSE: { g1: 4.7, g2: 10.8 },
      deltaPAR: { g1: null, g2: null }, // Valeurs vides
      carIBT: { g1: 3.9, g2: 6.3 },
      carTBSE: { g1: 6.3, g2: 12.3 },
      deltaCAR: { g1: null, g2: null } // Valeurs vides
    }, 

    F: {
      parIBT: { g1: 65.5, g2: 65.4},
      parTBSE: { g1: 65.9, g2: 67.7 },
      deltaPAR: { g1: null, g2: null }, // Valeurs vides
      carIBT: { g1: 62.0, g2: 61.0 },
      carTBSE: { g1: 48.3, g2: 65.0 },
      deltaCAR: { g1: null, g2: null } // Valeurs vides
    },
    	


    Variance: {
      parIBT: { g1: 0.47, g2: 2.92 },
      parTBSE: { g1: 4.16, g2: 18.86 },
      deltaPAR: { g1: null, g2: null }, // Valeurs vides
      carIBT: { g1: 2.18, g2: 5.52 },
      carTBSE: { g1: 6.43, g2: 22.50 },
      deltaCAR: { g1: null, g2: null } // Valeurs vides
    }, 

    EcartType: {
      parIBT: { g1: 0.7, g2: 1.7 },
      parTBSE: { g1: 2, g2: 4.3 },
      deltaPAR: { g1: null, g2: null }, // Valeurs vides
      carIBT: { g1: 1.48, g2: 2.35 },
      carTBSE: { g1: 2.54, g2: 4.7 },
      deltaCAR: { g1: null, g2: null } // Valeurs vides
    }, 


      EP: {
        fi: 54.15,
        parIBT: { menages: 1.2, individus: 1.78, enfants: 1.81 },
        parTBSE: { menages: 18.14, individus: 18.95, enfants: 20.90 },
        deltaPAR: { menages: -18.55, individus: -16.41, enfants: -16.82 },
        carIBT: { menages: 16.53, individus: 21.25, enfants: 24.09 },
        carTBSE: { menages: 35.08, individus: 37.66, enfants: 40.91 },
        deltaCAR: { menages: -18.55, individus: -16.41, enfants: -16.82 }
      },
      EPA: {
        fi: 45.85,
        parIBT: { menages: 15.7, individus: 15.3, enfants: 19.7 },
        parTBSE: { menages: 50, individus: 46.61, enfants: 51.29},
        deltaPAR: { menages: -20.48, individus: -16.24, enfants: -11.40 },
        carIBT: { menages: 43.33, individus: 46.02, enfants: 53.89 },
        carTBSE: { menages: 63.81, individus: 62.26, enfants: 65.28 },
        deltaCAR: { menages: -20.48, individus: -16.24, enfants: -11.40 }
      },
      Ensemble: {
        fi: 100,
        parIBT: { menages: 7.8, individus: 7.8, enfants: 9.92 },
        parTBSE: { menages: 32.75, individus: 31.63, enfants: 35.10 },
        deltaPAR: { menages: -19.43, individus: -16.33, enfants: -14.29 },
        carIBT: { menages: 28.82, individus: 32.60, enfants: 38.01 },
        carTBSE: { menages: 48.25, individus: 48.93, enfants: 52.30 },
        deltaCAR: { menages: -19.43, individus: -16.33, enfants: -14.29 }
      },
    
      

      

      
      
      
      
      

      
      
      
      

      

      
     
      
      

      
        EPBIntensite: {
          fi: 54.1,
          parIBT: { Moyenne: 0.06, Variance: 0.3437, Var_Inter: 2.0827  },
          parTBSE: { Moyenne: 4.50, Variance: 49.85, Var_Inter : 397.8474},
          deltaPAR: { delta_value: 43.33},
          fiCAR: 54.1,
          carIBT: { Moyenne: 3.02, Variance: 73.6276, Var_Inter: 49.7392  },
          carTBSE: { Moyenne: 10.68, Variance: 354.1678, Var_Inter : 397.8474 },
          deltaCAR: { delta_value: -7.66 }
        },
        EPAIntensite: {
          fi: 45.9,
          parIBT: { Moyenne: 2.96, Variance: 79.0985, Var_Intra: 36.4540          },
          parTBSE: { Moyenne:  32.77, Variance: 46.02, Var_Intra: 1320.8852  },
          deltaPAR: { delta_value: 43.33 },
          fiCAR: 45.9,
          carIBT: { Moyenne: 17.17, Variance: 654.3584,  Var_Intra: 339.9016 },
          carTBSE: { Moyenne: 50.71, Variance: 2462.5325 , Var_Intra : 1320.8852},
          deltaCAR: { delta_value: -33.53}
        },
        EPBIntensiteEnseble: {
          fi: 100.0,
          parIBT: { Moyenne: 1.39012380, Variance: 38.5366, Rap_Corr: 5.4  },
          parTBSE: { Moyenne: 17.4652600, Variance: 49.85, Rap_Corr :  23.1 },
          deltaPAR: { delta_value: 43.33},
          fiCAR: 100.0,
          carIBT: { Moyenne: 9.51048273, Variance: 389.6407, Rap_Corr: 12.8  },
          carTBSE: { Moyenne: 29.0336012, Variance: 1718.7326, Rap_Corr : 23.1 },
          deltaCAR: { delta_value: -19.52 }
        },
        
        




        



        
        
        




        
        



        
        



        
        
        
        
//

        EPIntensiteEffectif: {
          fi: 8.3,
          parIBT: { Moyenne: 18.27, Variance: 166.7086, Var_Inter: 441.6151},
          parTBSE: { Moyenne: 43.33, Variance: 46.02, Var_Inter: 49.7392   },
          deltaPAR: { delta_value: 43.33 },
          fiCAR: 39.4,
          carIBT: { Moyenne: 18.27, Variance:  166.7086,  Var_Inter: 97.7200 },
          carTBSE: { Moyenne: 30.44, Variance:  407.9785 , Var_Inter : 573.7630},
          deltaCAR: { delta_value: -12.17}
        },
        EPAIntensiteEffectif: {
          fi: 91.7,
          parIBT: { Moyenne: 39.63, Variance: 619.9151, Var_Intra: 582.1478 },
          parTBSE: { Moyenne: 43.33, Variance: 46.02, Var_Intra: 339.9016  },
          deltaPAR: { delta_value: 43.33 },
          fiCAR: 60.6,
          carIBT: { Moyenne: 39.63, Variance:     619.9151,  Var_Intra: 479.1464 },
          carTBSE: { Moyenne: 79.47, Variance: 1573.5957 , Var_Intra : 1114.7329},
          deltaCAR: { delta_value: -39.84}
        },
        EnsembleIntensiteEffectif: {
          fi: 100.0,
          parIBT: { Moyenne: 17.68546393, Variance: 202.0810, Rap_Corr: 218.5},
          parTBSE: { Moyenne: 43.33, Variance: 46.02, Rap_Corr: 12.8   },
          deltaPAR: { delta_value: 43.33 },
          fiCAR: 100.0,
          carIBT: { Moyenne: 32.99849310, Variance: 576.8663,  Rap_Corr: 16.9 },
          carTBSE: { Moyenne: 60.1691825, Variance:  1688.4959 , Rap_Corr : 34.0},
          deltaCAR: { delta_value: -27.2}
        },
       // 		
       
       
       


       
       
       
       
       
       

       
       
       
       
 
        
  };
}