import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {PlayersComponent} from './players/players.component';
import {DashboardComponent} from './dashboard/dashboard.component';
import {PlayerDetailComponent} from './player-detail/player-detail.component';
import {ReplayComponent} from "./replay/replay.component";
import {FpspickerComponent} from "./fpspicker/fpspicker.component";
import {FieldComponent} from "./field/field.component";

const routes: Routes = [
  {path: '', redirectTo: '/dashboard', pathMatch: 'full'},
  {path: 'dashboard', component: DashboardComponent},
  {path: 'replay', component: ReplayComponent},
  {path: 'fps', component: FpspickerComponent},
  {path: 'field', component: FieldComponent},
  {path: 'players', component: PlayersComponent},
  {path: 'detail/:id', component: PlayerDetailComponent}
];

@NgModule({
  exports: [RouterModule],
  imports: [RouterModule.forRoot(routes)]
})
export class AppRoutingModule {

}
