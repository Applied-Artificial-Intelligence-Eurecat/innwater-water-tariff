import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GemaComponent } from './gema.component';

describe('GemaComponent', () => {
  let component: GemaComponent;
  let fixture: ComponentFixture<GemaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GemaComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GemaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
