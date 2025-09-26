import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IncentiveEffectComponent } from './incentive-effect.component';

describe('IncentiveEffectComponent', () => {
  let component: IncentiveEffectComponent;
  let fixture: ComponentFixture<IncentiveEffectComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ IncentiveEffectComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(IncentiveEffectComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
