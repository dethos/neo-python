from neo.Wallets.Wallet import Wallet
from logzero import logger


class UserWallet(Wallet):
    """Wallet class, focused on working with the new wallet standard"""

    Version = None

    def __init__(self, path, passwordKey, create):
        super().__init__(path, passwordKey=passwordKey, create=create)

    @staticmethod
    def Open(path, password):
        return UserWallet(path=path, passwordKey=password, create=False)

    @staticmethod
    def Create(path, password):
        """Create a new user wallet.

        Args:
            path (str): A path indicating where to create or open the wallet
                        i.e. "/Wallets/mywallet".
            password (str): a 10 characters minimum password to secure the
                            wallet with.

        Returns:
             UserWallet: a UserWallet instance.
        """
        wallet = UserWallet(path=path, passwordKey=password, create=True)
        wallet.CreateKey()
        return wallet

    def BuildDatabase(self):
        pass

    def SaveStoredData(self, key, value):
        pass

    def LoadStoredData(self, key):
        pass

    def LoadKeyPairs(self):
        pass

    def LoadContracts(self):
        pass

    def LoadWatchOnly(self):
        pass

    def LoadCoins(self):
        pass

    def LoadNEP5Tokens(self):
        pass

    def OnProcessNewBlock(self, block, added, changed, deleted):
        pass

    def OnSaveTransaction(self, tx, added, changed, deleted):
        pass

    def BalanceChanged(self):
        pass

    def ToJson(self, verbose=False):
        pass
