import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ToolbarComponent } from './toolbar.component';
import { MaterialModule } from '../../../modules/material/material.module';
import { RouterModule } from '@angular/router';

@NgModule({
  declarations: [ToolbarComponent],
  exports: [ToolbarComponent],
  imports: [CommonModule, MaterialModule, RouterModule]
})
export class ToolbarModule {}
