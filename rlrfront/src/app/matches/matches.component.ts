import {Component, Input, OnInit} from '@angular/core';
import {Match} from '../models/match';
import {Player} from '../models/player';
import {MatchService} from '../match.service';

@Component({
  selector: 'app-matches',
  templateUrl: './matches.component.html',
  styleUrls: ['./matches.component.css']
})
export class MatchesComponent implements OnInit {

  @Input() player: Player;
  matches: Match[];

  constructor(private matchService: MatchService) {
  }

  ngOnInit() {
    this.getMatches();
  }

  getMatches(): void {
    this.matchService.getMatches(this.player.id)
      .subscribe(matches => this.matches = matches);
  }
}
