import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UsageTarificationComponent } from './usage-tarification.component';

describe('UsageTarificationComponent', () => {
  let component: UsageTarificationComponent;
  let fixture: ComponentFixture<UsageTarificationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UsageTarificationComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UsageTarificationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
