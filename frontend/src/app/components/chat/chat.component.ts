import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';
import { ChatService, ChatMessage } from '../../services/chat.service';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit, OnDestroy {
  messages: ChatMessage[] = [];
  newMessage: string = '';
  isOpen: boolean = false;
  isLoading: boolean = false;
  showMoreInfo: boolean = false;
  private destroy$ = new Subject<void>();

  constructor(private chatService: ChatService) {}

  ngOnInit(): void {
    this.chatService.getMessages()
      .pipe(takeUntil(this.destroy$))
      .subscribe(messages => {
        this.messages = messages;
        // Scroll to bottom when new messages arrive
        setTimeout(() => this.scrollToBottom(), 0);
      });

    this.chatService.getChatOpenState()
      .pipe(takeUntil(this.destroy$))
      .subscribe(isOpen => {
        this.isOpen = isOpen;
        if (isOpen) {
          // Scroll to bottom when chat is opened
          setTimeout(() => this.scrollToBottom(), 0);
        }
      });

    this.chatService.getLoadingState()
      .pipe(takeUntil(this.destroy$))
      .subscribe(isLoading => {
        this.isLoading = isLoading;
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  sendMessage(): void {
    if (!this.newMessage.trim()) return;

    this.chatService.sendMessage(this.newMessage);
    this.newMessage = '';
  }

  closeChat(): void {
    this.chatService.closeChat();
  }

  clearMessages(): void {
    this.chatService.clearChat();
  }

  private scrollToBottom(): void {
    const chatContainer = document.querySelector('.chat-messages');
    if (chatContainer) {
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }
  }

  toggleMoreInfo(): void {
    this.showMoreInfo = !this.showMoreInfo;
    // Scroll to bottom after expanding/collapsing to ensure visibility
    setTimeout(() => this.scrollToBottom(), 0);
  }
}
