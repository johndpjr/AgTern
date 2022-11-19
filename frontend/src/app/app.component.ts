import {Component, OnInit} from '@angular/core'
import {Internship, InternshipsService} from "../_generated/api";
import {InternshipClickedEvent} from "./internship-list/internship-list.component";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  internships: Internship[] = []
  selectedInternship!: Internship

  async ngOnInit() {
    this.internships = await InternshipsService.getAllInternships()
    this.selectedInternship = this.internships[0]
  }

  onInternshipClicked( event: InternshipClickedEvent ) {
    this.selectedInternship = event.internship
    window.scroll( { top: 0, left: 0, behavior: "smooth" } )
  }
}
