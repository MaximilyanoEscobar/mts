import datetime
from typing import List, Optional

from pydantic import BaseModel


class BaseRequestModel(BaseModel):
    text: str
    status_code: int


class MyTariff(BaseModel):
    subscriptionId: str
    contentId: str
    channelId: Optional[str]
    price: float
    period: int
    isPremiumSubscriber: bool
    isMtsSubscriber: bool
    subscriptionDate: datetime
    tarifficationDate: datetime
    nextTarifficationDate: datetime
    defaultTarifficationStartDate: Optional[datetime]
    tarifficationStatus: int
    contentName: str
    isTrial: bool
    isTrialProvided: bool
    isPromoCodePeriod: bool
    internalId: str
    sdpId: Optional[str]
    ecId: Optional[str]
    serviceGroupName: str
    bindingId: str
    userId: str
    promoCode: Optional[str]
    cppId: Optional[str]


class MyTariffsList(BaseModel):
    tariffs: List[Optional[MyTariff]]


class Tariff(BaseModel):
    contentId: str
    channelId: Optional[str]
    contentName: str
    period: int
    trialPeriod: int
    price: float
    isTrial: bool


class TariffList(BaseModel):
    tariffs: List[Optional[Tariff]]


class ActivationResponse(BaseModel):
    subscriptionId: str
