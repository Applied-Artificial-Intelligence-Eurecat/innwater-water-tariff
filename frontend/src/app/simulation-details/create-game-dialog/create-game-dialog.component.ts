import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import {GameService, GameRoundParams, GameRound, GameRoundResponse} from '../../game.service';

export interface CreateGameDialogData {
  newGameRound: GameRoundParams;
  simulationId: number | null;
}

@Component({
  selector: 'app-create-game-dialog',
  template: `
      <h2 mat-dialog-title>Create New Game</h2>
      <mat-dialog-content>
          <p>
              To create a <strong>game</strong>, you need to define the scoring rules shared by all simulations joined
              to it.
              The parameters are set to balance consumption accuracy against affordability and how strict we are with
              cost deviations.

          </p>
          <form class="game-form">
              <mat-form-field appearance="fill">
                  <mat-label>Alpha</mat-label>
                  <input matInput type="number" [(ngModel)]="gameParams.alpha" name="alpha" [defaultValue]="0.5" required>
                  <mat-hint>
                      Balance between affordability (low values) and consumption accuracy (high values).
                      Range: 0 to 1.
                  </mat-hint>
              </mat-form-field>

              <mat-form-field appearance="fill">
                  <mat-label>Ratio TBSE</mat-label>
                  <input matInput type="number" [(ngModel)]="gameParams.ratio_tbse" [defaultValue]="0.9" name="ratio_tbse" required>
                  <mat-hint>
                      Target consumption compared to baseline TBSE.
                      Example: 0.9 means a 10% reduction target.
                  </mat-hint>
              </mat-form-field>

              <mat-form-field appearance="fill">
                  <mat-label>Threshold Res</mat-label>
                  <input matInput type="number" [(ngModel)]="gameParams.threshold_res" [defaultValue]="5" name="threshold_res" required>
                  <mat-hint>
                      Maximum allowed deviation in cost performance.
                      If the absolute REX exceeds this threshold, the round is invalid.
                      Example: 5 means ±5%.
                  </mat-hint>
              </mat-form-field>
          </form>

          <div *ngIf="error" class="error-message">
              {{ error }}
          </div>
      </mat-dialog-content>
      <mat-dialog-actions align="end">
          <button mat-button (click)="onCancel()">Cancel</button>
          <button
                  mat-raised-button
                  color="primary"
                  [disabled]="creating || !isFormValid()"
                  (click)="createGame()"
          >
              Create & Link
          </button>
      </mat-dialog-actions>
  `,
  styles: [`
    .game-form {
      display: flex;
      flex-direction: column;
      margin-bottom: 20px;
    }
    
    .error-message {
      color: red;
      margin-top: 10px;
    }
  `]
})
export class CreateGameDialogComponent {
  gameParams: GameRoundParams;
  creating = false;
  error: string | null = null;

  constructor(
    public dialogRef: MatDialogRef<CreateGameDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: CreateGameDialogData,
    private gameService: GameService
  ) {
    // Create a copy of the game params to avoid modifying the original
    this.gameParams = { ...data.newGameRound };
  }

  onCancel(): void {
    this.dialogRef.close(false);
  }

  isFormValid(): boolean {
    return this.gameParams.alpha !== null && 
           this.gameParams.ratio_tbse !== null && 
           this.gameParams.threshold_res !== null;
  }

  createGame(): void {
    if (!this.data.simulationId) {
      this.error = 'Simulation ID is missing';
      return;
    }

    this.creating = true;
    this.error = null;

    // First create the game round
    this.gameService.createNewRound(this.gameParams).subscribe({
      next: (response: GameRoundResponse) => {
        const roundId = response.id;
        
        // Then link the simulation to the new game round
        this.gameService.participateInRound(roundId, this.data.simulationId!).subscribe({
          next: (participationResponse) => {
            this.creating = false;
            this.dialogRef.close(true);
          },
          error: (err) => {
            console.error('Error linking to new game:', err);
            this.creating = false;
            this.error = 'Game created but failed to link. Please try linking manually.';
          }
        });
      },
      error: (err) => {
        console.error('Error creating game:', err);
        this.creating = false;
        this.error = 'Failed to create game. Please try again.';
      }
    });
  }
}