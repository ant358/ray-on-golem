from typing import List, Dict

from pydantic.main import BaseModel

from models.types import NodeID


class GetNodeRequest(BaseModel):
    node_id: int


class CreateClusterRequest(BaseModel):
    image_hash: str
    network: str
    budget: int
    num_workers: int = 20


class CreateNodesRequest(BaseModel):
    count: int
    tags: Dict


class DeleteNodesRequest(BaseModel):
    node_ids: List[NodeID]


class SetNodeTagsRequest(BaseModel):
    tags: Dict
