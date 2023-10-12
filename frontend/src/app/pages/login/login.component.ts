import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { LoginService } from '../../../_generated/api';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  constructor(public router: Router) {}

  form: FormGroup = new FormGroup({
    username: new FormControl(''),
    password: new FormControl('')
  });

  submit() {
    if (this.form.valid) {
      LoginService.login({
        username: this.form.get('username')?.value,
        password: this.form.get('password')?.value
      }).then(
        () => {
          console.log('success');
          this.form.reset();
          this.router.navigate(['/jobs']);
        },
        () => {
          console.log('fail');
        }
      );
    }
  }
}
