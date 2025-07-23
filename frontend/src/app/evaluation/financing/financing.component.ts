import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-financing',
  templateUrl: './financing.component.html',
  styleUrls: ['./financing.component.css']
})
export class FinancingComponent {
  @Input() panelOpenState: boolean = true;
  @Input() dat: any;


  fred: string[]=['SQ0','TQ0','DQ0','S(Q-Q0)','T(Q-Q0)','D(Q-Q0)','DQ','Access fee','DAI'];

}
