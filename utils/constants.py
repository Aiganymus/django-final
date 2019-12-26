IMAGE_ALLOWED_EXTS = ['.png', '.jpg']

SILVER = 0
GOLD = 1
ORDINARY = 2

ACCOUNT_TYPES = (
    (SILVER, 'Silver'),
    (GOLD, 'Gold'),
    (ORDINARY, 'Ordinary')
)

DEPOSIT = 0
WITHDRAW = 1
TRANSFER = 2

OPERATION_TYPES = (
    (DEPOSIT, 'Deposit'),
    (WITHDRAW, 'Withdraw'),
    (TRANSFER, 'Transfer')
)
