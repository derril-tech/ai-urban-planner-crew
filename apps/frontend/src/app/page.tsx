export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
        <h1 className="text-4xl font-bold text-center mb-8">
          AI Urban Planner Crew
        </h1>
        <p className="text-center text-lg mb-4">
          Multi-agent planning studio for urban development
        </p>
        <div className="text-center">
          <p className="text-sm text-gray-600">
            Turn briefs into fully specified concept plans with zoning, mobility, utilities, and more.
          </p>
        </div>
      </div>
    </main>
  )
}
