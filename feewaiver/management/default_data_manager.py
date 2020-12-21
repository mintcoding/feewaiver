import datetime
import json
import logging
import os

import pytz
from django.contrib.auth.models import Group
from django.contrib.gis.geos import GEOSGeometry, fromfile
from django.core.exceptions import MultipleObjectsReturned
from ledger.settings_base import TIME_ZONE

from feewaiver import settings
from feewaiver.main_models import GlobalSettings
#from disturbance.components.proposals.models import ApiarySiteFeeType, SiteCategory, ApiarySiteFee, ProposalType, \
#    ApiaryAnnualRentalFeePeriodStartDate, ApiaryAnnualRentalFeeRunDate, ApiaryAnnualRentalFee

logger = logging.getLogger(__name__)


def construct_name_values(mul):
    ret = []
    for i in range(1, 21):
        ret.append({'name': str(i), 'value': i})
    return ret


class DefaultDataManager(object):


    def __init__(self):
        # Groups
        #CUSTOM_GROUPS = [settings.ADMIN_GROUP, settings.APIARY_ADMIN_GROUP, settings.DAS_APIARY_ADMIN_GROUP, settings.APIARY_PAYMENTS_OFFICERS_GROUP,]
        #for group_name in CUSTOM_GROUPS:
        #    try:
        #        group, created = Group.objects.get_or_create(name=group_name)
        #        if created:
        #            logger.info("Created group: {}".format(group_name))
        #    except Exception as e:
        #        logger.error('{}, Group name: {}'.format(e, group_name))


        # Store
        for item in GlobalSettings.default_values:
            try:
                obj, created = GlobalSettings.objects.get_or_create(key=item[0])
                if created:
                    obj.value = item[1]
                    obj.save()
                    logger.info("Created {}: {}".format(item[0], item[1]))
            except Exception as e:
                logger.error('{}, Key: {}'.format(e, item[0]))


