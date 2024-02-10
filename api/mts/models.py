from datetime import datetime
from typing import List, Optional, Any

from pydantic import BaseModel, RootModel


class BaseRequestModel(BaseModel):
    text: str
    status_code: int


class MyTariff(BaseModel):
    subscriptionId: str
    contentId: str
    channelId: Any
    price: float
    period: int
    isPremiumSubscriber: bool
    isMtsSubscriber: bool
    subscriptionDate: str
    tarifficationDate: str
    nextTarifficationDate: str
    defaultTarifficationStartDate: Any
    tarifficationStatus: int
    contentName: str
    isTrial: bool
    isTrialProvided: bool
    isPromoCodePeriod: bool
    internalId: str
    sdpId: Any
    ecId: Any
    serviceGroupName: str
    bindingId: str
    userId: str
    promoCode: Any
    cppId: Any

    def __str__(self):
        return f"Подключенный сейчас тариф: {self.contentName}"

class MyTariffsList(RootModel):
    root: List[MyTariff]


class Tariff(BaseModel):
    contentId: str
    channelId: Any
    contentName: str
    period: int
    trialPeriod: int
    price: float
    isTrial: bool




class TariffList(RootModel):
    root: List[Tariff]

    def __str__(self):
        return f"Возможные для подключения тарифы:"


class ActivationResponse(BaseModel):
    subscriptionId: str
