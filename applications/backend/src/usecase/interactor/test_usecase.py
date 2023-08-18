import random
from typing import Any

from src.adapter.gateway import RDBRepositoryGateway

class TestUsecase:
  def __init__(
    self,
    user_repository: RDBRepositoryGateway,
    item_repository: RDBRepositoryGateway,
    genra_repository: RDBRepositoryGateway,
    deck_repository: RDBRepositoryGateway,
    score_repository: RDBRepositoryGateway,
    history_repository: RDBRepositoryGateway,
  ):
    self.user_repository = user_repository
    self.item_repository = item_repository
    self.genra_repository = genra_repository
    self.deck_repository = deck_repository
    self.score_repository = score_repository
    self.history_repository = history_repository

  def make_random_test_set(self, num_items: int, source: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    source = [{
      "item_id": int,
      "english": str,
      "japanese": str,
    }]
    """
    # ランダムにnum_items個の問題を選択
    selected_items = random.sample(source, num_items)

    # 各問題につき、４つの選択肢をランダムに取得
    selected_items_with_options = self._get_options_for_each_item(selected_items, 4)

    return selected_items_with_options

  def _shuffle_and_split(self, l: list[Any], n: int) -> tuple[list[Any], list[Any]]:
    random.shuffle(l)
    return l[:n], l[n:]

  def _get_options_for_each_item(self, items: list[dict[str, Any]], num_options: int) -> list[dict[str, Any]]:
    # 全問題の数を取得し、間違い選択肢に用いることが可能な問題のIDリストを取得
    item_num = self.item_repository.get_new_id()
    option_source = list(range(item_num))

    # 各問題につき、間違い選択肢を取得
    for target_item_info in items:
      while True:
        # 間違い選択肢に用いる問題のIDをnum_options-1個取得
        wrong_options, option_source = self._shuffle_and_split(option_source, num_options-1)

        # 間違い選択肢に用いる問題のIDに正解の問題IDが含まれている場合は再度取得
        if target_item_info.item_id in wrong_options:
          continue

        # 選択肢の情報を追加
        # 間違いの選択肢の順番をランダムにする
        wrong_options = random.shuffle(wrong_options)
        # 何番目に正解の選択肢を入れるかをランダムに決める
        correct_option_index = random.randint(0, num_options-1)
        # 正解の選択肢を追加
        target_item_info[f"op{correct_option_index}"] = target_item_info.japanese
        # 間違いの選択肢を追加
        for idx, wrong_option_id in enumerate(wrong_options):
          if idx < correct_option_index:
            target_item_info[f"op{idx}"] = self.item_repository.get({"item_id": wrong_option_id})[0].japanese
          if idx >= correct_option_index:
            target_item_info[f"op{idx+1}"] = self.item_repository.get({"item_id": wrong_option_id})[0].japanese
        break

    return items