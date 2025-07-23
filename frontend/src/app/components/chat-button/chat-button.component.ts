import { Component } from '@angular/core';
import { ChatService } from '../../services/chat.service';

@Component({
  selector: 'app-chat-button',
  templateUrl: './chat-button.component.html',
  styleUrls: ['./chat-button.component.css']
})
export class ChatButtonComponent {
  constructor(private chatService: ChatService) {}

  toggleChat(): void {
    this.chatService.toggleChat();
  }
}
