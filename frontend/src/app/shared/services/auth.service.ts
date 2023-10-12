import { Injectable } from '@angular/core';
import { LoginService } from '../../../_generated/api';
import jwt_decode from 'jwt-decode';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  constructor() {}

  login(username: string, password: string) {
    return LoginService.login({
      username: username,
      password: password
    }).then((res) => {
      this.setSession(res);
    });
  }

  getDecodedAccessToken(token: string): any {
    try {
      return jwt_decode(token);
    } catch (Error) {
      return null;
    }
  }

  private setSession(authResult: any) {
    const tokenInfo = this.getDecodedAccessToken(authResult.access_token);
    localStorage.setItem('id_token', authResult.access_token);
    localStorage.setItem('expires_at', JSON.stringify(tokenInfo.exp));
  }

  logout() {
    localStorage.removeItem('id_token');
    localStorage.removeItem('expires_at');
  }

  public isLoggedIn() {
    return true;
  }

  isLoggedOut() {
    return !this.isLoggedIn();
  }

  getExpiration() {
    const expiration = localStorage.getItem('expires_at')!;
    return JSON.parse(expiration);
  }
}
