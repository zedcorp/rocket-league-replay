import {AfterViewInit, Component, OnInit, ViewChild} from '@angular/core';
import {ReplayService} from '../replay.service';

import {Frame} from '../models/frame.model';
import {Car} from '../models/car.model';
import {Coordinates} from '../models/coordinates.model';
import {Ball} from '../models/ball.model';
import {Team} from '../models/team';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-field',
  templateUrl: './field.component.html',
  styleUrls: ['./field.component.css']
})
export class FieldComponent implements OnInit, AfterViewInit {

  matchId;
  frames: Frame[];
  ctx: CanvasRenderingContext2D;
  pause = false;
  imgGround = new Image();
  imgGroundBoosts = new Image();
  showBoosts = true;
  imgBall = new Image();
  imgCar = new Image();
  fieldWidth = 300;
  fieldHeight = 450;
  carLength = 20;
  carWidth = 10;
  speedRatio = 1;
  zRatio = 8;
  xRange;
  yRange;
  zRange;
  fps = 600;
  index = 0;
  ballRadius = 15;
  reds = [];
  blues = [];
  carTeams = {};
  carColors = {};
  availableSpeedRatios = [0.2, 0.5, 1, 2, 3];
  ballAngle = 0;
  blueColors = ['#0066ff', '#00cc66', '#ccf5ff'];
  redColors = ['#ffff00', '#ff9900', '#ff0000'];
  previousPositions = {};
  storedPositionsCount = 20;
  path = false;
  positionRadius = 2;
  progressWidth = 0;
  totalFrames;
  blueScore = 0;
  redScore = 0;
  previousBlueScore = 0;
  previousRedScore = 0;
  goals = [];
  timeDisplay: string;
  totalSeconds: number;

  @ViewChild('canvas') canvas;

  constructor(
    private replayService: ReplayService,
    private route: ActivatedRoute
  ) {
    this.route.params.subscribe(params => this.matchId = params.id);
  }

  ngOnInit() {
    this.imgGround.src = '/assets/Ground.png';
    this.imgGroundBoosts.src = '/assets/groundboosts.png';
    this.imgBall.src = '/assets/Ball.png';
    this.imgCar.src = '/assets/Octane.png';
    this.replayService.getReplay(this.matchId)
      .subscribe(frames => {
        // this.frames = frames.slice(0, 1);
        console.log('frames', frames.length);
        console.log('frames[0]', frames[0]);
        console.log('last frame', frames[frames.length - 1]);
        this.frames = frames;
        this.getData(this.frames);
        console.log(this.goals);
        console.log('this.frames[0]', this.frames[0]);
        this.initTeams(this.frames[0]);
        this.drawFrames();
      });
  }

  ngAfterViewInit() {
    const can = this.canvas.nativeElement;
    this.ctx = can.getContext('2d');

    this.clear();
  }

  initTeams(frame: Frame) {
    Object.entries(frame.cars).forEach(([id, car]) => {
      const team = (car.loc.y > 0) ? Team.RED : Team.BLUE;
      this.carTeams[id] = team;
      this.carColors[id] = (car.loc.y > 0) ? Team.RED : Team.BLUE;
      if (team === Team.RED) {
        this.carColors[id] = this.redColors[0];
        this.redColors.splice(0, 1);
      } else {
        this.carColors[id] = this.blueColors[0];
        this.blueColors.splice(0, 1);
      }
    });
    console.log(this.carColors);
  }

  // Controls

  increaseSpeed() {
    const i = this.availableSpeedRatios.indexOf(this.speedRatio);
    if (i === this.availableSpeedRatios.length - 1) {
      return;
    }
    this.speedRatio = this.availableSpeedRatios[i + 1];
  }

  decreaseSpeed() {
    const i = this.availableSpeedRatios.indexOf(this.speedRatio);
    if (i === 0) {
      return;
    }
    this.speedRatio = this.availableSpeedRatios[i - 1];
  }

  setProgress(event) {
    const totalWidth = document.getElementById('total-prog').offsetWidth;
    this.index = Math.trunc( event.offsetX * this.totalFrames / totalWidth);
  }

  // Data

  getData(frames: Frame[]) {
    this.totalFrames = frames.length;
    this.totalSeconds = Math.trunc(this.frames[this.frames.length - 10].time);

    const xs = [];
    const ys = [];
    const zs = [];

    frames.forEach((frame, frameIndex) => {
      Object.entries(frame.cars).forEach(([id, car]) => {
        if (car.loc.x !== null) {
          xs.push(car.loc.x);
        }
        if (car.loc.y !== null) {
          ys.push(car.loc.y);
        }
        if (car.loc.z !== null) {
          zs.push(car.loc.z);
        }
      });

      if (frame.scoreboard.team1 > this.previousRedScore) {
        this.previousRedScore = frame.scoreboard.team1;
        this.goals.push({
          team: Team.RED,
          color: 'red',
          frame: frameIndex,
          offset: this.getGoalMargin(frameIndex)
        });
      }
      if (frame.scoreboard.team0 > this.previousBlueScore) {
        this.previousBlueScore = frame.scoreboard.team0;
        this.goals.push({
          team: Team.BLUE,
          color: 'blue',
          frame: frameIndex,
          offset: this.getGoalMargin(frameIndex)
        });
      }
    });

    this.xRange = Math.max(...xs) - Math.min(...xs);
    this.yRange = Math.max(...ys) - Math.min(...ys);
    this.zRange = Math.max(...zs) - Math.min(...zs);
  }

  getGoalMargin(frameIndex) {
    return Math.trunc((frameIndex / this.totalFrames) * document.getElementById('total-prog').offsetWidth);
  }

  updateTeams(frame: Frame) {
    this.reds = [];
    this.blues = [];
    Object.entries(frame.cars).forEach(([id, car]) => {
      const team = this.carTeams[id];
      if (team === Team.RED) {
        this.reds.push(car);
      } else {
        this.blues.push(car);
      }
    });
    this.reds.sort(this.compareScore);
    this.blues.sort(this.compareScore);
  }

  compareScore(car1: Car, car2: Car) {
    return car2.scoreboard.score - car1.scoreboard.score;
  }

  updatePreviousPositions(cars: Car[]) {
    Object.entries(cars).forEach(([carId, car]) => {
      if (!this.previousPositions[carId]) {
        this.previousPositions[carId] = [];
      } else if (this.index % 3 === 0) {
        if (this.previousPositions[carId].length > this.storedPositionsCount) {
          this.previousPositions[carId].shift();
        }
        this.previousPositions[carId].push(car.loc);
      }
    });
  }

  updateProgress() {
    const prog = document.getElementById('prog');
    const width = prog.parentElement.offsetWidth;
    this.progressWidth = Math.trunc((this.index / this.totalFrames) * width);
  }

  setCarIds(cars: Car[]) {
    Object.entries(cars).forEach(([carId, car]) => {
      car.id = carId;
    });
  }

  updateTime(frame: Frame) {
    // console.log(this.totalSeconds);
    const frameSeconds = Math.trunc(frame.time);
    const frameMinutes = Math.trunc(frameSeconds / 60);
    const totalMinutes = Math.trunc(this.totalSeconds / 60);
    this.timeDisplay = frameMinutes + ':' + frameSeconds % 60 + ' / ' + totalMinutes + ':' + this.totalSeconds % 60;
  }

  // Draw

  clear() {
    this.ctx.clearRect(0, 0, this.fieldWidth, this.fieldHeight);
    if (this.showBoosts) {
      this.ctx.drawImage(this.imgGroundBoosts, -5, -40, this.fieldWidth + 10, this.fieldHeight + 80);
    } else {
      this.ctx.drawImage(this.imgGround, -30, -30, this.fieldWidth + 60, this.fieldHeight + 60);
    }
  }

  getScaledPos(loc: Coordinates) {
    return {
      x: Math.trunc((loc.x * this.fieldWidth / this.xRange) + (this.fieldWidth / 2)),
      y: Math.trunc((loc.y * this.fieldHeight / this.yRange) + (this.fieldHeight / 2)),
      z: 1 + (loc.z * this.zRatio / this.zRange)
    };
  }

  drawCar(id: string, car: Car) {
    this.ctx.save();

    const scaledPos = this.getScaledPos(car.loc);
    const x = scaledPos.x;
    const y = scaledPos.y;
    const angle = Math.atan2(car.lin_vel.y, car.lin_vel.x) + (Math.PI / 2);

    this.ctx.translate(x, y);
    this.ctx.rotate(angle);
    this.ctx.scale(scaledPos.z, scaledPos.z);

    this.ctx.fillStyle = this.carColors[id];
    this.ctx.fillRect(-this.carWidth / 2, -this.carLength / 2, this.carWidth, this.carLength);
    this.ctx.drawImage(this.imgCar, -this.carWidth / 2, -this.carLength / 2, this.carWidth, this.carLength);

    this.ctx.restore();

    if (this.pause || this.path) {
      this.drawPath(id);
    }
  }

  drawPath(carId) {
    for (const position of this.previousPositions[carId]) {
      this.ctx.save();
      const scaledPos = this.getScaledPos(position);
      const x = scaledPos.x;
      const y = scaledPos.y;
      const radius = this.positionRadius * scaledPos.z;
      this.ctx.translate(x, y);
      this.ctx.fillStyle = this.carColors[carId];
      this.ctx.beginPath();
      this.ctx.arc(0, 0, radius, 0, 2 * Math.PI);
      this.ctx.closePath();
      this.ctx.fill();
      this.ctx.restore();
    }
  }

  drawCars(cars: Car[]) {
    Object.entries(cars).forEach(([id, car]) => {
      this.drawCar(id, car);
    });
  }

  drawBall(ball: Ball) {
    this.ctx.save();
    const scaledPos = this.getScaledPos(ball.loc);
    const x = scaledPos.x;
    const y = scaledPos.y;
    const radius = this.ballRadius * scaledPos.z;
    this.ctx.translate(x, y);
    this.ctx.rotate(this.ballAngle);
    this.ctx.drawImage(this.imgBall, -radius / 2, -radius / 2, radius, radius);
    this.ctx.arc(x, y, radius, 0, 2 * Math.PI);
    this.ballAngle += this.pause ? 0 : 0.05;

    if (this.ballAngle >= 360) {
      this.ballAngle = 0;
    }
    this.ctx.restore();
  }

  drawFrames = () => {
    if (this.index === this.frames.length - 1) {
      return;
    }
    this.clear();
    if (!this.pause) {
      this.index = this.index + 1;
    }
    const frame = this.frames[this.index];

    if (this.index % 5 === 0) {
      this.updateTime(frame);
    }

    this.blueScore = frame.scoreboard.team0;
    this.redScore = frame.scoreboard.team1;

    this.setCarIds(frame.cars);

    this.updatePreviousPositions(frame.cars);
    this.updateProgress();

    this.drawCars(frame.cars);
    this.drawBall(frame.ball);
    if (this.index % 20 === 0) {
      this.updateTeams(frame);
    }
    setTimeout(this.drawFrames.bind({}), (1000 / 60) / this.speedRatio);
  }
}
