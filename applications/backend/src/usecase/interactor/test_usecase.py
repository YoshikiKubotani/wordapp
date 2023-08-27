import random
import json
import uuid
import redis
from typing import Any
from pydantic import UUID4

from src.adapter.gateway import RDBRepositoryGateway
from src.domain.dto import TestItemDTO, TestItemQuestionDTO, TestItemAnswerDTO
from src.utils import get_my_logger

logger = get_my_logger(__name__)


class TestUsecase:
  def __init__(
    self,
    # user_repository: RDBRepositoryGateway,
    item_repository: RDBRepositoryGateway,
    # genra_repository: RDBRepositoryGateway,
    # deck_repository: RDBRepositoryGateway,
    # score_repository: RDBRepositoryGateway,
    # history_repository: RDBRepositoryGateway,
  ):
    # self.user_repository = user_repository
    self.item_repository = item_repository
    # self.genra_repository = genra_repository
    # self.deck_repository = deck_repository
    # self.score_repository = score_repository
    # self.history_repository = history_repository

  def make_random_test_set(self, num_items: int, source: list[dict[str, Any]]) -> list[TestItemDTO]:
    # ランダムにnum_items個の問題を選択
    selected_items = random.sample(source, num_items)

    # 各問題につき、４つの選択肢をランダムに取得
    selected_items_with_options = self._get_options_for_each_item(selected_items, 4)

    return selected_items_with_options


  def cache_test_set(self, test_set: list[TestItemDTO]) -> list[UUID4]:
    # Redisに接続
    pool = redis.ConnectionPool(host='redis', port=6379, db=0)
    r = redis.StrictRedis(connection_pool=pool)

    # Redisにテストセットを保存し、keyに用いるUUIDをリストに追加
    test_set_uuid_list = []
    for test_item in test_set:
      # UUID4の生成
      key_uuid = uuid.uuid4()
      # UUIDをkeyとして、作成したテストセットをRedisに保存
      r.set(str(key_uuid), test_item.model_dump_json(round_trip=True))
      # UUIDをリストに追加
      test_set_uuid_list.append(key_uuid)

    return test_set_uuid_list


  def get_question(self, item_uuid: UUID4) -> TestItemQuestionDTO:
    test_item_dto = self._retrieve_item_from_redis(item_uuid)

    # 問いに必要な情報のみを取得
    test_item_question_dto = TestItemQuestionDTO.model_validate({
      "item_index": test_item_dto.item_index,
      "english": test_item_dto.english,
      "op1": test_item_dto.op1,
      "op2": test_item_dto.op2,
      "op3": test_item_dto.op3,
      "op4": test_item_dto.op4,
    })

    return test_item_question_dto


  def get_answer(self, item_uuid: UUID4) -> TestItemAnswerDTO:
    test_item_dto = self._retrieve_item_from_redis(item_uuid)

    # 答えに必要な情報のみを取得
    test_item_answer_dto = TestItemAnswerDTO.model_validate({
      "answer": test_item_dto.answer,
    })

    return test_item_answer_dto


  def _shuffle_and_split(self, l: list[Any], n: int) -> tuple[list[Any], list[Any]]:
    random.shuffle(l)
    return l[:n], l[n:]


  def _get_options_for_each_item(self, items: list[dict[str, Any]], num_options: int) -> list[TestItemDTO]:
    # 帰り値用のリスト
    test_item_dto_list = []

    # 全問題の数を取得し、間違い選択肢に用いることが可能な問題のIDリストを取得
    item_num = self.item_repository.get_new_id()
    option_source = list(range(1, item_num))
    logger.debug(f"The number of items in a source DB: {item_num}")

    # 各問題につき、間違い選択肢を取得
    for i, target_item_info in enumerate(items):
      # DTO作成用の辞書
      test_item_dict = {
        "item_id": target_item_info.item_id,
        "item_index": i,
        "english": target_item_info.english,
      }

      while True:
        # 間違い選択肢に用いる問題のIDをnum_options-1個取得
        wrong_options, option_source = self._shuffle_and_split(option_source, num_options-1)

        # 間違い選択肢に用いる問題のIDに正解の問題IDが含まれている場合は再度取得
        if target_item_info.item_id in wrong_options:
          continue

        logger.debug(f"---{i}/{len(items)}--")
        # 選択肢の情報を追加
        # 間違いの選択肢の順番をランダムにする
        random.shuffle(wrong_options)

        # 何番目に正解の選択肢を入れるかをランダムに決める
        correct_option_index = random.randint(0, num_options-1)

        # 正解の選択肢を追加
        test_item_dict[f"op{correct_option_index+1}"] = target_item_info.japanese
        test_item_dict["answer"] = target_item_info.japanese
        logger.debug(f"Correct Answer Index: {correct_option_index+1}")

        # 間違いの選択肢を追加
        logger.debug("Wrong Options:")
        for idx, wrong_option_id in enumerate(wrong_options):
          if idx < correct_option_index:
            logger.debug(f"{idx+1}: {wrong_option_id}")
            test_item_dict[f"op{idx+1}"] = self.item_repository.select_data({"item_id": wrong_option_id})[0].japanese
          if idx >= correct_option_index:
            logger.debug(f"{idx+2}: {wrong_option_id}")
            test_item_dict[f"op{idx+2}"] = self.item_repository.select_data({"item_id": wrong_option_id})[0].japanese
        break

      # 辞書をDTOに変換
      test_item_dto = TestItemDTO.model_validate(test_item_dict)

      # DTOをリストに追加
      test_item_dto_list.append(test_item_dto)

    return test_item_dto_list


  def _retrieve_item_from_redis(self, item_uuid: UUID4) -> TestItemDTO:
    # Redisに接続
    pool = redis.ConnectionPool(host='redis', port=6379, db=0)
    r = redis.StrictRedis(connection_pool=pool)

    # RedisからUUIDに対応する問題の情報を取得
    test_item = r.get(str(item_uuid))
    # 問題情報をJSONから辞書に変換
    test_item_dict = json.loads(test_item)

    # 辞書をDTOに変換
    test_item_dto = TestItemDTO.model_validate(test_item_dict)

    return test_item_dto