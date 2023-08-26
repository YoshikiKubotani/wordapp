import inspect
import os

import networkx as nx
import psycopg2
from psycopg2.extensions import AsIs, connection

from src.frameworks import postgres
from src.adapter.gateway import RDBRepositoryGateway

from .logger_utils import get_my_logger

logger = get_my_logger(__name__)


def get_ordered_dbs(all_tool_classes: list[RDBRepositoryGateway]) -> list[RDBRepositoryGateway]:
    G = nx.DiGraph()

    for db in all_tool_classes:
        G.add_node(db.db_name)
        for v in db.fk.values():
            if isinstance(v, dict):
                v = v["table"]
            G.add_edge(v, db.db_name)

    order = list(nx.topological_sort(G))
    order_dict = {db.db_name: db for db in all_tool_classes}
    return [order_dict[o] for o in order]

def initialize_all(all_tool_classes: list[RDBRepositoryGateway]) -> None:
    ordered_db = get_ordered_dbs(all_tool_classes)

    for db in ordered_db:
        logger.info(f"initialize: {db.db_name}")
        db.create_table()