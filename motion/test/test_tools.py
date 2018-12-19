# coding=utf-8
import arrow
from django.db.models import Q
from django.test.testcases import TestCase

from convention.models import Convention, Section
from motion.models import MOTION_STATUS_ACCEPTED, Referral
from motion.tools import add_motion_from_json


class TestAddMotionFromJSON(TestCase):

    def setUp(self):
        self.test_json1 = {
            "convention_link": "I/2017",
            "convention_title": "I/2017",
            "id": "0a993ca8-f22b-4e53-8345-2de31eb95d3d",
            "motion": {
                "body": " <p><strong>In das Bundeswahlprogramm wird aufgenommen:"
                        "</strong><br/>\u00a0<br/>Die SPD fordert, den erforderlichen Rechtsrahmen zu schaffen, "
                        "um auch \u00fcber das Jahr 2019 hinaus den Sozialen Wohnungsbau durch den Bund "
                        "finanziell zu unterst\u00fctzen.<br/>\u00a0<br/>\u00a0</p>",
                "title": "F\u00f6rderung des sozialen Wohnungsbaus durch den Bund auch nach 2019 erm\u00f6glichen"
            },
            "motion_id": "Antrag 37/I/2017",
            "motion_link": "https://parteitag.spd-berlin.de/antraege/foerderung-des-sozialen-wohnungsbaus-durch-den-bund-auch-nach-2019-ermoeglichen/",
            "pdf_link": "https://parteitag.spd-berlin.de/wp-content/uploads/antrag-37i2017_-foerderung-des-sozialen-wohnungsbaus-durch-den-bund-auch-nach-2019-ermoeglichen.pdf",
            "referral": "AG Sozialdemokratischer Bezirksb\u00fcrgermeister, Bundesparteitag_2018-04-22, Landesgruppe, Landesvorstand",
            "section": "Bauen / Wohnen / Stadtentwicklung",
            "status": "Annahme",
            "submitter": "KDV Marzahn-Hellersdorf, Abt. 11/05 Friedrichsfelde-Rummelsburg, KDV Treptow-K\u00f6penick",
            "title": "F\u00f6rderung des sozialen Wohnungsbaus durch den Bund auch nach 2019 erm\u00f6glichen"
        }

    def test_add_motion_from_json(self):
        motion = add_motion_from_json(self.test_json1)

        # motion looks as expected
        self.assertEqual(motion.identifier, u'Antrag 37/I/2017')
        self.assertEqual(
            motion.title, u'Förderung des sozialen Wohnungsbaus durch den Bund auch nach 2019 ermöglichen')
        self.assertEqual(
            motion.body, u' <p><strong>In das Bundeswahlprogramm wird aufgenommen:'
                         u'</strong><br/>\u00a0<br/>Die SPD fordert, den erforderlichen Rechtsrahmen zu schaffen, '
                         u'um auch über das Jahr 2019 hinaus den Sozialen Wohnungsbau durch den Bund '
                         u'finanziell zu unterstützen.<br/>\u00a0<br/>\u00a0</p>')
        self.assertEqual(
            motion.pdf_name,
            u'antrag-37i2017_-foerderung-des-sozialen-wohnungsbaus-durch-den-bund-auch-nach-2019-ermoeglichen.pdf')
        self.assertEqual(motion.status, MOTION_STATUS_ACCEPTED)

        # convention exists
        convention_query = Q(label=u'I/2017')
        self.assertTrue(Convention.objects.filter(convention_query).exists())
        convention = Convention.objects.get(convention_query)
        self.assertEqual(convention.slot, 1)
        self.assertEqual(convention.year, arrow.get(2017, 1, 1).date())
        self.assertEqual(Convention.objects.count(), 1)

        # section exists
        section_query = Q(name=u'Bauen / Wohnen / Stadtentwicklung')
        self.assertTrue(Section.objects.filter(section_query).exists())
        self.assertEqual(Section.objects.count(), 1)

        # submitters exists
        submitters = [
            u'KDV Marzahn-Hellersdorf',
            u'Abt. 11/05 Friedrichsfelde-Rummelsburg',
            u'KDV Treptow-Köpenick'
        ]
        for submitter in submitters:
            self.assertTrue(motion.submitters.filter(name=submitter).exists(),
                            u'submitter {} could not be found'.format(submitter))
        self.assertEqual(motion.submitters.all().count(), 3)

        # referrals exists
        referrals = [
            u'AG Sozialdemokratischer Bezirksbürgermeister',
            u'Bundesparteitag_2018-04-22',
            u'Landesgruppe',
            u'Landesvorstand'
        ]
        for referral in referrals:
            self.assertTrue(motion.referral.filter(name=referral).exists(),
                            u'referral {} could not be found'.format(referral))
        self.assertEqual(motion.referrals.all().count(), 4)
