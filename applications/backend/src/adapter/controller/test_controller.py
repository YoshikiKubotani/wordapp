import json
import uuid
from typing import Any

import redis
from pydantic import UUID4

from src.adapter.gateway import RDBRepositoryGateway
from src.domain.dto import TestItemAnswerDTO, TestItemQuestionDTO
from src.usecase.interactor import DeckUsecase, TestUsecase


class TestController:
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

    def _create_test_usecase(self) -> TestUsecase:
        return TestUsecase(
            # self.user_repository,
            self.item_repository,
            # self.genra_repository,
            # self.deck_repository,
            # self.score_repository,
            # self.history_repository,
        )

    def _create_deck_usecase(self) -> DeckUsecase:
        return DeckUsecase(
            # self.user_repository,
            self.item_repository,
            # self.genra_repository,
            # self.deck_repository,
            # self.score_repository,
            # self.history_repository,
        )

    def make_test_set(self, grade_id: int, num_items: int) -> list[UUID4]:
        # テストセットを作成するためのユースケースを作成
        test_usecase = self._create_test_usecase()
        # deck_usecase = self._create_deck_usecase()

        # デッキを取得
        # deck = deck_usecase.get_deck(grade_id)
        # 指定した学年の問題を取得
        deck = self.item_repository.select_data({"grade": grade_id})

        # 取得したデッキからテストセットを作成
        test_set = test_usecase.make_random_test_set(num_items, deck)

        # テストセットをRedisにキャッシュし、その際にUUIDを生成して返す
        test_set_uuid_list = test_usecase.cache_test_set(test_set)

        return test_set_uuid_list

    def get_question(self, item_uuid: UUID4) -> TestItemQuestionDTO:
        # テストセットを取得するためのユースケースを作成
        test_usecase = self._create_test_usecase()

        # RedisからUUIDに対応する問題の情報を取得
        test_item_question_dto = test_usecase.get_question(item_uuid)

        return test_item_question_dto

    def get_answer(self, item_uuid: UUID4) -> TestItemAnswerDTO:
        # テストセットを取得するためのユースケースを作成
        test_usecase = self._create_test_usecase()

        # RedisからUUIDに対応する答えの情報を取得
        test_item_answer_dto = test_usecase.get_answer(item_uuid)

        return test_item_answer_dto

    def check_answer(self, item_uuid: UUID4, response_info: dict[str, Any]) -> bool:
        # テストセットを取得するためのユースケースを作成
        test_usecase = self._create_test_usecase()

        # RedisからUUIDに対応する答えの情報を取得
        test_item_answer_dto = test_usecase.get_answer(item_uuid)

        # ユーザーの回答と正解を比較
        print(response_info)
        if test_item_answer_dto.answer == response_info["userAnswer"]:
            return True
        else:
            return False
