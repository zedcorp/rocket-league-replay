import {Ball} from './ball.model';
import {Car} from './car.model';
import {ScoreBoard} from './scoreboard.model';

export class Frame {
  ball: Ball;
  cars: Car[];
  scoreBoard: ScoreBoard;
  color: string;
}
