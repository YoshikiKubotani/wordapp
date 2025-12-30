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
          <CardTitle>単語一覧</CardTitle>
          <CardDescription>追加した単語の一覧（追加した順）</CardDescription>
        </div>
        <Badge variant="solid">合計 {words.length}</Badge>
      </CardHeader>
      <CardContent className="space-y-3">
        {words.length === 0 ? (
          <p className="text-sm text-secondary-foreground">
            まだ単語が追加されていないよ！まずは学習したい単語を追加しよう
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
                    <p className="text-sm text-secondary-foreground">{word.meaning}</p>
                  </div>
                  <Button
                    type="button"
                    size="sm"
                    variant="ghost"
                    className="opacity-0 transition group-hover:opacity-100"
                    onClick={() => removeWord(word.id)}
                    aria-label={`Remove ${word.term}`}
                  >
                    削除
                  </Button>
                </div>
                {word.note ? (
                  <p className="mt-1 text-xs text-secondary-foreground">{word.note}</p>
                ) : null}
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  )
}
