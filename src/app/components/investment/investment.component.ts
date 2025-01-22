import { Component, Input } from '@angular/core';
import { InvestmentResult } from '../../models/investment';
import { CurrencyPipe } from '@angular/common';

@Component({
  selector: 'app-investment',
  standalone: true,
  imports: [CurrencyPipe],
  templateUrl: './investment.component.html',
  styleUrl: './investment.component.css'
})
export class InvestmentComponent {
  @Input() results? : InvestmentResult[];
}
