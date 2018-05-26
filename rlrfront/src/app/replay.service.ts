import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs/index';
import {Frame} from './models/frame.model';

@Injectable({
  providedIn: 'root'
})
export class ReplayService {

  private url = 'http://localhost:8000/rest/';

  constructor(
    private http: HttpClient
  ) { }

  getReplay(id: string): Observable<Frame[]> {
    return this.http.get<Frame[]>(this.url + 'replays/' + id);
  }
}
