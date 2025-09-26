import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';
import {environment} from 'src/environments/environment';

// Interface for creating a new game round
export interface GameRoundParams {
    alpha: number;
    ratio_tbse: number;
    threshold_res: number;
}

// Interface for the response when creating a new game round
export interface GameRoundResponse {
    round_id: number;
}

// Interface for game round data
export interface GameRound {
    round_id: number;
    alpha: number;
    ratio_tbse: number;
    threshold_res: number;
}

// Interface for participation response
export interface ParticipationResponse {
    score: number;
}

@Injectable({
    providedIn: 'root',
})
export class GameService {
    private apiUrl = environment.apiUrl;

    constructor(private http: HttpClient) {
    }

    /**
     * Creates a new game round
     * @param params The parameters for the new game round
     * @returns Observable with the created game round ID
     */
    createNewRound(params: GameRoundParams): Observable<GameRoundResponse> {
        return this.http.post<GameRoundResponse>(
            `${this.apiUrl}/api/v1/game/round/new`,
            params,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

    /**
     * Gets all game rounds
     * @returns Observable with an array of game rounds
     */
    getAllRounds(): Observable<GameRound[]> {
        return this.http.get<GameRound[]>(
            `${this.apiUrl}/api/v1/game/round/`
        );
    }

    /**
     * Submits participation in a game round
     * @param roundId The ID of the game round
     * @param simulationID The ID of the user
     * @returns Observable with the participation score
     */
    participateInRound(roundId: number, simulationID: number): Observable<ParticipationResponse> {
        return this.http.get<ParticipationResponse>(
            `${this.apiUrl}/api/v1/game/round/${roundId}/participation/${simulationID}`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

    /**
     * Gets participations for a specific game round
     * @param roundId The ID of the game round
     * @returns Observable with an array of participations
     */
    getRoundParticipations(roundId: number): Observable<{ simulation_name: string; score: number }[]> {
        return this.http.get<{ simulation_name: string; score: number }[]>(
            `${this.apiUrl}/api/v1/game/round/${roundId}/participations`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

    /**
     * Gets participations and parameters for a specific game
     * @param simulationId The ID of the game
     * @returns Observable with an array of participations including parameters
     */
    getGameParticipations(simulationId: number): Observable<{
        round_id: number;
        alpha: number;
        ratio_tbse: number;
        threshold_res: number;
        score: number
    }[]> {
        return this.http.get<{ round_id: number; alpha: number; ratio_tbse: number; threshold_res: number; score: number }[]>(
            `${this.apiUrl}/api/v1/game/${simulationId}/participations`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
    }

}
