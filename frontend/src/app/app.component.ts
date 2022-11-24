import {Component, OnInit} from '@angular/core'
import {Internship, InternshipsService} from "../_generated/api";
import {InternshipClickedEvent} from "./internship-list/internship-list.component";
import {MatSnackBar} from "@angular/material/snack-bar";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  internships: Internship[] = []
  selectedInternship!: Internship
  loading: boolean = true
  search: string = ""

  constructor( private snackBar: MatSnackBar ) {
  }

  ngOnInit() {
    this.updateInternships = this.updateInternships.bind(this)
    InternshipsService.getInternships().then(this.updateInternships)
  }

  onInternshipClicked( event: InternshipClickedEvent ) {
    this.selectedInternship = event.internship
    window.scroll( { top: 0, left: 0, behavior: "smooth" } )
  }

  doSearch( search: string ) {
    this.search = search
    this.internships = []
    this.loading = true
    InternshipsService.searchInternships(this.search).then( internships => {
      this.snackBar.open(
        internships.length + ( internships.length === 100 ? " or more" : "" ) + " internships found",
        undefined,
        {
        verticalPosition: "bottom",
        duration: 2000
      } )
      this.updateInternships( internships )
    })
  }

  updateInternships( internships: Internship[] ) {
    this.internships = internships
    this.selectedInternship = this.internships[0]
    this.loading = false
  }
}
