# coding=utf-8
import os

import arrow
from django.db import transaction

from convention.tools import get_or_create_convention, get_or_create_section
from motion.models import Motion, MOTION_STATUS_ACCEPTED, MOTION_STATUS_DISMISSED, MOTION_STATUS_REFERRED, \
    MOTION_STATUS_REJECTED, MOTION_STATUS_NOT_VOTED, Referral
from submitter.tools import get_or_create_submitter


@transaction.atomic
def add_motion_from_json(motion_json):
    convention = get_or_create_convention(motion_json.get('convention_title'))
    section = get_or_create_section(motion_json.get('section'))
    identifier = motion_json.get('motion_id')

    try:
        return Motion.objects.get(convention=convention, identifier=identifier)
    except Motion.DoesNotExist:
        pass

    status = map_status(motion_json.get('status'))

    title = motion_json.get('motion').get('title')
    body = motion_json.get('motion').get('body')

    pdf_name = os.path.basename(motion_json.get('pdf_link'))

    motion = Motion(
        convention=convention,
        section=section,
        identifier=identifier,

        title=title,
        body=body,

        pdf_name=pdf_name,

        status=status,

        created=arrow.utcnow().datetime
    )
    motion.save()

    # add submitters
    submitter_names = motion_json.get('submitter').split(',') if motion_json.get('submitter') else []
    for submitter_name in submitter_names:
        submitter = get_or_create_submitter(submitter_name.strip())
        motion.submitters.add(submitter)

    # add referrals
    referral_names = motion_json.get('referral').split(',') if motion_json.get('referral') else []
    for referral_name in referral_names:
        referral = get_or_create_referral(referral_name.strip())
        motion.referrals.add(referral)

    return motion


def map_status(raw_status):
    status_mapping = {
        u'Annahme': MOTION_STATUS_ACCEPTED,
        u'Erledigt': MOTION_STATUS_DISMISSED,
        u'Überweisung': MOTION_STATUS_REFERRED,
        u'Ablehnung': MOTION_STATUS_REJECTED,
        u'Nicht abgestimmt': MOTION_STATUS_NOT_VOTED,
    }
    if not raw_status in status_mapping:
        raise AssertionError(u'unexpected raw status: {}'.format(raw_status))
    return status_mapping.get(raw_status)


def get_or_create_referral(name):
    try:
        return Referral.objects.get(name=name)
    except Referral.DoesNotExist:
        return create_referral(name)


def create_referral(name):
    referral = Referral(name=name)
    referral.save()
    return referral
