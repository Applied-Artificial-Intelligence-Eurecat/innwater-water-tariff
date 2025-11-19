import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { FormControl, Validators } from '@angular/forms';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Component({
  selector: 'app-confirm-dialog',
  template: `
    <h2 mat-dialog-title>{{ data.title }}</h2>
    <mat-dialog-content>
      <p *ngIf="!data.isHtml">{{ data.message }}</p>
      <p *ngIf="data.isHtml" [innerHTML]="sanitizedMessage"></p>
      <mat-form-field *ngIf="data.showInput" appearance="fill" style="width: 100%;">
        <mat-label>{{ data.inputLabel || 'Name' }}</mat-label>
        <input matInput [formControl]="inputControl" required>
        <mat-error *ngIf="inputControl.invalid">This field is required</mat-error>
      </mat-form-field>
    </mat-dialog-content>
    <mat-dialog-actions align="end">
      <button mat-button mat-dialog-close *ngIf="data.cancelText">{{ data.cancelText }}</button>
      <button mat-raised-button color="warn" 
              [mat-dialog-close]="data.showInput ? inputControl.value : true"
              [disabled]="data.showInput && inputControl.invalid">
        {{ data.confirmText }}
      </button>
    </mat-dialog-actions>
  `,
  styles: [`
    mat-dialog-actions {
      justify-content: flex-end;
    }
    button {
      margin-left: 8px;
    }
  `]
})
export class ConfirmDialogComponent {
  inputControl = new FormControl('', Validators.required);
  sanitizedMessage: SafeHtml;

  constructor(
    public dialogRef: MatDialogRef<ConfirmDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: {
      title: string;
      message: string;
      confirmText: string;
      cancelText: string;
      showInput?: boolean;
      inputLabel?: string;
      isHtml?: boolean;
    },
    private sanitizer: DomSanitizer
  ) {
    this.sanitizedMessage = this.data.isHtml ? this.sanitizer.bypassSecurityTrustHtml(this.data.message) : '';
  }
}
