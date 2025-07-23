import { TableData } from './table-data.interface';

/**
 * Interface for components that want to provide data to the chat service.
 * Components implementing this interface can expose their data to be included in chat messages.
 */
export interface ChatDataProvider {

  getComponentDescription() : string;

  /**
   * Returns the component's data in a format that can be included in chat messages.
   * @returns An object containing the component's data and metadata.
   */
  getChatData(): { 
    componentName: string;
    pageName: string;
    data: TableData[];
  };
}
