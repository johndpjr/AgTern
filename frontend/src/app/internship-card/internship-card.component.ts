import {Component, Input, OnInit} from '@angular/core';
import {Internship} from "../../_generated/api";

@Component({
  selector: 'app-internship-card',
  templateUrl: './internship-card.component.html',
  styleUrls: ['./internship-card.component.scss']
})
export class InternshipCardComponent implements OnInit {
  @Input() internship!: Internship
  tags: string[] = []

  ngOnInit(): void {
    let all_tags = (
      "cloud electrical management sales big-data " +
      "ui web-dev finance robotics research " +
      "ai nlp design c++ python " +
      "database statistics seo devops security " +
      "java c# rust"
    ).split(" ").sort(() => 0.5 - Math.random())
    this.tags = all_tags.slice(0, Math.floor(Math.random() * 8) + 3)
  }
}
