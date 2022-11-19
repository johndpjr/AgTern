import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-internship-details',
  templateUrl: './internship-details.component.html',
  styleUrls: ['./internship-details.component.scss']
})
export class InternshipDetailsComponent {
    @Input() public name: string = ""
    @Input() public company: string = ""
    @Input() public description: string = ""
}
