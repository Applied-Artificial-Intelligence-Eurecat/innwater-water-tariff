import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {environment} from 'src/environments/environment';
import {Router} from "@angular/router";

export interface UserResponse {
    id: number;
    email: string;
    message: string;
}

export interface TokenResponse {
    access_token: string;
    token_type: string;
}

export interface Simulation {
    id: number;
    name: string;
    status: string;
    number_of_periods: number;
    project_id: number;
}

export interface SimulationsResponse {
    status: string;
    message: string;
    data: Simulation[];
}

export interface SimulationPayload {
    demand: {
        coefficients: {
            a0: number;
            a1: number;
            a2: number;
            a3: number;
            a4: number;
            a5: number;
            a6: number;
        };
        has_garden: boolean;
        has_pool: boolean;
        k: number;
    };
    launch: {
        periods: number;
        simulation_name: string;
    };
    population: {
        bd: string;
        eps: number;
        std: number;
    };
    primitives: {
        drinking_water: {
            fixed_costs: number;
            number_of_subscribers: number;
            variable_costs: number;
        };
        environment: {
            average_variable_cost: number;
            fixed_costs_per_year: number;
        };
        sanitation: {
            fixed_costs: number;
            number_of_subscribers: number;
            variable_costs: number;
        };
        social_data: {
            extreme_poverty: number;
            poverty: number;
            threshold_car: number;
            threshold_par: number;
        };
        taxation: {
            drinking_water: {
                fees: number;
                vat: number;
            };
            sanitation: {
                fees: number;
                vat: number;
            }
        }
    };
    tariff: {
        drinking_water: {
            subscription: number;
            usage_tiers: {
                price: number;
                threshold: number;
            }[];
        };
        sanitation: {
            subscription: number;
            usage_tiers: {
                price: number;
                threshold: number;
            }[];
        }
    }
}

export interface SimulationResponse {
    status: string;
    message: string;
    data: {
        simulation_id: number;
        name: string;
        status: string;
        project_id: number;
    }
}

export interface SimulationDetailResponse {
    status: string;
    message: string;
    data: {
        id: number;
        demand: {
            coefficients: {
                a0: number;
                a1: number;
                a2: number;
                a3: number;
                a4: number;
                a5: number;
                a6: number;
            };
            k: number;
            piscine: boolean;
            jardin: boolean;
        };
        launch: {
            periods: number;
            simulation_name: string;
        };
        population: {
            bd: string;
            eps: number;
            std: number;
        };
        primitives: {
            ep: {
                couts_fixes: number;
                couts_variables: number;
                nombre_abonnes: number;
            };
            assainissement: {
                couts_fixes: number;
                couts_variables: number;
                nombre_abonnes: number;
            };
            environnement: {
                couts_fixes_par_an: number;
                couts_variable_moyen: number;
            };
            fiscalite: {
                eau_potable: {
                    tva: number;
                    redevances: number;
                };
                assainissement: {
                    tva: number;
                    redevances: number;
                };
            };
            donnees_sociales: {
                seuil_par: number;
                seuil_car: number;
                pauvrete: number;
                grande_pauvrete: number;
            };
        };
        status: string;
        tariff: {
            ep: {
                abonnement: number;
                usage_tiers: {
                    seuil: number;
                    prix: number;
                }[];
            };
            assainissement: {
                abonnement: number;
                usage_tiers: {
                    seuil: number;
                    prix: number;
                }[];
            };
        };
    };
}

@Injectable({
    providedIn: 'root',
})
export class InitialAPIService {
    private apiUrl = environment.apiUrl;

    constructor(private http: HttpClient,
                private router: Router,
    ) {
    }

    /**
     * Creates a new user
     * @param email User email
     * @param password User password
     * @returns Observable with user creation response
     */
    createUser(email: string, password: string): Observable<UserResponse> {
        return this.http.post<UserResponse>(`${this.apiUrl}/api/v1/initial/user`, {
            email,
            password
        });
    }

    /**
     * Authenticates a user and gets JWT token
     * @param email User email
     * @param password User password
     * @returns Observable with token response
     */
    login(email: string, password: string): Observable<TokenResponse> {
        const formData = new FormData();
        formData.append('grant_type', 'password');
        formData.append('username', email);
        formData.append('password', password);
        formData.append('scope', '');
        formData.append('client_id', 'string');
        formData.append('client_secret', '********');

        return this.http.post<TokenResponse>(
            `${this.apiUrl}/api/v1/initial/token`,
            formData
        );
    }

    logout() {
        localStorage.clear();
        this.router.navigateByUrl('/account');

    }

    /**
     * Gets the list of simulations for the current user
     * @returns Observable with simulations response
     */
    getSimulations(): Observable<SimulationsResponse> {
        return this.http.get<SimulationsResponse>(
            `${this.apiUrl}/api/v1/initial/simulations`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

    /**
     * Creates a new simulation
     * @param payload The simulation data
     * @returns Observable with simulation creation response
     */
    createSimulation(payload: SimulationPayload): Observable<SimulationResponse> {
        return this.http.post<SimulationResponse>(
            `${this.apiUrl}/api/v1/initial/simulation/new`,
            payload,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

    /**
     * Gets a specific simulation by ID
     * @param id The simulation ID
     * @returns Observable with simulation detail response
     */
    getSimulationById(id: number): Observable<SimulationDetailResponse> {
        return this.http.get<SimulationDetailResponse>(
            `${this.apiUrl}/api/v1/initial/simulation/${id}`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

    /**
     * Updates an existing simulation
     * @param id The simulation ID
     * @param payload The updated simulation data
     * @returns Observable with simulation update response
     */
    updateSimulation(id: number, payload: SimulationPayload): Observable<SimulationResponse> {
        return this.http.put<SimulationResponse>(
            `${this.apiUrl}/api/v1/initial/simulation/${id}/edit`,
            payload,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

    getPlot(url: string) {
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Accept': 'image/png',
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        });
        return this.http.get(url, {
            headers: headers,
            responseType: 'blob'
        });
    }}
