import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {PlayersComponent} from './players/players.component';
import {DashboardComponent} from './dashboard/dashboard.component';
import {PlayerDetailComponent} from './player-detail/player-detail.component';
import {FpspickerComponent} from './fpspicker/fpspicker.component';
import {FieldComponent} from './field/field.component';
import {ReplaysComponent} from './replays/replays.component';
import {HeatmapComponent} from "./heatmap/heatmap.component";

const routes: Routes = [
  {path: '', redirectTo: '/players', pathMatch: 'full'},
  {path: 'dashboard', component: DashboardComponent},
  {path: 'replays', component: ReplaysComponent},
  {path: 'replays/:id', component: FieldComponent},
  {path: 'fps', component: FpspickerComponent},
  {path: 'field', component: FieldComponent},
  {path: 'players', component: PlayersComponent},
  {path: 'players/:id', component: ReplaysComponent},
  {path: 'detail/:id', component: PlayerDetailComponent},
  {path: 'heatmap', component: HeatmapComponent}
];

@NgModule({
  exports: [RouterModule],
  imports: [RouterModule.forRoot(routes)]
})
export class AppRoutingModule {

}
