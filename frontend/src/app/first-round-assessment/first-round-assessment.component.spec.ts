import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FirstRoundAssessmentComponent } from './first-round-assessment.component';

describe('FirstRoundAssessmentComponent', () => {
  let component: FirstRoundAssessmentComponent;
  let fixture: ComponentFixture<FirstRoundAssessmentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FirstRoundAssessmentComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FirstRoundAssessmentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
