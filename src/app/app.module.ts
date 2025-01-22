import { NgModule } from "@angular/core";
import { AppComponent } from "./app.component";
import { HeaderComponent } from "./components/header/header.component";
import { UserComponent } from "./components/user/user.component";
import { InvestmentComponent } from "./components/investment/investment.component";
import { FormsModule } from "@angular/forms";
import { BrowserModule } from "@angular/platform-browser";

@NgModule({
    declarations: [AppComponent, HeaderComponent, UserComponent, InvestmentComponent],
    imports: [FormsModule, BrowserModule],
    bootstrap: [AppComponent]
})
export class AppModule { }