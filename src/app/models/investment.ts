export interface InvestmentInput {
    initialInvestment: number,
    expectedReturn: number,
    annualInvestment: number,
    duration: number
}

export interface InvestmentResult {
    year: number,
    interest: number,
    valueEndOfYear: number,
    annualInvestment: number,
    totalInterest: number,
    totalAmountInvested: number,
}