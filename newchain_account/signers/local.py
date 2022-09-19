import base58
import binascii
import warnings

from newchain_account.signers.base import (
    BaseAccount,
)


class LocalAccount(BaseAccount):
    r"""
    A collection of convenience methods to sign and encrypt, with an embedded private key.

    :var bytes key: the 32-byte private key data

    .. code-block:: python

        >>> my_local_account.address # doctest: +SKIP
        "0xF0109fC8DF283027b6285cc889F5aA624EaC1F55"
        >>> my_local_account.key # doctest: +SKIP
        b"\x01\x23..."

    You can also get the private key by casting the account to :class:`bytes`:

    .. code-block:: python

        >>> bytes(my_local_account) # doctest: +SKIP
        b"\\x01\\x23..."
    """
    
    def __init__(self, key, account, chain_id):
        '''
        Initialize a new account with the the given private key.
        
        :param newchain_keys.PrivateKey key: to prefill in private key execution
        :param ~newchain_account.account.Account account: the key-unaware management API
        '''
        self._publicapi = account

        self._address = key.public_key.to_checksum_address()

        key_raw = key.to_bytes()
        self._private_key = key_raw

        self._key_obj = key

        self._chain_id = chain_id
        self._new_address = self.__encode_new_address()

    def __encode_new_address(self):
        address_data = self._address
        if address_data.startswith('0x'):
            address_data = address_data[2:]
        hex_chainID = hex(self._chain_id)[2:][-8:]
        if (len(hex_chainID) % 2) == 1:
            hex_chainID = '0' + hex_chainID
        num_sum = hex_chainID + address_data
        data = base58.b58encode_check(b'\0' + binascii.a2b_hex(num_sum))
        new_address = 'NEW' + data.decode()
        return new_address

    @property
    def address(self):
        return self._address

    @property
    def new_address(self):
        return self._new_address

    @property
    def privateKey(self):
        """
        .. CAUTION:: Deprecated for :meth:`~newchain_account.signers.local.LocalAccount.key`.
            This attribute will be removed in v0.5
        """
        warnings.warn(
            "privateKey is deprecated in favor of key",
            category=DeprecationWarning,
        )
        return self._private_key

    @property
    def key(self):
        """
        Get the private key.
        """
        return self._private_key

    def encrypt(self, password, kdf=None, iterations=None):
        """
        Generate a string with the encrypted key.

        This uses the same structure as in
        :meth:`~newchain_account.account.Account.encrypt`, but without a private key argument.
        """
        return self._publicapi.encrypt(self.key, password, kdf=kdf, iterations=iterations)

    def signHash(self, message_hash):
        return self._publicapi.signHash(
            message_hash,
            private_key=self.key,
        )

    def sign_message(self, signable_message):
        """
        Generate a string with the encrypted key.

        This uses the same structure as in
        :meth:`~newchain_account.account.Account.sign_message`, but without a private key argument.
        """
        return self._publicapi.sign_message(signable_message, private_key=self.key)

    def signTransaction(self, transaction_dict):
        warnings.warn(
            "signTransaction is deprecated in favor of sign_transaction",
            category=DeprecationWarning,
        )
        return self.sign_transaction(transaction_dict)

    def sign_transaction(self, transaction_dict):
        return self._publicapi.sign_transaction(transaction_dict, self.key)

    def __bytes__(self):
        return self.key
