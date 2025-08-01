import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router, UrlTree } from '@angular/router';
import { Observable } from 'rxjs';
import { map, take } from 'rxjs/operators';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  constructor(private authService: AuthService, private router: Router) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
    return this.authService.isLoggedIn$.pipe(
      take(1),
      map(isLoggedIn => {
        const url = state.url;
        
        // If trying to access /account while logged in, redirect to /home
        if (isLoggedIn && url === '/account') {
          return this.router.createUrlTree(['/home']);
        }
        
        // If trying to access /home while not logged in, redirect to /account
        if (!isLoggedIn && url === '/home') {
          return this.router.createUrlTree(['/account']);
        }
        
        // Otherwise allow access
        return true;
      })
    );
  }
}