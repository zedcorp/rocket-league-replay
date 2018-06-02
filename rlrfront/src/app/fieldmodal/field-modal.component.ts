import {Component, Input, OnInit, ViewEncapsulation} from '@angular/core';

import {NgbActiveModal} from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-field-modal',
  templateUrl: './field-modal.component.html',
  styleUrls: ['./field-modal.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class FieldModalComponent implements OnInit {

  @Input() matchId;

  constructor(public activeModal: NgbActiveModal) { }

  ngOnInit() {
  }

}
