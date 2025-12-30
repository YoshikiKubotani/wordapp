import { useAtomValue, useSetAtom } from 'jotai'
import { removeWordAtom, sortedWordsAtom } from '@/features/word-book'
import { Badge } from '@/shared/ui/badge'
import { Button } from '@/shared/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shared/ui/card'

export function WordList() {
  const words = useAtomValue(sortedWordsAtom)
  const removeWord = useSetAtom(removeWordAtom)

  return (
    <Card className="backdrop-blur">
      <CardHeader className="flex flex-row items-start justify-between">
        <div className="space-y-1">
          <CardTitle>Word deck</CardTitle>
          <CardDescription>Newest first. Use them all in the flashcard loop.</CardDescription>
        </div>
        <Badge variant="solid">Total {words.length}</Badge>
      </CardHeader>
      <CardContent className="space-y-3">
        {words.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            No words yet. Add a few and start practicing.
          </p>
        ) : (
          <div className="space-y-3">
            {words.map((word) => (
              <div
                key={word.id}
                className="group rounded-lg border border-border/70 bg-card/60 p-3 shadow-sm transition hover:-translate-y-[1px] hover:shadow-md"
              >
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="text-base font-semibold text-foreground">{word.term}</p>
                    <p className="text-sm text-muted-foreground">{word.meaning}</p>
                  </div>
                  <Button
                    type="button"
                    size="sm"
                    variant="ghost"
                    className="opacity-0 transition group-hover:opacity-100"
                    onClick={() => removeWord(word.id)}
                    aria-label={`Remove ${word.term}`}
                  >
                    Remove
                  </Button>
                </div>
                {word.note ? (
                  <p className="mt-1 text-xs text-muted-foreground">{word.note}</p>
                ) : null}
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  )
}
