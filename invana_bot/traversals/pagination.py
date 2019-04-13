from .base import TraversalBase


class PaginationTraversal(TraversalBase):
    """


    """

    def __init__(self, current_page_count=None, traversal_config=None):
        self.current_page_content = current_page_count
        self.traversal_config = traversal_config
