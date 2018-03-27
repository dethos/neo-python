from neo.Utils.WalletFixtureTestCase import WalletFixtureTestCase
from neo.Wallets.utils import to_aes_key
from neo.Settings import settings
from neo.Implementations.Wallets.nep6.UserWallet import UserWallet
from hashlib import sha256
import os


class NEP6WalletTestCase(WalletFixtureTestCase):

    existing_path = os.path.join(settings.DATA_DIR_PATH, 'random-file')
    new_path = os.path.join(settings.DATA_DIR_PATH, 'new-wallet.json')

    @classmethod
    def setUpClass(cls):
        super(NEP6WalletTestCase, cls).setUpClass()
        open(cls.existing_path, 'a').close()

    @classmethod
    def tearDownClass(cls):
        super(NEP6WalletTestCase, cls).tearDownClass()
        os.remove(cls.existing_path)
        os.remove(cls.new_path)

    def test_create_with_inexistent_path(self):
        passwordKey = to_aes_key('password')
        passwordHash = sha256(passwordKey).digest()
        wallet = UserWallet(self.new_path, passwordKey, True)
        self.assertEqual(os.path.exists(self.new_path), True)
        self.assertEqual(wallet._extra['PasswordHash'], passwordHash)

    def test_create_using_existing_path(self):
        with self.assertRaises(Exception) as context:
            UserWallet(self.existing_path, to_aes_key('password'), True)
        self.assertEqual("The path does not belong to a NEP6 Wallet",
                         str(context.exception))
