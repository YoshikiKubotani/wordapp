import { useAtomValue } from 'jotai'
import { FlashcardPanel } from '@/features/flashcard-practice/ui/flashcard-panel'
import { sortedWordsAtom, wordStatsAtom } from '@/features/word-book'
import { WordForm } from '@/features/word-book/ui/word-form'
import { WordList } from '@/features/word-book/ui/word-list'
import { Badge } from '@/shared/ui/badge'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shared/ui/card'

export function HomePage() {
  const stats = useAtomValue(wordStatsAtom)
  const words = useAtomValue(sortedWordsAtom)

  return (
    <div className="mx-auto flex max-w-6xl flex-col gap-6 px-4 py-8 lg:py-12">
      <header className="rounded-3xl border border-border/70 bg-card/70 p-8 shadow-lg backdrop-blur">
        <div className="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
          <div className="space-y-4">
            <p className="text-sm font-semibold uppercase tracking-wide text-primary">Word app</p>
            <div className="space-y-2">
              <h1 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
                Build your English vocab and test it instantly
              </h1>
              <p className="max-w-2xl text-base text-muted-foreground">
                Register words, keep quick notes to remember them, and practice with a focused
                flashcard loop—all on a single page.
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              <Badge variant="solid">Words {stats.total}</Badge>
              {stats.newestTerm ? <Badge variant="outline">Newest {stats.newestTerm}</Badge> : null}
              <Badge variant="outline">Ready for API hookup</Badge>
            </div>
          </div>
          <Card className="w-full max-w-sm border-primary/30 bg-primary text-primary-foreground shadow-xl">
            <CardHeader className="pb-3">
              <CardTitle>Quick guide</CardTitle>
              <CardDescription className="text-primary-foreground/90">
                A tight workflow for daily drilling.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-2 pt-0 text-sm">
              <p className="rounded-lg bg-primary-foreground/10 px-3 py-2 text-primary-foreground">
                1) Add a word with a note you like.
              </p>
              <p className="rounded-lg bg-primary-foreground/10 px-3 py-2 text-primary-foreground">
                2) Shuffle the deck—cards pick up your latest edits.
              </p>
              <p className="rounded-lg bg-primary-foreground/10 px-3 py-2 text-primary-foreground">
                3) Reveal, self-grade, and loop until confident.
              </p>
            </CardContent>
          </Card>
        </div>
      </header>

      <main className="grid gap-5 lg:grid-cols-2">
        <div className="space-y-4">
          <WordForm />
          <WordList />
        </div>
        <FlashcardPanel words={words} />
      </main>
    </div>
  )
}
