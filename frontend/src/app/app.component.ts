import {Component} from '@angular/core';
import {NavigationEnd, Router, ActivatedRoute} from '@angular/router';
import {AuthService} from './auth.service';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent {
    title = 'newts';
    showHeader: boolean = true;
    showFooter: boolean = true;

    constructor(
        private router: Router,
        private route: ActivatedRoute,
        private authService: AuthService
    ) {
        // Initial check from cookies
        this.showFooter = this.getCookie('hide_footer') !== '1';

        this.router.events.subscribe((val) => {
            if (val instanceof NavigationEnd) {
                if (val.url.startsWith('/wait')) {
                    this.showHeader = false;
                } else {
                    this.showHeader = true;
                }

                const urlTree = this.router.parseUrl(val.url);
                const hideFooterParam = urlTree.queryParamMap.get('hide_footer');
                if (hideFooterParam === '1') {
                    this.showFooter = false;
                    this.setCookie('hide_footer', '1', 365);
                } else if (hideFooterParam === '0') {
                    this.showFooter = true;
                    this.setCookie('hide_footer', '0', 365);
                } else {

                }
            }
        });
    }

    private setCookie(name: string, value: string, days: number) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        const expires = "; expires=" + date.toUTCString();
        document.cookie = name + "=" + (value || "") + expires + "; path=/; SameSite=Lax";
    }

    private getCookie(name: string) {
        const nameEQ = name + "=";
        const ca = document.cookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) == ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
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
