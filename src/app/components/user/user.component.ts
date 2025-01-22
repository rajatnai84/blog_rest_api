import { Component, inject, output, signal } from '@angular/core';
import { InvestmentInput } from '../../models/investment';
import { InvestmentService } from '../../services/investment.service';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrl: './user.component.css'
})
export class UserComponent {
  calculate = output<InvestmentInput>();

  initialInvestment = signal('0');
  annualInvestment = signal('0');
  expectedReturn = signal('5');
  duration = signal('10');

  private investmentService = inject(InvestmentService)

  onSubmit() {
    this.investmentService.calculateInvestmentResults({
      initialInvestment: +this.initialInvestment(),
      annualInvestment: +this.annualInvestment(),
      expectedReturn: +this.expectedReturn(),
      duration: +this.duration(),
    })

    this.initialInvestment.set('0')
    this.annualInvestment.set('0')
    this.expectedReturn.set('5')
    this.duration.set('10')
  }

}
