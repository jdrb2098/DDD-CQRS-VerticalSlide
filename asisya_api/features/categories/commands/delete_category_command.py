class DeleteCategoryCommand:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, category_id: int):
        category = self.repo.get_by_id(category_id)
        if not category:
            raise ValueError("Category not found")
        self.repo.delete(category)
