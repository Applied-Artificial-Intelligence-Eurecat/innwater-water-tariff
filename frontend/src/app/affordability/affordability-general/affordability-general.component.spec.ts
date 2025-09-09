import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AffordabilityGeneralComponent } from './affordability-general.component';

describe('ResultatAffichageComponent', () => {
  let component: AffordabilityGeneralComponent;
  let fixture: ComponentFixture<AffordabilityGeneralComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AffordabilityGeneralComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AffordabilityGeneralComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
