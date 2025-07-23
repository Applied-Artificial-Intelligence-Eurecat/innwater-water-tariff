import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TestTComponent } from './test-t.component';

describe('TestTComponent', () => {
  let component: TestTComponent;
  let fixture: ComponentFixture<TestTComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TestTComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TestTComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
