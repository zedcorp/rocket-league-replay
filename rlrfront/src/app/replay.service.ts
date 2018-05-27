import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs/index';
import {Frame} from './models/frame.model';
import {environment} from '../environments/environment';
import {Replay} from './models/replay';

@Injectable({
  providedIn: 'root'
})
export class ReplayService {

  private url = environment.rest_url;

  constructor(private http: HttpClient) {
  }

  getReplays(playerId: number): Observable<Replay[]> {
    return this.http.get<Replay[]>(
      this.url + 'replays',
      {params: {userid: String(playerId)}}
    );
  }

  getReplay(id: string): Observable<Frame[]> {
    return this.http.get<Frame[]>(this.url + 'replays/' + id);
  }
}
