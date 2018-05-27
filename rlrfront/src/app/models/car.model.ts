import {Coordinates} from './coordinates.model';
import {CarScoreBoard} from './car-scoreboard.model';
import {Team} from './team';

export class Car {
  name: string;
  team: Team;
  ping: number;
  ang_vel: Coordinates;
  lin_vel: Coordinates;
  loc: Coordinates;
  rot: Coordinates;
  scoreboard: CarScoreBoard;
}
