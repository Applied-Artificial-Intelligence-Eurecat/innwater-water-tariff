import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AbordabiliteComponent } from './abordabilite.component';

describe('AbordabiliteComponent', () => {
  let component: AbordabiliteComponent;
  let fixture: ComponentFixture<AbordabiliteComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AbordabiliteComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AbordabiliteComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
