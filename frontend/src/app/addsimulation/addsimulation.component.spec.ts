import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddsimulationComponent } from './addsimulation.component';

describe('AddsimulationComponent', () => {
  let component: AddsimulationComponent;
  let fixture: ComponentFixture<AddsimulationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AddsimulationComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddsimulationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
