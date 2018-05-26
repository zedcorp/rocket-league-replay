import {Component, OnInit, Output} from '@angular/core';

@Component({
  selector: 'app-fpspicker',
  templateUrl: './fpspicker.component.html',
  styleUrls: ['./fpspicker.component.css']
})
export class FpspickerComponent implements OnInit {

  fpsOptions: number[] = [5, 10, 30, 60];
  @Output() fps = 60;

  constructor() { }

  ngOnInit() {
  }
}
