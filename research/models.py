import json
import requests
from datetime import datetime
from django.db import models
from django.core import serializers

from timeline.settings import PERMA_KEY, PERMA_FOLDER, STORAGES


class Tag(models.Model):
    name = models.CharField(max_length=1000)
    description = models.TextField(blank=True)
    date_start = models.DateTimeField(null=True, blank=True)
    date_end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def as_json(self):
        return self.name


class Citation(models.Model):
    name = models.CharField(max_length=800)
    cite = models.CharField(max_length=800, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    book_or_article = models.CharField(blank=True, null=True, max_length=2000)
    archived_url = models.URLField(blank=True, null=True)
    archived_date = models.DateTimeField(blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True,
                            choices=(("image", "image"),
                                     ("caselaw", "caselaw"),
                                     ("webpage", "webpage"),
                                     ("article", "article"),
                                     ("book", "book")))

    def __str__(self):
        return self.name

    def as_json(self):
        return dict(
            name=self.name,
            cite=self.cite,
            url=self.url,
            book_or_article=self.book_or_article,
            archived_url=self.archived_url,
            archived_date=str(self.archived_date),
            type=self.type
        )

    def save(self, *args, **kwargs):
        if self.url and not self.archived_url:
            if PERMA_KEY:
                data = {"url": self.url, "folder": PERMA_FOLDER}
                res = requests.post("https://api.perma.cc/v1/archives/?api_key=%s" % PERMA_KEY,
                                    data=json.dumps(data),
                                    headers={'Content-type': 'application/json'},
                                    allow_redirects=True)

                if res.status_code == 201:
                    content = json.loads(res.content.decode())
                    self.archived_url = "https://perma.cc/%s" % content['guid']
                    self.archived_date = content['creation_timestamp']

        return super(Citation, self).save(*args, **kwargs)


class Event(models.Model):
    name = models.CharField(max_length=1000)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    citation = models.ForeignKey('Citation', null=True, blank=True, related_name='events', on_delete=models.DO_NOTHING)
    weight = models.ForeignKey('Weight', null=True, blank=True, related_name='events', on_delete=models.DO_NOTHING)
    image = models.ForeignKey('Image', null=True, blank=True, related_name='events', on_delete=models.DO_NOTHING)
    description_long = models.TextField(blank=True)
    description_short = models.CharField(max_length=800, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    hide = models.BooleanField(default=False)
    type = models.CharField(blank=True, null=True, max_length=100,
                            choices=(("us_event", "us_event"),
                                     ("international_event", "international_event"),
                                     ("legislation", "legislation"),
                                     ("caselaw", "caselaw")))

    def __str__(self):
        return self.name

    def as_json(self):
        return dict(
            id=self.id,
            name=self.name,
            start_date=str(self.start_date),
            start_date_parsed=self.start_date.strftime("%B %d, %Y"),
            citation=self.citation.as_json(),
            type=self.type,
            hide=self.hide,
            description_long=self.description_long,
            description_short=self.description_short,
            tags=[tag.as_json() for tag in self.tags.all()],
        )


class Finding(models.Model):
    """
        Editorializing events
    """
    description_short = models.CharField(max_length=1000, blank=True)
    description_long = models.TextField(blank=True)
    events = models.ManyToManyField(Event, blank=True)

    def __str__(self):
        return self.description_short


class Weight(models.Model):
    level = models.PositiveIntegerField(null=True)
    description = models.CharField(blank=True, max_length=1000)

    def __str__(self):
        return "%s: %s" % (self.level, self.description)


class Image(models.Model):
    data = models.FileField(storage=STORAGES['image_storage'])
    src = models.ForeignKey('Citation', null=True, related_name='images', on_delete=models.DO_NOTHING)

    def __str__(self):
        return "%s %s" % (str(self.id), str(self.src.name))

    def save(self, *args, **kwargs):
        self.src.type = 'image'
        return super(Image, self).save(*args, **kwargs)
