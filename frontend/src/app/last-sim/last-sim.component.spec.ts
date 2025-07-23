import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LastSimComponent } from './last-sim.component';

describe('LastSimComponent', () => {
  let component: LastSimComponent;
  let fixture: ComponentFixture<LastSimComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LastSimComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LastSimComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
