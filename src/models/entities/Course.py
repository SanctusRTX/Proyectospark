class Course():
    def __init__(self, id, title, image_url, external_url, description="", active=True):
        self.id = id
        self.title = title
        self.image_url = image_url
        self.external_url = external_url
        self.description = description
        self.active = active
