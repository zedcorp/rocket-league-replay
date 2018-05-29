import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FieldModalComponent } from './field-modal.component';

describe('FieldModalComponent', () => {
  let component: FieldModalComponent;
  let fixture: ComponentFixture<FieldModalComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FieldModalComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FieldModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
