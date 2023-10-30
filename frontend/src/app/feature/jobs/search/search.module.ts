import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SearchComponent } from './search.component';
import { MaterialModule } from '../../../modules/material/material.module';
import { ReactiveFormsModule } from '@angular/forms';

@NgModule({
  declarations: [SearchComponent],
  exports: [SearchComponent],
  imports: [CommonModule, MaterialModule, ReactiveFormsModule]
})
export class SearchModule {}
