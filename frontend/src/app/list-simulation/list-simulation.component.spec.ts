import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListSimulationComponent } from './list-simulation.component';

describe('ListSimulationComponent', () => {
  let component: ListSimulationComponent;
  let fixture: ComponentFixture<ListSimulationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ListSimulationComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ListSimulationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
