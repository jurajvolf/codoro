from django.contrib import admin
from .models import (
    RewardItem, RewardPurchase, DorosTransaction,
    Quest, StudentQuestProgress, ClassQuest, ClassQuestContribution,
    CoinDrop, CoinDropClaim, Badge, StudentBadge
)

admin.site.register(RewardItem)
admin.site.register(RewardPurchase)
admin.site.register(DorosTransaction)
admin.site.register(Quest)
admin.site.register(StudentQuestProgress)
admin.site.register(ClassQuest)
admin.site.register(ClassQuestContribution)
admin.site.register(CoinDrop)
admin.site.register(CoinDropClaim)
admin.site.register(Badge)
admin.site.register(StudentBadge)