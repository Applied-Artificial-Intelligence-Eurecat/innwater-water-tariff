import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RegistComponent } from './regist.component';

describe('RegistComponent', () => {
  let component: RegistComponent;
  let fixture: ComponentFixture<RegistComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RegistComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RegistComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
