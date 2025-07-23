import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AffordabilityComponent } from './affordability.component';

describe('AffordabilityComponent', () => {
  let component: AffordabilityComponent;
  let fixture: ComponentFixture<AffordabilityComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AffordabilityComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AffordabilityComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
