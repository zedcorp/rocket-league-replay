import { Injectable } from '@angular/core';
import {Player} from "./player";
import { PLAYERS } from './mock-players';
import { Observable, of } from 'rxjs';
import { MessageService } from './message.service';

@Injectable({
  providedIn: 'root'
})
export class PlayerService {

  constructor(private messageService: MessageService) { }

  getPlayers(): Observable<Player[]> {
    this.messageService.add('HeroService: fetched heroes');
    return of(PLAYERS);
  }

  getPlayer(id: string): Observable<Player> {
    // TODO: send the message _after_ fetching the player
    this.messageService.add(`PlayerService: fetched player id=${id}`);
    return of(PLAYERS.find(player => player.id === id));
  }
}
