import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { GameService } from '../game.service';

@Component({
  selector: 'app-game-detail',
  templateUrl: './game-detail.component.html',
  styleUrls: ['./game-detail.component.css']
})
export class GameDetailComponent implements OnInit {
  roundId: number | null = null;
  participants: { simulation_name: string; score: number }[] = [];
  loading: boolean = true;
  error: string | null = null;
  displayedColumns: string[] = ['simulation_name', 'score'];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private gameService: GameService
  ) { }

  ngOnInit(): void {
    // Get the round ID from the route parameter
    this.route.paramMap.subscribe(params => {
      let idParam = params.get('id');
      this.roundId = idParam !== null ? Number(idParam) : null;
      if (this.roundId) {
        this.loadParticipants();
      } else {
        this.error = 'No round ID provided';
        this.loading = false;
      }
    });
  }

  /**
   * Loads participants for the current game round
   */
  loadParticipants(): void {
    if (!this.roundId) return;

    this.loading = true;
    this.gameService.getRoundParticipations(this.roundId).subscribe({
      next: (participants) => {
        this.participants = participants;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error loading participants:', err);
        this.loading = false;
        this.error = 'Failed to load participants. Please try again.';
      }
    });
  }

  /**
   * Navigates back to the previous page
   */
  goBack(): void {
    window.history.back();
  }
}
