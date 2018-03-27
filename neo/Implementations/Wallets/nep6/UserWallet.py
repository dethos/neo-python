from neo.Wallets.Wallet import Wallet
from .utils import is_nep6_wallet
from logzero import logger
import json
import os


class UserWallet(Wallet):
    """Wallet class, focused on working with the new wallet standard"""

    Version = None

    def __init__(self, path, passwordKey, create):
        self._extra = {}
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
        """Makes sure the wallet file exist and is in NEP6 format"""
        if os.path.exists(self._path):
            if not is_nep6_wallet(self._path):
                logger.error("The existing file in the provided path is not a "
                             "valid NEP6 wallet")
                raise Exception("The path does not belong to a NEP6 Wallet")
            return self._load_wallet()
        else:
            with open(self._path, mode='w') as f:
                base_wallet = {
                    'name': os.path.basename(self._path),
                    'version': '1.0',
                    'scrypt': {'n': 16384, 'r': 8, 'p': 8},
                    'accounts': [],
                    'extra': {}
                }
                f.write(json.dumps(base_wallet))

    def SaveStoredData(self, key, value):
        """Write extra data in the wallet extra field"""
        self._extra[key] = value
        self._persist()

    def LoadStoredData(self, key):
        return self._extra.get(key, None)

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

    def ToNEP6Json(self):
        base = {
            'name': os.path.basename(self._path),
            'version': '1.0',
            'scrypt': {'n': 16384, 'r': 8, 'p': 8},
            'accounts': self._accounts_dict(),
            'extra': self._encode_extra()
        }
        return json.dumps(base)

    def _load_wallet(self):
        """Populate the current wallet from the NEP6 file"""
        pass

    def _accounts_dict(self):
        return {}

    def _encode_extra(self):
        enc_extras = {}
        for key, val in self._extra.items():
            enc_extras[key] = val.hex() if isinstance(val, bytes) else val
        return enc_extras

    def _persist(self):
        with open(self._path, mode='w') as f:
            f.write(self.ToNEP6Json())
