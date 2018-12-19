# coding=utf-8
from django.contrib.gis.db import models


MOTION_STATUS_NOT_VOTED = u'not_voted'
MOTION_STATUS_DISMISSED = u'dismissed'
MOTION_STATUS_REFERRED = u'referred'
MOTION_STATUS_ACCEPTED = u'accepted'
MOTION_STATUS_REJECTED = u'rejected'

MOTION_STATUS_CHOICES = (
    (MOTION_STATUS_NOT_VOTED, u'nicht abgestimmt'),
    (MOTION_STATUS_DISMISSED, u'erledigt'),
    (MOTION_STATUS_REFERRED, u'überwiesen'),
    (MOTION_STATUS_ACCEPTED, u'angenommen'),
    (MOTION_STATUS_REJECTED, u'abgelehnt'),
)


class Motion(models.Model):
    convention = models.ForeignKey('convention.Convention')
    submitters = models.ManyToManyField('submitter.Submitter')
    section = models.ForeignKey('convention.Section')
    identifier = models.CharField(max_length=128)

    title = models.CharField(max_length=512)
    body = models.TextField()

    pdf_name = models.CharField(max_length=512)

    status = models.CharField(max_length=64, choices=MOTION_STATUS_CHOICES)

    referrals = models.ManyToManyField('motion.Referral')

    created = models.DateTimeField()

    class Meta:
        unique_together = ('convention', 'identifier')


class Referral(models.Model):
    name = models.CharField(max_length=128, unique=True)
