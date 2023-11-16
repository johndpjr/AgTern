import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MaterialModule } from './shared/modules/material/material.module';
import { MAT_FORM_FIELD_DEFAULT_OPTIONS } from '@angular/material/form-field';
import { LoginComponent } from './pages/login/login.component';
import { SignUpComponent } from './pages/sign-up/sign-up.component';
import { AppRoutingModule } from './app-routing.module';
import { NotFoundComponent } from './pages/not-found/not-found.component';
import { GoogleSignInComponent } from './shared/components/google-sign-in/google-sign-in.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    SignUpComponent,
    NotFoundComponent,
    GoogleSignInComponent
  ],
  imports: [
    BrowserAnimationsModule,
    BrowserModule,
    FormsModule,
    MaterialModule,
    ReactiveFormsModule,
    AppRoutingModule
  ],
  providers: [
    {
      provide: MAT_FORM_FIELD_DEFAULT_OPTIONS,
      useValue: {
        appearance: 'outline'
      }
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}
