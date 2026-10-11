import ExtractDemo from "@/components/ExtractDemo";

const PHASES = [
  { title: "Your background", text: "Add jobs, courses, projects and letters. Stored only in your browser." },
  { title: "The job", text: "Paste the job description. We work out what the role is looking for." },
  { title: "The match", text: "Pick what to highlight, with suggestions you can accept, reject or steer." },
  { title: "Your CV", text: "A tailored, one-page CV, rendered right in your browser." },
];

export default function Home() {
  return (
    <main className="mx-auto w-full max-w-3xl px-4 py-16 sm:py-24">
      <header className="space-y-4">
        <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">CVTailor</h1>
        <p className="max-w-xl text-lg text-muted">
          Tailor your CV to each job, from everything you&apos;ve done. Your data stays in your browser.
        </p>
      </header>

      <ol className="mt-12 grid gap-4 sm:grid-cols-2">
        {PHASES.map((phase, i) => (
          <li key={phase.title} className="rounded-lg border border-border bg-surface p-4">
            <span className="text-xs font-medium text-accent">Step {i + 1}</span>
            <h2 className="mt-1 font-medium">{phase.title}</h2>
            <p className="mt-1 text-sm text-muted">{phase.text}</p>
          </li>
        ))}
      </ol>

      <section className="mt-16 space-y-4">
        <h2 className="text-xl font-semibold">Try step 1</h2>
        <ExtractDemo />
      </section>
    </main>
  );
}
