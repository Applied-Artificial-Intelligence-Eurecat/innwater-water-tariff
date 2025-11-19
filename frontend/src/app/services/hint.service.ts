import { Injectable } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '../components/confirm-dialog/confirm-dialog.component';

@Injectable({
  providedIn: 'root'
})
export class HintService {
  constructor(private dialog: MatDialog) {}

  /**
   * Shows a hint dialog with the specified title and message
   * @param title The title of the hint dialog
   * @param message The message to display in the hint dialog
   * @param isHtml Whether the message contains HTML content
   */
  showHint(title: string, message: string, isHtml: boolean = false) {
    this.dialog.open(ConfirmDialogComponent, {
      width: '600px',
      data: {
        title: title,
        message: message,
        confirmText: 'Close',
        cancelText: '',
        isHtml: isHtml
      }
    });
  }
}