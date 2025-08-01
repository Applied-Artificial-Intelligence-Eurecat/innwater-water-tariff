import {Component} from '@angular/core';
import {NavigationEnd, Router} from '@angular/router';
import {AuthService} from './auth.service';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent {
    title = 'newts';
    showHeader: boolean = true;

    constructor(
        private router: Router,
        private authService: AuthService
    ) {
        router.events.subscribe((val) => {
            if (val instanceof NavigationEnd) {
                if (val.url == '/wait') {
                    this.showHeader = false;
                } else {
                    this.showHeader = true;
                }
            }
        });
    }

    public isLoggedIn(): boolean {
        let status = false;
        if (localStorage.getItem('token') == null) {
            status = false;
        } else {
            status = true;
        }
        return status;
    }

    logout() {
        localStorage.clear();
        // Update auth service state
        this.authService['_isLoggedIn$'].next(false);
        // Redirect to the connect page
        this.router.navigateByUrl('/account');
    }
}
