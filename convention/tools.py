import arrow
import roman as roman

from convention.models import Convention, Section


def get_or_create_convention(label):
    slot, year = get_components_from_convention_label(label)

    try:
        return Convention.objects.get(label=label, slot=slot, year=year)
    except Convention.DoesNotExist:
        return create_convention(label, slot=slot, year=year)


def get_components_from_convention_label(label):
    parts = label.split('/')
    slot = roman.fromRoman(parts[0])
    year = arrow.get(int(parts[1]), 1, 1).date()
    return slot, year


def create_convention(label, slot=None, year=None):
    if not slot:
        slot, _ = get_components_from_convention_label(label)
    if not year:
        _, year = get_components_from_convention_label(label)

    convention = Convention(label=label, slot=slot, year=year)
    convention.save()

    return convention


def get_or_create_section(name):
    try:
        return Section.objects.get(name=name)
    except Section.DoesNotExist:
        return create_section(name)


def create_section(name):
    section = Section(name=name)
    section.save()
    return section
