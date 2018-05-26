import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {HttpClient} from '@angular/common/http';
import {Match} from './models/match';

@Injectable({
  providedIn: 'root'
})
export class MatchService {

  private playersUrl = 'http://localhost:8000/rest/';  // URL to web api

  constructor(private http: HttpClient) {
  }

  // getMatches(): Observable<Match[]> {
  getMatches(playerId: number): Observable<Match[]> {
    return this.http.get<Match[]>(this.playersUrl + 'matches/' + playerId);
  }
}
