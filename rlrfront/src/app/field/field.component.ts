import {AfterViewInit, Component, Input, OnInit, ViewChild} from '@angular/core';
import {ReplayService} from '../replay.service';

import {Frame} from '../models/frame.model';
import {Car} from '../models/car.model';
import {Coordinates} from '../models/coordinates.model';
import {Ball} from '../models/ball.model';
import {Team} from '../models/team';
import {ActivatedRoute} from '@angular/router';
import {Boost} from '../models/boost.model';

@Component({
  selector: 'app-field',
  templateUrl: './field.component.html',
  styleUrls: ['./field.component.css']
})
export class FieldComponent implements OnInit, AfterViewInit {

  allBoosts = [];
  boostsMid = [
    {
      'X': 3450,
      'Y': 0,
      'Z': 17.01,
      big: true,
      color: '#659df7'
    },
    {
      'X': 1040.55,
      'Y': 0,
      'Z': 17.01,
      color: '#659df7'
    },
    {
      'X': -1174.4,
      'Y': 0,
      'Z': 17.01,
      color: '#659df7'
    },
    {
      'X': -3450,
      'Y': 0,
      'Z': 16.98,
      big: true,
      color: '#659df7'
    }
  ];
  boostsTop = [
    {
      'X': -2900,
      'Y': -4154,
      'Z': 17.01,
      big: true,
      color: '#659df7'
    },
    {
      'X': -1850,
      'Y': -4154,
      'Z': 17.01,
      color: '#659df7'
    },
    {
      'X': 0,
      'Y': -4154,
      'Z': 19.06,
      color: '#659df7'
    },
    {
      'X': 2900,
      'Y': -4154,
      'Z': 17.01,
      color: '#659df7',
      big: true
    },
    {
      'X': 1850,
      'Y': -4154,
      'Z': 17,
      color: '#659df7'
    },

    {
      'X': -875,
      'Y': -3250,
      'Z': 44.03,
      color: '#659df7'
    },
    {
      'X': 875,
      'Y': -3250,
      'Z': 19.53,
      color: '#659df7'
    },

    {
      'X': 0,
      'Y': -2900,
      'Z': 17.01,
      color: '#659df7'
    },

    {
      'X': 3550,
      'Y': -2500,
      'Z': 17.01,
      color: 'orange'
    },
    {
      'X': -3550,
      'Y': -2500,
      'Z': 17.01,
      color: 'orange'
    },
    {
      'X': -1745,
      'Y': -2500,
      'Z': 104.96,
      color: 'orange'
    },
    {
      'X': 1745,
      'Y': -2500,
      'Z': 17.01,
      color: 'orange'
    },
    {
      'X': 0,
      'Y': -1209.91,
      'Z': 17.01,
      color: 'magenta'
    },
    {
      'X': 1972.35,
      'Y': -1123.49,
      'Z': 17.01,
      color: 'magenta'
    },
    {
      'X': -2180.67,
      'Y': -992.76,
      'Z': 17.01,
      color: 'magenta'
    },
  ];

  @Input() matchId;
  frames: Frame[];
  ctx: CanvasRenderingContext2D;
  pause = false;
  imgGround = new Image();
  imgGroundBoosts = new Image();
  showBoosts = true;
  imgBall = new Image();
  imgCarBlue1 = new Image();
  imgCarBlue2 = new Image();
  imgCarBlue3 = new Image();
  imgCarRed1 = new Image();
  imgCarRed2 = new Image();
  imgCarRed3 = new Image();
  redImages = [this.imgCarRed1, this.imgCarRed2, this.imgCarRed3];
  blueImages = [this.imgCarBlue1, this.imgCarBlue2, this.imgCarBlue3];
  carImages = {};
  imgDemolition = new Image();
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
  availableSpeedRatios = [0.2, 0.5, 1, 2, 3, 10];
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
  finished = false;
  boostPickups = [];
  boostPickupsPerCar = {};
  boostPerCar = {};

  // Heatmaps
  showHeatmap = false;
  selectedCarIdHeatmap;
  heatmapCarLocations: Coordinates[];

  @ViewChild('canvas') canvas;

  constructor(private replayService: ReplayService,
              private route: ActivatedRoute) {
    this.route.params.subscribe(params => this.matchId = params.id);
  }

  ngOnInit() {
    console.log('matchId', this.matchId);
    this.imgGround.src = '/assets/Ground.png';
    this.imgGroundBoosts.src = '/assets/groundwhite.png';
    this.imgBall.src = '/assets/Ball.png';
    this.imgCarBlue1.src = '/assets/car_blue_1.png';
    this.imgCarBlue2.src = '/assets/car_blue_2.png';
    this.imgCarBlue3.src = '/assets/car_blue_3.png';
    this.imgCarRed1.src = '/assets/car_red_1.png';
    this.imgCarRed2.src = '/assets/car_red_2.png';
    this.imgCarRed3.src = '/assets/car_red_3.png';
    this.imgDemolition.src = '/assets/boom.png';

    Array.prototype.push.apply(this.allBoosts, this.boostsMid);
    Array.prototype.push.apply(this.allBoosts, this.boostsTop);
    Array.prototype.push.apply(this.allBoosts, this.boostsTop.map(boost => {
      return {
        X: boost.X,
        Y: -boost.Y,
        Z: boost.Z,
        color: boost.color,
        big: boost.big
    };
    }));

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

  showHeatMap(carId: string) {
    this.pause = true;
    this.selectedCarIdHeatmap = carId;
    const data = [];
    this.frames.forEach((frame) => {
      Object.entries(frame.cars).forEach(([id, car]) => {
        if (id === carId && car.position && car.linear_velocity) {
          if (car.linear_velocity.X !== 0 || car.linear_velocity.Y !== 0 || car.linear_velocity.Z !== 0) {
            data.push(this.getScaledPos(car.position));
          }
        }
      });
    });
    this.heatmapCarLocations = data;
    this.showHeatmap = true;
  }

  hideHeatMap() {
    this.selectedCarIdHeatmap = null;
    this.showHeatmap = false;
    this.pause = false;
  }

  initTeams(frame: Frame) {
    Object.entries(frame.cars).forEach(([id, car]) => {
      if (!car.position) {
        return;
      }
      const team = (car.position.Y > 0) ? Team.RED : Team.BLUE;
      this.carTeams[id] = team;

      if (team === Team.RED) {
        this.carColors[id] = this.redColors[0];
        this.redColors.splice(0, 1);
        this.carImages[id] = this.redImages[0];
        this.redImages.splice(0, 1);
      } else {
        this.carColors[id] = this.blueColors[0];
        this.blueColors.splice(0, 1);
        this.carImages[id] = this.blueImages[0];
        this.blueImages.splice(0, 1);
      }
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

  setProgress(event) {
    const totalWidth = document.getElementById('total-prog').offsetWidth;
    this.index = Math.trunc(event.offsetX * this.totalFrames / totalWidth);
    if (this.finished) {
      this.finished = false;
      this.drawFrames();
    }
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
        if (car.boost_pickup) {
          this.boostPickups.push(car.position as Boost);
          if (!this.boostPickupsPerCar[car.name]) {
            this.boostPickupsPerCar[car.name] = 0;
          }
          this.boostPickupsPerCar[car.name]++;
        }
        if (!car.position || !car.position.X) {
          return;
        }
        if (car.position.X !== null) {
          xs.push(car.position.X);
        }
        if (car.position.Y !== null) {
          ys.push(car.position.Y);
        }
        if (car.position.Z !== null) {
          zs.push(car.position.Z);
        }
      });

      if (frame.teams['red'] && frame.teams['red'].score > this.previousRedScore) {
        this.previousRedScore = frame.teams['red'].score;
        this.goals.push({
          team: Team.RED,
          color: 'red',
          frame: frameIndex,
          offset: this.getGoalMargin(frameIndex)
        });
      }
      if (frame.teams['blue'] && frame.teams['blue'].score > this.previousBlueScore) {
        this.previousBlueScore = frame.teams['blue'].score;
        this.goals.push({
          team: Team.BLUE,
          color: 'blue',
          frame: frameIndex,
          offset: this.getGoalMargin(frameIndex)
        });
      }
    });

    console.log('this.boostPickupsPerCar', this.boostPickupsPerCar);
    console.log('this.boostPickups.length', this.boostPickups.length);

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
    this.reds.sort((c1, c2) => c1.name.localeCompare(c2.name));
    this.blues.sort((c1, c2) => c1.name.localeCompare(c2.name));
  }

  updatePreviousPositions(cars: Car[]) {
    if (this.pause) {
      return;
    }
    Object.entries(cars).forEach(([carId, car]) => {
      if (!this.previousPositions[carId]) {
        this.previousPositions[carId] = [];
      } else if (this.index % 3 === 0) {
        if (this.previousPositions[carId].length > this.storedPositionsCount) {
          this.previousPositions[carId].shift();
        }
        this.previousPositions[carId].push(car.position);
      }
    });
  }

  updateProgress() {
    const prog = document.getElementById('prog');
    const width = prog.parentElement.offsetWidth;
    this.progressWidth = Math.trunc((this.index / this.totalFrames) * width);
  }

  updateCarsBoost(cars: Car[]) {
    Object.entries(cars).forEach(([carId, car]) => {
      this.boostPerCar[carId] = car.boost;
    });
  }

  setCarIds(cars: Car[]) {
    Object.entries(cars).forEach(([carId, car]) => {
      car.id = carId;
    });
  }

  updateTime(frame: Frame) {
    const frameSeconds = Math.trunc(frame.time);
    const frameMinutes = Math.trunc(frameSeconds / 60);
    const totalMinutes = Math.trunc(this.totalSeconds / 60);
    this.timeDisplay =
      this.addLeading0(frameMinutes)
      + ':'
      + this.addLeading0(frameSeconds % 60)
      + ' / '
      + this.addLeading0(totalMinutes)
      + ':'
      + this.addLeading0(this.totalSeconds % 60);
  }

  addLeading0(value) {
    return ((value.toString().length === 1) ? '0' : '') + value;
  }

  // Draw

  clear() {
    this.ctx.clearRect(0, 0, this.fieldWidth, this.fieldHeight);
    if (this.showBoosts) {
      this.ctx.drawImage(this.imgGroundBoosts, -5, -40, this.fieldWidth + 10, this.fieldHeight + 80);
    } else {
      this.ctx.drawImage(this.imgGround, -30, -30, this.fieldWidth + 60, this.fieldHeight + 60);
    }
    this.drawBoosts();
  }

  getScaledPos(position: Coordinates) {
    return {
      X: Math.trunc((position.X * this.fieldWidth / this.xRange) + (this.fieldWidth / 2)),
      Y: Math.trunc((position.Y * this.fieldHeight / this.yRange) + (this.fieldHeight / 2)),
      Z: 1 + (position.Z * this.zRatio / this.zRange)
    } as Coordinates;
  }

  drawBoosts() {
    const time = this.frames[this.index].time;
    for (const boost of this.allBoosts) {
      const spawnDelay = 5 * (boost.big ? 2 : 1);
      if (!boost.pickupTime || time < boost.pickupTime || time - boost.pickupTime > spawnDelay) {
        this.ctx.save();
        const scaledPos = this.getScaledPos(boost);
        const x = scaledPos.X;
        const y = scaledPos.Y;
        const radius = 5 + (boost.big ? 3 : 0);
        this.ctx.translate(x, y);
        this.ctx.fillStyle = (boost.Y === 0) ? 'black' : (boost.Y < 0) ? '#659df7' : '#ef3939';
        this.ctx.beginPath();
        this.ctx.arc(0, 0, radius, 0, 2 * Math.PI);
        this.ctx.closePath();
        this.ctx.fill();
        this.ctx.restore();
      }
    }
  }

  getCloseBoosts(car: Car) {
    const response: Boost[] = [];
    const maxDistance = 300;
    for (const boost of this.allBoosts) {
      const x = boost.X - car.position.X;
      const y = boost.Y - car.position.Y;
      const distance = Math.sqrt(x * x + y * y);
      if (distance < maxDistance) {
        response.push(boost);
      }
    }
    return response;
  }

  updateBoosts(car: Car) {
    const closeBoosts = this.getCloseBoosts(car);
    for (const boost of closeBoosts) {
      boost.pickupTime = this.frames[this.index].time;
    }
  }

  drawCar(id: string, car: Car) {

    if (!car.position) {
      return;
    }

    this.ctx.save();

    const scaledPos = this.getScaledPos(car.position);
    const x = scaledPos.X;
    const y = scaledPos.Y;
    const angle = Math.atan2(car.linear_velocity.Y, car.linear_velocity.X) + (Math.PI / 2);

    this.ctx.translate(x, y);
    this.ctx.rotate(angle);
    this.ctx.scale(scaledPos.Z, scaledPos.Z);

    this.ctx.drawImage(this.carImages[id], -this.carWidth / 2, -this.carLength / 2, this.carWidth, this.carLength);

    this.ctx.restore();

    if (this.path) {
      this.drawPath(id);
    }

    if (car.boost_pickup) {
      this.updateBoosts(car);
    }
  }

  drawPath(carId) {
    for (const position of this.previousPositions[carId]) {

      if (!position) {
        return;
      }
      this.ctx.save();
      const scaledPos = this.getScaledPos(position);
      const x = scaledPos.X;
      const y = scaledPos.Y;
      const radius = this.positionRadius * scaledPos.Z;
      this.ctx.translate(x, y);
      this.ctx.fillStyle = this.carColors[carId];
      this.ctx.beginPath();
      this.ctx.arc(0, 0, radius, 0, 2 * Math.PI);
      this.ctx.closePath();
      this.ctx.fill();
      this.ctx.restore();
    }
  }

  drawDemolition(car) {
    this.ctx.save();

    const scaledPos = this.getScaledPos(car.position);
    const x = scaledPos.X;
    const y = scaledPos.Y;

    this.ctx.translate(x, y);

    this.ctx.drawImage(this.imgDemolition, -20, -20, 40, 40);

    this.ctx.restore();
  }

  drawCars(cars: Car[]) {
    Object.entries(cars).forEach(([id, car]) => {
      if (car.position && car.linear_velocity) {
        this.drawCar(id, car);
        if (car.dist_ball < 25000) {
          console.log(car.dist_ball + ' : ' + car.name);
        }
      } else if (car.demolition) {
        this.drawDemolition(car);
      }
    });
  }

  drawBall(ball: Ball) {
    this.ctx.save();
    const scaledPos = this.getScaledPos(ball.position);
    const x = scaledPos.X;
    const y = scaledPos.Y;
    const radius = this.ballRadius * scaledPos.Z;
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
      this.finished = true;
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

    this.blueScore = frame.teams['blue'].score;
    this.redScore = frame.teams['red'].score;

    this.setCarIds(frame.cars);

    this.updateCarsBoost(frame.cars);
    this.updatePreviousPositions(frame.cars);
    this.updateProgress();

    this.drawBall(frame.ball);
    this.drawCars(frame.cars);

    if (this.index % 20 === 0) {
      this.updateTeams(frame);
    }

    setTimeout(this.drawFrames.bind({}), (1000 / 60) / this.speedRatio);
  }
}
