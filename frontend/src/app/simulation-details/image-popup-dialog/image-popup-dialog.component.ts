import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { SafeResourceUrl } from '@angular/platform-browser';

export interface ImagePopupDialogData {
  imageUrl: SafeResourceUrl;
  title?: string;
}

@Component({
  selector: 'app-image-popup-dialog',
  template: `
    <h2 mat-dialog-title *ngIf="data.title">{{ data.title }}</h2>
    <mat-dialog-content class="image-container">
      <div class="zoom-controls">
        <button mat-icon-button (click)="zoomIn()">
          <mat-icon>zoom_in</mat-icon>
        </button>
        <button mat-icon-button (click)="zoomOut()">
          <mat-icon>zoom_out</mat-icon>
        </button>
        <button mat-icon-button (click)="resetZoom()">
          <mat-icon>refresh</mat-icon>
        </button>
      </div>
      <div class="image-wrapper" [style.transform]="'scale(' + zoomLevel + ')'">
        <img [src]="data.imageUrl" alt="Enlarged image" />
      </div>
    </mat-dialog-content>
    <mat-dialog-actions align="end">
      <button mat-button mat-dialog-close>Close</button>
    </mat-dialog-actions>
  `,
  styles: [`
    .image-container {
      position: relative;
      overflow: auto;
      max-height: 80vh;
      max-width: 90vw;
    }
    
    .zoom-controls {
      position: absolute;
      top: 10px;
      right: 10px;
      z-index: 10;
      background-color: rgba(255, 255, 255, 0.7);
      border-radius: 4px;
      padding: 4px;
    }
    
    .image-wrapper {
      transition: transform 0.2s ease-in-out;
      transform-origin: top left;
    }
    
    img {
      max-width: 100%;
      display: block;
    }
  `]
})
export class ImagePopupDialogComponent {
  zoomLevel: number = 1;
  
  constructor(
    public dialogRef: MatDialogRef<ImagePopupDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: ImagePopupDialogData
  ) {}
  
  zoomIn(): void {
    this.zoomLevel += 0.1;
  }
  
  zoomOut(): void {
    if (this.zoomLevel > 0.2) {
      this.zoomLevel -= 0.1;
    }
  }
  
  resetZoom(): void {
    this.zoomLevel = 1;
  }
}