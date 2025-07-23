import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-equity',
  templateUrl: './equity.component.html',
  styleUrls: ['./equity.component.css']
})
export class EquityComponent {
  @Input() panelOpenState: boolean = true;
  @Input() dat: any;
  frede: string[]=['-','Extreme Poor','Poor','Non Poor','Poor/ Non Poor','Extreme Poor/ Non Poor'];



}
