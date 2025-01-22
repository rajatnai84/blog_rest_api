import { Component, computed, inject, input } from '@angular/core';
import { InvestmentService } from '../../services/investment.service';

@Component({
  selector: 'app-investment',
  templateUrl: './investment.component.html',
  styleUrl: './investment.component.css'
})
export class InvestmentComponent {
  private investmentService = inject(InvestmentService)

  // with computed function we can insure that we are not changing the value outside of the service
  // else also
  // results = this.investmentService.resultData.asReadonly();
  results = computed(() => this.investmentService.resultData())
}
