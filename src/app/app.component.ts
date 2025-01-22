import { Component, signal } from '@angular/core';
import { HeaderComponent } from "./components/header/header.component";
import { UserComponent } from "./components/user/user.component";
import { InvestmentComponent } from './components/investment/investment.component';

@Component({
    selector: 'app-root',
    standalone: true,
    templateUrl: './app.component.html',
    imports: [HeaderComponent, UserComponent, InvestmentComponent],
})
export class AppComponent {}
