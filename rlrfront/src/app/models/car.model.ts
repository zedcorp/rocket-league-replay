import {Coordinates} from './coordinates.model';
import {CarScoreBoard} from './car-scoreboard.model';
import {Team} from './team';

export class Car {
  id: string;
  name: string;
  boost;
  team: Team;
  ping: number;
  dist_ball: number
  angular_velocity: Coordinates;
  linear_velocity: Coordinates;
  position: Coordinates;
  rotation: Coordinates;
  scoreboard: CarScoreBoard;
  color: string;
  demolition;
  boost_pickup;
}
