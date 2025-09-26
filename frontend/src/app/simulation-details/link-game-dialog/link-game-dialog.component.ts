import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { GameService, GameRound } from '../../game.service';

export interface LinkGameDialogData {
  gameRounds: GameRound[];
  simulationId: number | null;
}

@Component({
  selector: 'app-link-game-dialog',
  template: `
    <h2 mat-dialog-title>Link to Existing Game</h2>
    <mat-dialog-content>
      <div *ngIf="loading" class="loading-container">
        <mat-spinner diameter="40"></mat-spinner>
        <p>Loading...</p>
      </div>
      
      <div *ngIf="!loading && data.gameRounds.length === 0" class="no-games">
        <p>No game rounds available.</p>
      </div>
      
      <div *ngIf="!loading && data.gameRounds.length > 0" class="games-list">
        <table class="games-table">
          <thead>
            <tr>
              <th>Alpha</th>
              <th>Ratio TBSE</th>
              <th>Threshold Res</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let round of data.gameRounds">
              <td>{{ round.alpha }}</td>
              <td>{{ round.ratio_tbse }}</td>
              <td>{{ round.threshold_res }}</td>
              <td>
                <button 
                  mat-raised-button 
                  color="primary" 
                  [disabled]="linking" 
                  (click)="linkToGame(round)"
                >
                  Link
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div *ngIf="error" class="error-message">
        {{ error }}
      </div>
    </mat-dialog-content>
    <mat-dialog-actions align="end">
      <button mat-button (click)="onCancel()">Cancel</button>
    </mat-dialog-actions>
  `,
  styles: [`
    .loading-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin: 20px 0;
    }
    
    .games-table {
      width: 100%;
      border-collapse: collapse;
    }
    
    .games-table th, .games-table td {
      padding: 8px;
      text-align: left;
      border-bottom: 1px solid #ddd;
    }
    
    .error-message {
      color: red;
      margin-top: 10px;
    }
    
    .no-games {
      margin: 20px 0;
      text-align: center;
    }
  `]
})
export class LinkGameDialogComponent {
  loading = false;
  linking = false;
  error: string | null = null;

  constructor(
    public dialogRef: MatDialogRef<LinkGameDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: LinkGameDialogData,
    private gameService: GameService
  ) {}

  onCancel(): void {
    this.dialogRef.close(false);
  }

  linkToGame(round: GameRound): void {
    if (!this.data.simulationId) {
      this.error = 'Simulation ID is missing';
      return;
    }
    console.log("round", round)
    this.linking = true;
    this.error = null;

    this.gameService.participateInRound(round.round_id, this.data.simulationId).subscribe({
      next: (response) => {
        this.linking = false;
        this.dialogRef.close(true);
      },
      error: (err) => {
        console.error('Error linking to game:', err);
        this.linking = false;
        this.error = 'Failed to link to game. Please try again.';
      }
    });
  }
}