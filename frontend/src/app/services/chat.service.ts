import {Injectable} from '@angular/core';
import {BehaviorSubject, Observable} from 'rxjs';
import {HttpClient} from '@angular/common/http';
import {catchError, finalize} from 'rxjs/operators';
import {ChatDataProvider} from '../interfaces/chat-data-provider.interface';
import {TableData} from '../interfaces/table-data.interface';

export interface ChatMessage {
    id: number;
    text: string;
    sender: 'user' | 'system';
    timestamp: Date;
}

@Injectable({
    providedIn: 'root'
})
export class ChatService {
    private messages = new BehaviorSubject<ChatMessage[]>([]);
    private isOpen = new BehaviorSubject<boolean>(false);
    private isLoading = new BehaviorSubject<boolean>(false);
    private activeComponents = new Map<string, ChatDataProvider>();

    constructor(
        private http: HttpClient
    ) {
        // Initialize with a welcome message
        this.addMessage({
            text: 'Welcome to the chat! How can I help you with the Water Tariff Dashboard?',
            sender: 'system'
        });
    }

    /**
     * Registers a component as an active component that can provide data to the chat.
     * @param componentId A unique identifier for the component
     * @param component The component instance that implements ChatDataProvider
     */
    registerComponent(componentId: string, component: ChatDataProvider): void {
        this.activeComponents.set(componentId, component);
    }

    /**
     * Unregisters a component from the active components list.
     * @param componentId The unique identifier of the component to unregister
     */
    unregisterComponent(componentId: string): void {
        this.activeComponents.delete(componentId);
    }

    /**
     * Gets the data from all active components.
     * @returns An array of component data objects
     */
    getActiveComponentsData(): Array<{
        componentName: string;
        description: string,
        pageName: string;
        data: TableData[]
    }> {
        const componentsData: Array<{
            componentName: string;
            description: string;
            pageName: string;
            data: TableData[]
        }> = [];

        this.activeComponents.forEach((component) => {
            try {
                const data = component.getChatData();
                const description = component.getComponentDescription();
                if (data) {
                    // Add the component data to the array
                    componentsData.push({
                        description: description,
                        ...data
                    });
                }
            } catch (error) {
                console.error('Error getting data from component:', error);
            }
        });

        return componentsData;
    }

    getMessages(): Observable<ChatMessage[]> {
        return this.messages.asObservable();
    }

    getLoadingState(): Observable<boolean> {
        return this.isLoading.asObservable();
    }

    getChatOpenState(): Observable<boolean> {
        return this.isOpen.asObservable();
    }

    toggleChat(): void {
        this.isOpen.next(!this.isOpen.value);
    }

    openChat(): void {
        this.isOpen.next(true);
    }

    closeChat(): void {
        this.isOpen.next(false);
    }

    addMessage(message: Omit<ChatMessage, 'id' | 'timestamp'>): void {
        const currentMessages = this.messages.value;
        const newMessage: ChatMessage = {
            id: currentMessages.length > 0 ? Math.max(...currentMessages.map(m => m.id)) + 1 : 1,
            text: message.text,
            sender: message.sender,
            timestamp: new Date()
        };

        this.messages.next([...currentMessages, newMessage]);
    }

    sendMessage(text: string): void {
        if (!text.trim()) return;

        // Add user message
        this.addMessage({
            text,
            sender: 'user'
        });

        // Prepare current messages for API
        let messagesForApi = (this.messages.value.map(msg => ({
            role: msg.sender === 'user' ? 'user' : 'assistant',
            content: msg.text
        })));

        // Get data from active components
        const componentsData = this.getActiveComponentsData();

        // Create sections object with component data
        const sections: { [key: string]: any } = {};
        componentsData.forEach(componentData => {
            if (componentData.pageName) {
                sections[componentData.pageName] = componentData;
            }
        });
        console.log(sections);

        // Show loading indicator
        this.isLoading.next(true);

        // Call the external API similar to your Python code
        this.http.post('https://innwater.eurecatprojects.com/assistant/api/water_tariff/ask', {
            messages: messagesForApi,
            components: sections
        }, {responseType: 'text'}).pipe(
            catchError(error => {
                // Handle errors
                this.addMessage({
                    text: 'Sorry, there was an error processing your request. Please try again later.',
                    sender: 'system'
                });
                throw error;
            }),
            finalize(() => {
                this.isLoading.next(false);
            })
        ).subscribe(response => {
            // Add API response to chat
            this.addMessage({
                text: response,
                sender: 'system'
            });
        });
    }

    clearChat(): void {
        this.messages.next([]);
        // Add welcome message again
        this.addMessage({
            text: 'Welcome to the chat! How can I help you with the water governance assessment?',
            sender: 'system'
        });
    }
}
