import { useAtomValue } from 'jotai'
import { FlashcardPanel } from '@/features/flashcard-practice/ui/flashcard-panel'
import { sortedWordsAtom, wordStatsAtom } from '@/features/word-book'
import { WordForm } from '@/features/word-book/ui/word-form'
import { WordList } from '@/features/word-book/ui/word-list'
import { Badge } from '@/shared/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/shared/ui/tabs'

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
                シンプル単語学習アプリ
              </h1>
              <p className="max-w-2xl text-base text-secondary-foreground">
                単語を登録して、さくっと学習しちゃおう！難しい場合は思い出すためのヒントをつけてもOK
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              <Badge variant="solid">登録単語数 {stats.total}</Badge>
              {stats.newestTerm ? <Badge variant="outline">Newest {stats.newestTerm}</Badge> : null}
            </div>
          </div>
        </div>
      </header>

      <main>
        <Tabs defaultValue="study" className="gap-4">
          <TabsList>
            <TabsTrigger value="study">学習</TabsTrigger>
            <TabsTrigger value="add">追加</TabsTrigger>
          </TabsList>
          <TabsContent value="study">
            <div className="grid gap-5">
              <FlashcardPanel words={words} />
            </div>
          </TabsContent>
          <TabsContent value="add">
            <div className="grid gap-5 lg:grid-cols-2">
              <WordForm />
              <WordList />
            </div>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}
