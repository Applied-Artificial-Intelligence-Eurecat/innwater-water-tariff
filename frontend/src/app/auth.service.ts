import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
    providedIn: 'root',
  })
  export class AuthService {
    private _isLoggedIn$ = new BehaviorSubject<boolean>(false);
    isLoggedIn$ = this._isLoggedIn$.asObservable();
  
    constructor() {
      const token = localStorage.getItem('token');
      this._isLoggedIn$.next(!!token);
    }
  
    login(username: string, password: string) {
    }
  }