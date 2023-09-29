import {AfterViewInit, ChangeDetectorRef, Component, OnInit, ViewChild} from '@angular/core';
import {MatPaginator, MatPaginatorIntl, PageEvent} from "@angular/material/paginator";
import {Job, JobsService} from "../../../_generated/api";
import {MatSnackBar} from "@angular/material/snack-bar";
import {JobClickedEvent} from "../../job-list/job-list.component";

enum PaginationContext {
  Search,
  NonSearch,
}

@Component({
  selector: 'app-jobs',
  templateUrl: './jobs.component.html',
  styleUrls: ['./jobs.component.scss']
})
export class JobsComponent implements OnInit, AfterViewInit {
  @ViewChild('paginator', { static: false }) paginator: MatPaginator = new MatPaginator(new MatPaginatorIntl(), ChangeDetectorRef.prototype)
  jobs: Job[] = []
  selectedJob!: Job
  loading: boolean = true
  paginationContext: PaginationContext = PaginationContext.NonSearch
  search: string = ""

  constructor(private snackBar: MatSnackBar) {
  }

  ngOnInit() {
    this.updateJobs = this.updateJobs.bind(this)
  }

  ngAfterViewInit() {
    JobsService.getJobs(this.paginator.pageIndex * this.paginator.pageSize, this.paginator.pageSize).then(this.updateJobs)
  }

  onJobClicked(event: JobClickedEvent) {
    this.selectedJob = event.job
    window.scroll( { top: 0, left: 0, behavior: "smooth" } )
  }

  doSearch( search: string ) {
    this.search = search
    this.jobs = []
    this.loading = true

    if (search === "") {
      this.paginationContext = PaginationContext.NonSearch;
    } else {
      this.paginationContext = PaginationContext.Search;
    }
    const jobsResp = this.ctxGetJobs(this.paginator.pageIndex * this.paginator.pageSize, this.paginator.pageSize)
    if (this.paginationContext === PaginationContext.Search) {
      jobsResp.then(jobs => {
        // TODO: we have no current way to retrieve the job count from a search if we want to paginate
        //  since we are limiting our result set (intentionally)
        // this.snackBar.open(
        //   jobs.length + (jobs.length === 100 ? " or more" : "" ) + " jobs found",
        //   undefined,
        //   {
        //     verticalPosition: "bottom",
        //     duration: 2000
        // });
        this.updateJobs(jobs);
      });
    } else {
      jobsResp.then(this.updateJobs);
    }
  }

  ctxGetJobs(skip: number, limit: number) {
    if (this.paginationContext === PaginationContext.Search) {
      return JobsService.searchJobs(this.search, skip, limit);
    } else {
      return JobsService.getJobs(skip, limit);
    }
  }

  updateJobs(jobs: Job[] ) {
    this.jobs = jobs
    this.selectedJob = this.jobs[0]
    this.loading = false
  }

  onPageChange(event: PageEvent) {
    this.ctxGetJobs(event.pageIndex * event.pageSize, event.pageSize).then(this.updateJobs);
  }
}
