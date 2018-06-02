import {Component, OnInit} from '@angular/core';

import {NgbModal} from '@ng-bootstrap/ng-bootstrap';

import {ReplayService} from '../replay.service';
import {Replay} from '../models/replay';
import {ActivatedRoute} from '@angular/router';
import {FieldModalComponent} from '../fieldmodal/field-modal.component';

@Component({
  selector: 'app-replays',
  templateUrl: './replays.component.html',
  styleUrls: ['./replays.component.css']
})
export class ReplaysComponent implements OnInit {

  playerId;
  replays: Replay[];
  modalRef;

  constructor(
    private replayService: ReplayService,
    private route: ActivatedRoute,
    private modalService: NgbModal
  ) {
    this.route.params.subscribe(params => this.playerId = params.id);
  }

  ngOnInit() {
    this.replayService.getReplays(this.playerId)
      .subscribe(replays => {
        console.log(replays[0]);
        this.replays = replays;
        this.replays.sort((r1, r2) => r2.datetime - r1.datetime);
      });
  }

  open(matchId: string) {
    this.modalRef = this.modalService.open(FieldModalComponent, { size: 'lg'});
    this.modalRef.componentInstance.matchId = matchId;
  }
}
