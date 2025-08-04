import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SimplifiedDashboardComponent } from './simplified-dashboard.component';

describe('SimplifiedDashboardComponent', () => {
  let component: SimplifiedDashboardComponent;
  let fixture: ComponentFixture<SimplifiedDashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SimplifiedDashboardComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SimplifiedDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
