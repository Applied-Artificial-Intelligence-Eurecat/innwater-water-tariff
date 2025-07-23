import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-efficiency',
  templateUrl: './efficiency.component.html',
  styleUrls: ['./efficiency.component.css']
})
export class EfficiencyComponent {
    @Input() panelOpenState: boolean = true;
    @Input() dat: any;
}
