import { Component } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../shared/services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  // Reference to itself
  public selfRef: LoginComponent = this;
  constructor(
    public authService: AuthService,
    public router: Router
  ) {}

  incorrectLogin: boolean = false;

  form: FormGroup = new FormGroup({
    username: new FormControl(''),
    password: new FormControl('')
  });

  submit() {
    if (this.form.valid) {
      this.authService
        .login(
          this.form.get('username')?.value,
          this.form.get('password')?.value
        )
        .then(
          () => {
            this.form.reset();
            this.router.navigate(['/jobs']);
          },
          () => {
            this.incorrectLogin = true;
          }
        );
    }
  }
}
