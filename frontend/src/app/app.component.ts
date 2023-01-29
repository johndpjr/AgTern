import {ChangeDetectorRef, Component, OnInit, AfterViewInit, ViewChild} from '@angular/core'
import {Internship, InternshipsService} from "../_generated/api";
import {InternshipClickedEvent} from "./internship-list/internship-list.component";
import {MatSnackBar} from "@angular/material/snack-bar";
import {MatPaginator, MatPaginatorIntl, PageEvent} from "@angular/material/paginator";

enum PaginationContext {
  Search,
  NonSearch,
}

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
  paginationContext: PaginationContext = PaginationContext.NonSearch
  search: string = ""

  constructor(private snackBar: MatSnackBar) {
  }

  ngOnInit() {
    this.updateInternships = this.updateInternships.bind(this)
  }

  ngAfterViewInit() {
    InternshipsService.getInternships(this.paginator.pageIndex * this.paginator.pageSize, this.paginator.pageSize).then(this.updateInternships)
  }

  onInternshipClicked(event: InternshipClickedEvent) {
    this.selectedInternship = event.internship
    window.scroll( { top: 0, left: 0, behavior: "smooth" } )
  }

  doSearch( search: string ) {
    this.search = search
    this.internships = []
    this.loading = true

    if (search === "") {
      this.paginationContext = PaginationContext.NonSearch;
    } else {
      this.paginationContext = PaginationContext.Search;
    }
    let internshipsResp = this.ctxGetInternships(this.paginator.pageIndex * this.paginator.pageSize, this.paginator.pageSize)
    if (this.paginationContext === PaginationContext.Search) {
      internshipsResp.then(internships => {
        // TODO: we have no current way to retrieve the internship count from a search if we want to paginate
        //  since we are limiting our result set (intentionally)
        // this.snackBar.open(
        //   internships.length + (internships.length === 100 ? " or more" : "" ) + " internships found",
        //   undefined,
        //   {
        //     verticalPosition: "bottom",
        //     duration: 2000
        // });
        this.updateInternships(internships);
      });
    } else {
      internshipsResp.then(this.updateInternships);
    }
  }

  ctxGetInternships(skip: number, limit: number) {
    if (this.paginationContext === PaginationContext.Search) {
      return InternshipsService.searchInternships(this.search, skip, limit);
    } else {
      return InternshipsService.getInternships(skip, limit);
    }
  }

  updateInternships( internships: Internship[] ) {
    this.internships = internships
    this.selectedInternship = this.internships[0]
    this.loading = false
  }

  onPageChange(event: PageEvent) {
    this.ctxGetInternships(event.pageIndex * event.pageSize, event.pageSize).then(this.updateInternships);
  }
}
