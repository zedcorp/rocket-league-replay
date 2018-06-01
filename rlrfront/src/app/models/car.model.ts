import {Coordinates} from './coordinates.model';
import {CarScoreBoard} from './car-scoreboard.model';
import {Team} from './team';

export class Car {
  id: string;
  name: string;
  team: Team;
  ping: number;
  angular_velocity: Coordinates;
  linear_velocity: Coordinates;
  position: Coordinates;
  rot: Coordinates;
  scoreboard: CarScoreBoard;
  color: string;
}
