import { Component, Input } from '@angular/core';
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
    password: new FormControl('', [
      Validators.required,
      Validators.minLength(8)
    ])
  });

  submit() {
    console.log('here');
    if (this.form.valid) {
      LoginService.registerUser(
        this.form.get('username')?.value,
        'Placeholder',
        'some@email.com',
        this.form.get('password')?.value
      );
      this.form.reset();
      this.router.navigate(['/jobs']);
    }
  }
  @Input() error: string | null = null;
}
