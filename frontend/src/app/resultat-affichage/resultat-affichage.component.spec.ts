import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ResultatAffichageComponent } from './resultat-affichage.component';

describe('ResultatAffichageComponent', () => {
  let component: ResultatAffichageComponent;
  let fixture: ComponentFixture<ResultatAffichageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ResultatAffichageComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ResultatAffichageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
