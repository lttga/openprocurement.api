# -*- coding: utf-8 -*-
from openprocurement.api.roles import RolesFromCsv
from schematics.types.serializable import serializable
from openprocurement.api.models import Period
from openprocurement.tender.core.models import get_tender
from openprocurement.api.utils import get_now
from openprocurement.tender.core.utils import calc_auction_end_time, rounding_shouldStartAfter


class LotAuctionPeriod(Period):
    """The auction period."""

    class Options:
        roles = RolesFromCsv("LotAuctionPeriod.csv", relative_to=__file__)

    @serializable(serialize_when_none=False)
    def shouldStartAfter(self):
        if self.endDate:
            return
        tender = get_tender(self)
        lot = self.__parent__
        if tender.status not in ["active.tendering", "active.auction"] or lot.status != "active":
            return
        if tender.status == "active.auction" and lot.numberOfBids < 2:
            return
        if self.startDate and get_now() > calc_auction_end_time(lot.numberOfBids, self.startDate):
            start_after = calc_auction_end_time(tender.numberOfBids, self.startDate)
        else:
            start_after = tender.tenderPeriod.endDate
        return rounding_shouldStartAfter(start_after, tender).isoformat()
