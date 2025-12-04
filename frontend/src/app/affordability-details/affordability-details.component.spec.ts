import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AffordabilityDetailsComponent } from './affordability-details.component';

describe('AffordabilityDetailsComponent', () => {
  let component: AffordabilityDetailsComponent;
  let fixture: ComponentFixture<AffordabilityDetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AffordabilityDetailsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AffordabilityDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
