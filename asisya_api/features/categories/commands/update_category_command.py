class UpdateCategoryCommand:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, category_id: int, data):
        category = self.repo.get_by_id(category_id)
        if not category:
            raise ValueError("Category not found")

        category.name = data.name or category.name
        category.slug = data.slug or category.slug
        category.description = data.description or category.description
        category.picture_path = data.picture_path or category.picture_path

        return self.repo.update(category)
