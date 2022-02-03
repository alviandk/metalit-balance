from django.urls import path

from django.conf import settings
from .views import (
    TestingAddBalance,
    TestingDeductBalance,
    UserBalanceCreationView,
    UserBalanceView,
    GenerateJWTMockup,
    TestJWTResponse,
    UserBuyProductView,
    UserReceiveRewardView,
    UserTopUpView,
    UserTransactionHistoryView,
    UserWithdrawView,
)

urlpatterns = [
    path("user-balance/get", UserBalanceView.as_view(), name="get_user_balance"),
    path("user-transaction-history/get", UserTransactionHistoryView.as_view()),
    path("user/topup", UserTopUpView.as_view(), name="user_topup"),
    path("user/withdraw", UserWithdrawView.as_view(), name="user_withdraw"),
    path("user/buy-product", UserBuyProductView.as_view(), name="user_buy_product"),
    path(
        "user/receive-reward",
        UserReceiveRewardView.as_view(),
        name="user_receive_reward",
    ),
    path("user-balance/create", UserBalanceCreationView.as_view()),
]

"""
Additional API for dev mode
"""
if settings.DEV_MODE:
    urlpatterns += [
        # Endpoint to test internal method
        path("add-balance", TestingAddBalance.as_view()),
        path("deduct-balance", TestingDeductBalance.as_view()),
        path(
            "auth/generate-token/<str:user_id>",
            GenerateJWTMockup.as_view(),
            name="generate-token",
        ),
        path("auth/test-token", TestJWTResponse.as_view()),
    ]
