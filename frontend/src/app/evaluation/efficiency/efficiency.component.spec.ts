import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EfficiencyComponent } from './efficiency.component';

describe('EfficiencyComponent', () => {
  let component: EfficiencyComponent;
  let fixture: ComponentFixture<EfficiencyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EfficiencyComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EfficiencyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
