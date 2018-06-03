import {Component, Input, OnInit} from '@angular/core';

import {Coordinates} from '../models/coordinates.model';

declare var h337: any;

@Component({
  selector: 'app-heatmap',
  templateUrl: './heatmap.component.html',
  styleUrls: ['./heatmap.component.css']
})
export class HeatmapComponent implements OnInit {

  private _carLocations: Coordinates[];
  heatmap;

  constructor() {
  }

  @Input()
  set carLocations(carLocations: Coordinates[]) {
    this._carLocations = carLocations;

    const container = document.getElementById('container');
    while (container.firstChild) {
      container.removeChild(container.firstChild);
    }

    this.heatmap = h337.create({
      container: container,
      radius: 50
    });

    const data = this._carLocations.map(position => ({x: position.X, y: position.Y, value: 1}));

    this.heatmap.setData({
      max: 100,
      data: data
    });
  }

  get carLocations(): Coordinates[] { return this._carLocations; }

  ngOnInit() {

  }

}
