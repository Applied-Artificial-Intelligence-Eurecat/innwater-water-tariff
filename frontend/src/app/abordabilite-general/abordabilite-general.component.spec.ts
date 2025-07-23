import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AbordabiliteGeneralComponent } from './abordabilite-general.component';

describe('AbordabiliteGeneralComponent', () => {
  let component: AbordabiliteGeneralComponent;
  let fixture: ComponentFixture<AbordabiliteGeneralComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AbordabiliteGeneralComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AbordabiliteGeneralComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
