/**
 * Interface for standardized table data format to be used in chat messages.
 * This ensures consistent data structure across different components.
 */
export interface TableData {
  /**
   * The name of the table
   */
  tableName: string;

  /**
   * The column names of the table
   */
  columnNames: string[];

  /**
   * The table data as a list of lists (rows)
   * Each inner list represents a row of values
   */
  values: any[][];
}
