from electrum.bip32 import BIP32Node
from electrum.bitcoin import pubkey_to_address
from electrum.constants import set_testnet, set_mainnet
from bitcoinlib.keys import Address, BKeyError, HDKey, check_network_and_key, path_expand
from bitcoinlib.transactions import serialize_multisig_redeemscript

set_mainnet()
# To get all the xpub use the BitGo CLI and generate a new address. The JSON result will contain all the xpubs and address types.
bitgo_xpub=''
backup_xpub=''
user_xpub=''
script_type = 'p2sh'


def get_bitgo_address_at_derivation(deriv):
    bip_go = BIP32Node.from_xkey(bitgo_xpub)
    bip_backup = BIP32Node.from_xkey(backup_xpub)
    bip_user = BIP32Node.from_xkey(user_xpub)
    non_change_bip_go = bip_go.subkey_at_public_derivation((0,0,0))
    non_change_bip_backup = bip_backup.subkey_at_public_derivation((0,0,0))
    non_change_bip_user = bip_user.subkey_at_public_derivation((0,0,0))
    pubkey_go = non_change_bip_go.subkey_at_public_derivation((deriv,))
    pubkey_backup = non_change_bip_backup.subkey_at_public_derivation((deriv,))
    pubkey_user = non_change_bip_user.subkey_at_public_derivation((deriv,))
    pubkey_list = [pubkey_user.eckey.get_public_key_hex(), pubkey_backup.eckey.get_public_key_hex(), pubkey_go.eckey.get_public_key_hex()]
    redeemscript=serialize_multisig_redeemscript(pubkey_list, 2) # Might need 3 for 2 of 3
    address = Address(redeemscript, encoding=None, script_type=script_type)
    return address
