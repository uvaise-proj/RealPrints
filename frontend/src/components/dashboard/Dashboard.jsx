import SummarySection  from './SummarySection.jsx'
import FailureInsights from './FailureInsights.jsx'
import BestConfig      from './BestConfig.jsx'

export default function Dashboard() {
  return (
    <div className="screen db-screen">
      <SummarySection />
      <FailureInsights />
      <BestConfig />
    </div>
  )
}
