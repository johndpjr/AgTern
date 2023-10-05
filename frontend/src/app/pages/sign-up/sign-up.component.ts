import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { LoginService } from '../../../_generated/api';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.scss']
})
export class SignUpComponent {
  constructor(public router: Router) {}

  form: FormGroup = new FormGroup({
    username: new FormControl('', Validators.required),
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [
      Validators.required,
      Validators.minLength(8)
    ])
  });

  submit() {
    if (this.form.valid) {
      LoginService.registerUser(
        this.form.get('username')?.value,
        '',
        this.form.get('email')?.value,
        this.form.get('password')?.value
      );
      this.form.reset();
      this.router.navigate(['/jobs']);
    }
  }
}
