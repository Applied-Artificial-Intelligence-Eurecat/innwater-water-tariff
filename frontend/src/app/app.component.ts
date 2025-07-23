import { Component, ViewChild } from '@angular/core';
import { BreakpointObserver } from '@angular/cdk/layout';
import { MatSidenav } from '@angular/material/sidenav';
import { delay, filter } from 'rxjs/operators';
import { Router,NavigationEnd } from '@angular/router';
import { UntilDestroy, untilDestroyed } from '@ngneat/until-destroy';

@UntilDestroy()
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'newts';
  @ViewChild(MatSidenav)
  sidenav!: MatSidenav;
  showHeader: boolean = true;

  constructor(private observer: BreakpointObserver, private router: Router) {
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
    if (localStorage.getItem('userid') == null) {      
       status = false;      
    }
      else {      
       status = true;      
       }      
    return status;      
    }   
    logout(){
      localStorage.clear();
      this.router.navigateByUrl('/');
    } 

  ngAfterViewInit() {
    this.observer
      .observe(['(max-width: 800px)'])
      .pipe(delay(1), untilDestroyed(this))
      .subscribe((res:any) => {
        if (res.matches) {
          this.sidenav.mode = 'over';
          this.sidenav.close();
        } else {
          this.sidenav.mode = 'side';
          this.sidenav.open();
        }
      });

    this.router.events
      .pipe(
        untilDestroyed(this),
        filter((e:any) => e instanceof NavigationEnd)
      )
      .subscribe(() => {
        if (this.sidenav.mode === 'over') {
          this.sidenav.close();
        }
      });
  }
}
