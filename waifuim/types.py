from dateutil.parser import parse


class Tag:
    """Represents an API tag."""
    def __init__(self, data):
        for key, values in data.items():
            setattr(self, key.lower(), values)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Tag) and self.tag_id == other.tag_id


class Image:
    """Represents an API Image."""
    def __init__(self, data):
        for key, values in data.items():
            setattr(self, key.lower(), values)
        self.tags = [Tag(tag) for tag in self.tags]
        self.uploaded_at = parse(self.uploaded_at)

    def __str__(self):
        return self.url

    def __eq__(self, other):
        return isinstance(other, Image) and self.file == other.file
