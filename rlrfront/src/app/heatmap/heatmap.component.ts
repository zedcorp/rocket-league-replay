import {Component, Input, OnInit} from '@angular/core';

import {Coordinates} from '../models/coordinates.model';

declare var h337: any;

@Component({
  selector: 'app-heatmap',
  templateUrl: './heatmap.component.html',
  styleUrls: ['./heatmap.component.css']
})
export class HeatmapComponent implements OnInit {

  @Input() fieldWidth;
  @Input() fieldHeight;
  private _carLocations: Coordinates[];

  constructor() { }

  @Input()
  set carLocations(carLocations: Coordinates[]) {
    this._carLocations = carLocations;
    console.log('init heatmap');

    const heatmap = h337.create({
      container: document.getElementById('container')
    });

    const data = this._carLocations.map(position => ({x: position.X, y: position.Y, value: 1}));

    heatmap.setData({
      max: 100,
      // data: [{ x: 10, y: 15, value: 5}]
      data: data
    });
  }

  get carLocations(): Coordinates[] { return this._carLocations; }

  ngOnInit() {

  }

}
