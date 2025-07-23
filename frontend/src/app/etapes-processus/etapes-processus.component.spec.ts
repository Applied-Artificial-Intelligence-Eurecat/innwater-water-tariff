import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EtapesProcessusComponent } from './etapes-processus.component';

describe('EtapesProcessusComponent', () => {
  let component: EtapesProcessusComponent;
  let fixture: ComponentFixture<EtapesProcessusComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EtapesProcessusComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EtapesProcessusComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
