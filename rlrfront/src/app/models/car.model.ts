import {Coordinates} from './coordinates.model';
import {CarScoreBoard} from './car-scoreboard.model';

export class Car {
  name: string;
  ping: number;
  ang_vel: Coordinates;
  lin_vel: Coordinates;
  loc: Coordinates;
  rot: Coordinates;
  scoreboard: CarScoreBoard;
}
