import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PenParadeChartComponent } from './pen-parade-chart.component';

describe('PenParadeChartComponent', () => {
  let component: PenParadeChartComponent;
  let fixture: ComponentFixture<PenParadeChartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PenParadeChartComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PenParadeChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
