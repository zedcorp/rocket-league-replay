import {AfterViewInit, Component, OnInit, ViewChild} from '@angular/core';
import {ReplayService} from '../replay.service';

import {Frame} from '../models/frame.model';
import {Car} from '../models/car.model';
import {Coordinates} from '../models/coordinates.model';
import {Ball} from '../models/ball.model';
import {Team} from '../models/team';
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-field',
  templateUrl: './field.component.html',
  styleUrls: ['./field.component.css']
})
export class FieldComponent implements OnInit, AfterViewInit {

  matchId;
  frames: Frame[];
  ctx: CanvasRenderingContext2D;
  // imgGround = new HTMLImageElement();
  imgGround = new Image();
  fieldWidth = 400;
  fieldHeight = 600;
  carLength = 20;
  carWidth = 10;
  speedRatio = 1;
  zRatio = 8;
  xRange;
  yRange;
  zRange;
  fps = 600;
  index = 0;
  ballRadius = 5;
  reds = [];
  blues = [];
  carTeams = {};
  availableSpeedRatios = [0.2, 0.5, 1, 2, 3];

  @ViewChild('canvas') canvas;

  constructor(
    private replayService: ReplayService,
    private route: ActivatedRoute
  ) {
    this.route.params.subscribe(params => this.matchId = params.id);
  }

  ngOnInit() {
    this.imgGround.src = '/assets/Ground.png';
    this.replayService.getReplay(this.matchId)
      .subscribe(frames => {
        // this.frames = frames.slice(0, 1);
        this.frames = frames;
        this.getData(this.frames);
        console.log(this.frames[0]);
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
      this.carTeams[id] = (car.loc.y > 0) ? Team.RED : Team.BLUE;
    });
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

  getData(frames: Frame[]) {
    const xs = [];
    const ys = [];
    const zs = [];

    frames.forEach(frame => {
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
    });

    this.xRange = Math.max(...xs) - Math.min(...xs);
    this.yRange = Math.max(...ys) - Math.min(...ys);
    this.zRange = Math.max(...zs) - Math.min(...zs);
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

  clear() {
    this.ctx.clearRect(0, 0, this.fieldWidth, this.fieldHeight);
    // this.ctx.drawImage(this.imgGround, -30, -30, this.canvas.width + 60, this.canvas.height + 60);
  }

  getScaledPos(loc: Coordinates) {
    return {
      x: Math.floor((loc.x * this.fieldWidth / this.xRange) + (this.fieldWidth / 2)),
      y: Math.floor((loc.y * this.fieldHeight / this.yRange) + (this.fieldHeight / 2)),
      z: 1 + (loc.z * this.zRatio / this.zRange)
    };
  }

  drawCar(car: Car) {
    this.ctx.save();

    const scaledPos = this.getScaledPos(car.loc);
    const x = scaledPos.x;
    const y = scaledPos.y;
    const angle = Math.atan2(car.lin_vel.y, car.lin_vel.x) + (Math.PI / 2);

    this.ctx.translate(x, y);
    this.ctx.rotate(angle);
    this.ctx.scale(scaledPos.z, scaledPos.z);

    this.ctx.fillStyle = 'red';
    this.ctx.fillRect(-this.carWidth / 2, -this.carLength / 2, this.carWidth, this.carLength);
    // this.ctx.drawImage(imgCar, -this.carWidth / 2, -this.carLength / 2, this.carWidth, this.carLength);

    this.ctx.restore();
  }

  drawCars(cars: Car[]) {
    Object.entries(cars).forEach(([id, car]) => {
      this.drawCar(car);
    });
  }

  drawBall(ball: Ball) {
    this.ctx.save();
    this.ctx.fillStyle = 'lightgray';
    this.ctx.beginPath();
    const scaledPos = this.getScaledPos(ball.loc);
    const x = scaledPos.x;
    const y = scaledPos.y;
    const radius = this.ballRadius * scaledPos.z;
    this.ctx.arc(x, y, radius, 0, 2 * Math.PI);
    this.ctx.closePath();
    this.ctx.fill();
    this.ctx.restore();
  }

  drawFrames = () => {
    if (this.index === this.frames.length - 1) {
      return;
    }
    this.clear();
    this.index = this.index + 1;
    const frame = this.frames[this.index];
    this.drawCars(frame.cars);
    this.drawBall(frame.ball);
    if (this.index % 20 === 0) {
      this.updateTeams(frame);
    }
    setTimeout(this.drawFrames.bind({}), (1000 / 60) / this.speedRatio);
  }
}
