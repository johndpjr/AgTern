import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ToolbarModule } from './toolbar/toolbar.module';
import { MainComponent } from './main.component';
import { RouterOutlet } from '@angular/router';
import { MainRoutingModule } from './main-routing.module';

@NgModule({
  declarations: [MainComponent],
  imports: [CommonModule, MainRoutingModule, ToolbarModule, RouterOutlet]
})
export class MainModule {}
