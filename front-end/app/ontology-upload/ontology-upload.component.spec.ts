import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OntologyUploadComponent } from './ontology-upload.component';

describe('OntologyUploadComponent', () => {
  let component: OntologyUploadComponent;
  let fixture: ComponentFixture<OntologyUploadComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ OntologyUploadComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OntologyUploadComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
