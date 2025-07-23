import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IncitatifComponent } from './incitatif.component';

describe('IncitatifComponent', () => {
  let component: IncitatifComponent;
  let fixture: ComponentFixture<IncitatifComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ IncitatifComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(IncitatifComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
