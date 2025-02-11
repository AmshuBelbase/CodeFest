import pandas as pd
import numpy as np
from typing import Tuple, Dict, List
import matplotlib.pyplot as plt
import seaborn as sns


class HealthcarePlanAnalyzer:
    def _init_(self):
        self.plans_df = None
        self.insulin_df = None
        self.beneficiary_df = None

    def load_data(self, plans_file: str, insulin_file: str, beneficiary_file: str) -> None:
        """Load and prepare the data files"""
        self.plans_df = pd.read_csv(plans_file, sep='|')
        self.insulin_df = pd.read_csv(insulin_file, sep='|')
        self.beneficiary_df = pd.read_csv(beneficiary_file, sep='|')

    def analyze_market_coverage(self) -> Dict:
        """Analyze market coverage and opportunities"""
        coverage = {
            'states': len(self.plans_df['STATE'].unique()),
            'counties': len(self.plans_df['COUNTY_CODE'].unique()),
            'total_plans': len(self.plans_df['PLAN_ID'].unique()),
            'plans_by_state': self.plans_df.groupby('STATE').size().to_dict(),
            'snp_plans': len(self.plans_df[self.plans_df['SNP'] > 0])
        }
        return coverage

    def analyze_pricing_strategy(self) -> Dict:
        """Analyze current pricing strategy and identify optimization opportunities"""
        pricing_analysis = {
            'premium_stats': self.plans_df['PREMIUM'].describe().to_dict(),
            'deductible_stats': self.plans_df['DEDUCTIBLE'].describe().to_dict(),
            'zero_premium_plans': len(self.plans_df[self.plans_df['PREMIUM'] == 0]),
            'avg_insulin_cost': self.insulin_df['copay_amt_nonpref_insln'].mean()
        }
        return pricing_analysis

    def identify_expansion_opportunities(self) -> List[Dict]:
        """Identify potential market expansion opportunities"""
        # Group counties by state and analyze penetration
        state_coverage = self.plans_df.groupby(
            'STATE')['COUNTY_CODE'].nunique()

        # Get total counties data (you would need to add actual total counties data)
        total_counties = {
            'OH': 88,
            'NE': 93,
            'IL': 102,
            'MO': 115
        }

        opportunities = []
        for state in state_coverage.index:
            if state in total_counties:
                coverage_ratio = state_coverage[state] / total_counties[state]
                if coverage_ratio < 0.8:  # Less than 80% coverage
                    opportunities.append({
                        'state': state,
                        'current_counties': state_coverage[state],
                        'total_counties': total_counties[state],
                        'coverage_ratio': coverage_ratio,
                        'opportunity_level': 'High' if coverage_ratio < 0.5 else 'Medium'
                    })

        return opportunities

    def analyze_competitive_advantage(self) -> Dict:
        """Analyze competitive advantages in current markets"""
        advantages = {
            'zero_premium_markets': self.plans_df[self.plans_df['PREMIUM'] == 0]['COUNTY_CODE'].nunique(),
            'low_deductible_markets': self.plans_df[self.plans_df['DEDUCTIBLE'] < 200]['COUNTY_CODE'].nunique(),
            'snp_coverage': self.plans_df[self.plans_df['SNP'] > 0]['COUNTY_CODE'].unique().tolist()
        }
        return advantages

    def generate_recommendations(self) -> List[Dict]:
        """Generate actionable recommendations based on analysis"""
        market_coverage = self.analyze_market_coverage()
        pricing = self.analyze_pricing_strategy()
        expansion_opps = self.identify_expansion_opportunities()

        recommendations = []

        # Market Expansion Recommendations
        for opp in expansion_opps:
            recommendations.append({
                'category': 'Market Expansion',
                'state': opp['state'],
                'action': f"Consider expansion in {opp['state']} - {opp['opportunity_level']} opportunity",
                'potential_impact': 'High' if opp['coverage_ratio'] < 0.5 else 'Medium'
            })

        # Pricing Optimization Recommendations
        if pricing['zero_premium_plans'] < market_coverage['total_plans'] * 0.3:
            recommendations.append({
                'category': 'Pricing',
                'action': 'Consider increasing zero-premium plan offerings',
                'rationale': 'Market analysis shows opportunity for more zero-premium plans',
                'potential_impact': 'High'
            })

        # Product Mix Recommendations
        snp_ratio = market_coverage['snp_plans'] / \
            market_coverage['total_plans']
        if snp_ratio < 0.2:
            recommendations.append({
                'category': 'Product Mix',
                'action': 'Evaluate expansion of SNP plan offerings',
                'rationale': 'Current SNP penetration is below market potential',
                'potential_impact': 'High'
            })

        return recommendations

    def generate_report(self) -> Dict:
        """Generate comprehensive analysis report"""
        return {
            'market_coverage': self.analyze_market_coverage(),
            'pricing_strategy': self.analyze_pricing_strategy(),
            'expansion_opportunities': self.identify_expansion_opportunities(),
            'competitive_advantages': self.analyze_competitive_advantage(),
            'recommendations': self.generate_recommendations()
        }


def main():
    # Initialize analyzer
    analyzer = HealthcarePlanAnalyzer()

    # Load data
    analyzer.load_data('plan_information.txt',
                       'insulin_beneficiary.txt', 'beneficiary_cost.txt')

    # Generate comprehensive report
    report = analyzer.generate_report()

    # Print key findings and recommendations
    print("\n=== Market Coverage Analysis ===")
    print(f"States: {report['market_coverage']['states']}")
    print(f"Counties: {report['market_coverage']['counties']}")
    print(f"Total Plans: {report['market_coverage']['total_plans']}")

    print("\n=== Recommendations ===")
    for rec in report['recommendations']:
        print(f"\nCategory: {rec['category']}")
        print(f"Action: {rec['action']}")
        print(f"Potential Impact: {rec['potential_impact']}")

    return report


analyzer = HealthcarePlanAnalyzer()
analyzer.load_data('plan_information.txt',
                   'insulin_beneficiary.txt', 'beneficiary_cost.txt')
report = analyzer.generate_report()
print(report)

expansion_df = pd.DataFrame(report["expansion_opportunities"])
expansion_df.to_csv("expansion_opportunities.csv", index=False)

# Convert Recommendations to DataFrame
recommendations_df = pd.DataFrame(report["recommendations"])
recommendations_df.to_csv("recommendations.csv", index=False)

# Convert Market Coverage to DataFrame
market_coverage_df = pd.DataFrame([report["market_coverage"]])
market_coverage_df.to_csv("market_coverage.csv", index=False)

print("CSV files saved successfully!")


# if __name__ == "__main__":
#     main()
