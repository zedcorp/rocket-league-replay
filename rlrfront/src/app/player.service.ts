import {Injectable} from '@angular/core';
import {Player} from './models/player';
import {Observable} from 'rxjs';
import {HttpClient} from '@angular/common/http';
import {environment} from "../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class PlayerService {

  private playersUrl = environment.rest_url;

  constructor(private http: HttpClient) {
  }

  getPlayers(): Observable<Player[]> {
    return this.http.get<Player[]>(this.playersUrl + 'list_players');
  }

  getPlayer(id: string): Observable<Player> {
    return this.http.get<Player>(this.playersUrl + 'players/' + id);
  }
}
