import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {HttpClientModule} from '@angular/common/http';

import {NgbModule} from '@ng-bootstrap/ng-bootstrap';

import {AppComponent} from './app.component';
import {PlayersComponent} from './players/players.component';
import {PlayerDetailComponent} from './player-detail/player-detail.component';
import {MessagesComponent} from './messages/messages.component';
import {AppRoutingModule} from './/app-routing.module';
import {DashboardComponent} from './dashboard/dashboard.component';
import {MatchesComponent} from './matches/matches.component';
import {MenuComponent} from './menu/menu.component';
import {FpspickerComponent} from './fpspicker/fpspicker.component';
import {FieldComponent} from './field/field.component';
import { ReplaysComponent } from './replays/replays.component';
import { FieldModalComponent } from './field-modal/field-modal.component';

@NgModule({
  declarations: [
    AppComponent,
    PlayersComponent,
    PlayerDetailComponent,
    MessagesComponent,
    DashboardComponent,
    MatchesComponent,
    MenuComponent,
    FpspickerComponent,
    FieldComponent,
    ReplaysComponent,
    FieldModalComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule,
    HttpClientModule,
    NgbModule.forRoot()
  ],
  providers: [],
  bootstrap: [AppComponent],
  entryComponents: [
    FieldModalComponent
  ]
})
export class AppModule {
}
