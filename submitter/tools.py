from submitter.models import Submitter


def get_or_create_submitter(name):
    try:
        return Submitter.objects.get(name=name)
    except Submitter.DoesNotExist:
        return create_submitter(name)


def create_submitter(name):
    submitter = Submitter(name=name)
    submitter.save()
    return submitter
