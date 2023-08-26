from typing import Any

from src.adapter.gateway import RDBRepositoryGateway

class DeckUsecase:
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