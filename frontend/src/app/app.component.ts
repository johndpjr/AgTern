import {ChangeDetectorRef, Component, OnInit, AfterViewInit, ViewChild} from '@angular/core'
import {Internship, InternshipsService} from "../_generated/api";
import {InternshipClickedEvent} from "./internship-list/internship-list.component";
import {MatSnackBar} from "@angular/material/snack-bar";
import {MatPaginator, MatPaginatorIntl, PageEvent} from "@angular/material/paginator";
import {MatTableDataSource} from "@angular/material/table";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, AfterViewInit {
  @ViewChild('paginator', { static: false }) paginator: MatPaginator = new MatPaginator(new MatPaginatorIntl(), ChangeDetectorRef.prototype)
  internships: Internship[] = []
  selectedInternship!: Internship
  loading: boolean = true
  search: string = ""

  constructor( private snackBar: MatSnackBar ) {
  }

  ngOnInit() {
    this.updateInternships = this.updateInternships.bind(this)
  }

  ngAfterViewInit() {
    console.log(this.paginator.pageIndex)
    console.log(this.paginator.pageSize)
    InternshipsService.getInternships(this.paginator.pageIndex * this.paginator.pageSize, this.paginator.pageSize).then(this.updateInternships)
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

  pageChange(event: PageEvent) {
    console.log(event);
    InternshipsService.getInternships(event.pageIndex * event.pageSize, event.pageSize).then(this.updateInternships)
  }
}
