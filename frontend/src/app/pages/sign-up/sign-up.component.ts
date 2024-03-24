import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../shared/services/auth.service';
import { LoginComponent } from '../login/login.component';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.scss']
})
export class SignUpComponent extends LoginComponent {
  isTakenUsername: boolean = false;

  override form: FormGroup = new FormGroup({
    username: new FormControl('', Validators.required),
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [
      Validators.required,
      Validators.minLength(8)
    ])
  });

  override submit() {
    if (this.form.valid) {
      this.authService
        .signUp(
          this.form.get('username')?.value,
          '',
          this.form.get('email')?.value,
          this.form.get('password')?.value
        )
        .then(
          () => {
            this.form.reset();
            this.isTakenUsername = false;
            this.router.navigate(['/jobs']);
          },
          () => {
            this.isTakenUsername = true;
          }
        );
    }
  }
}
