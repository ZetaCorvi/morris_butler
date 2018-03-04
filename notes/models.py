from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Notes(models.Model):
    data = models.TextField()
    user = models.ForeignKey(User, default=1, on_delete=set([1, ]))
    name = models.CharField(max_length=128, default="title")
    added_time = models.DateTimeField(auto_now_add=True)
    is_voise = models.BooleanField(default=False)

    @staticmethod
    def get_notes(sorting_type, user=1):
        # if aim = 'date' -> 'up' = new-old, 'down' = old-new
        # if aim = 'title' -> 'up' = a-z, 'down' = z-a
        notes = Notes.objects.filter(user=user)
        if sorting_type != 'all':
            sort = sorting_type.split('_')
            aim = sort[0]
            direction = sort[1]
        else:
            return notes
        if aim == "date":
            if direction == "up":
                notes = notes.order_by('-added_time')
            elif direction == "down":
                notes = notes.order_by('added_time')
        elif aim == "title":
            if direction == "up":
                notes = notes.order_by('name')
            elif direction == "down":
                notes = notes.order_by('-name')
        return notes

    @staticmethod
    def get_note_by_id(id):
        return Notes.objects.filter(id=id).first()

    @staticmethod
    def notes_sort_by_date(datetime, user): #note: datetime = {1: date_one NOT NULL, 2: date_two}
        notelist = []
        if len(datetime) == 1:
            date = datetime[0].date()
            for note in Notes.objects.filter(user=user):
                if note.added_time == date:
                    notelist.append(note)
        else:
            for note in Notes.objects.filter(user=user):
                if ((note.added_time.year <= datetime[1].year) and
                    (note.added_time.year >= datetime[0].year) and
                    (note.added_time.month <= datetime[1].month) and
                    (note.added_time.month >= datetime[0].month) and
                    (note.added_time.day <= datetime[1].day) and
                    (note.added_time.day >= datetime[0].day)):
                        notelist.append(note)
                        sort_hl(notelist)


        return notelist


def sort_hl(notelist):
    for note in notelist:
        pass #todo: add sorting algorithm