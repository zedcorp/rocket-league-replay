import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FpspickerComponent } from './fpspicker.component';

describe('FpspickerComponent', () => {
  let component: FpspickerComponent;
  let fixture: ComponentFixture<FpspickerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FpspickerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FpspickerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
