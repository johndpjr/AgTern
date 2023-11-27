import { Component, OnInit, Input, NgZone } from '@angular/core';
import 'zone.js';
import { LoginService } from 'src/_generated/api';
import { Router } from '@angular/router';
import { LoginComponent } from 'src/app/pages/login/login.component';

@Component({
  selector: 'app-google-sign-in',
  templateUrl: './google-sign-in.component.html',
  styleUrls: ['./google-sign-in.component.scss']
})
export class GoogleSignInComponent implements OnInit {
  @Input() loginRef!: LoginComponent;
  constructor(private zone: NgZone) { }

  ngOnInit(): void {
    // @ts-ignore
    google.accounts.id.initialize({
      client_id:
        '710734565405-3nkf5plf0m4p460osals94rnksheoh93.apps.googleusercontent.com',
      callback: this.handleCredentialResponse.bind(this),
      auto_select: false,
      cancel_on_tap_outside: true
    });
    // @ts-ignore
    google.accounts.id.renderButton(
      // @ts-ignore
      document.getElementById('google-button'),
      { theme: 'outline', size: 'large', width: '100%' }
    );
    // @ts-ignore
    // Enable for an additional "Sign-in with Google" notification on the top right
    // google.accounts.id.prompt((notification: PromptMomentNotification) => {});
  }


  async handleCredentialResponse(googleUser: any) {
    console.log(googleUser);
    var token: string = googleUser.credential

    LoginService.googleLogin(token).then(
      () => {
        // login
        console.log("Resetting");
        this.loginRef.form.reset()
        console.log("Navigating");
        this.zone.run(() => this.loginRef.router.navigate(['/jobs']));
      },
      () => {
        // Do nothing since we failed
        console.log("Failed");
      }
    );
  };

}



