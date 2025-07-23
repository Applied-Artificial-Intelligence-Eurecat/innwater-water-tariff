import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-incentive',
  templateUrl: './incentive.component.html',
  styleUrls: ['./incentive.component.css']
})
export class IncentiveComponent {
    @Input() panelOpenState: boolean = true;
    @Input() dat: any;
}
