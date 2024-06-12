// SPDX-License-Identifier: GPL-2.0-or-later

pragma solidity ^0.8.0;

import {IEVC} from "ethereum-vault-connector/interfaces/IEthereumVaultConnector.sol";
import "../../src/EVault/shared/Base.sol";
import "../../src/EVault/shared/types/Owed.sol";

// This exists so that Base.LTVConfig and other type declarations 
// are available in CVL and can be used across specs for different modules.
// We need to split this into a concrete contract and an Abstract contract
// so that we can refer to Base.LTVConfig as a type in shared CVL functions
// while also making function definitions sharable among harnesses via
// AbstractBase. AbstractBaseHarness includes the shared function definitions.
abstract contract AbstractBaseHarness is Base {
    uint256 constant BALANCE_FORWARDER_MASK = 0x8000000000000000000000000000000000000000000000000000000000000000;
    uint256 constant OWED_MASK = 0x7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF0000000000000000000000000000;
    uint256 constant SHARES_MASK = 0x000000000000000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFFFFFF;
    uint256 constant OWED_OFFSET = 112;
    uint256 constant MAX_ALLOWED_INTEREST_RATE = 291867278914945094175;
    uint32 constant CFG_EVC_COMPATIBLE_ASSET = 1 << 1;


    using TypesLib for uint256;
    using OwedLib for uint256;

    function getLTVConfig(address collateral) external view returns (LTVConfig memory) {
        return vaultStorage.ltvLookup[collateral];
    }

    function vaultCacheOracleConfigured() external returns (bool) {
        return address(loadVault().oracle) != address(0);
    }

    function isAccountStatusCheckDeferredExt(address account) external view returns (bool) {
        return isAccountStatusCheckDeferred(account);
    }

    function areChecksDeferredExt() external view returns (bool) {
        return IEVC(evc).areChecksDeferred();
    }

    function isInLiquidationCoolOffExt(address account) external view returns (bool) {
        return block.timestamp < getLastAccountStatusCheckTimestamp(account) + vaultStorage.liquidationCoolOffTime;
    }
    
    function getBalanceAndForwarderExt(address account) public returns (Shares, bool) {
        return vaultStorage.users[account].getBalanceAndBalanceForwarder();
    }


    //--------------------------------------------------------------------------
    // Controllers
    //--------------------------------------------------------------------------
    function vaultIsOnlyController(address account) external view returns (bool) {
        address[] memory controllers = IEVC(evc).getControllers(account);
        return controllers.length == 1 && controllers[0] == address(this);
    }

    function vaultIsController(address account) external view returns (bool) {
        return IEVC(evc).isControllerEnabled(account, address(this));
    }

    function getControlersExt(address account) external view returns (address[] memory) {
        return IEVC(evc).getControllers(account);
    }

    //--------------------------------------------------------------------------
    // Collaterals
    //--------------------------------------------------------------------------
    function getCollateralsExt(address account) public view returns (address[] memory) {
        return getCollaterals(account);
    }

    function isCollateralEnabledExt(address account, address market) external view returns (bool) {
        return isCollateralEnabled(account, market);
    }


    //--------------------------------------------------------------------------
    // Operation disable checks
    //--------------------------------------------------------------------------
    function isOperationDisabledExt(uint32 operation) public returns (bool) {
        VaultCache memory vaultCache = updateVault();
        return isOperationDisabled(vaultCache.hookedOps, operation);
    }

    function isDepositDisabled() public returns (bool) {
        return isOperationDisabledExt(OP_DEPOSIT);
    }

    function isMintDisabled() public returns (bool) {
        return isOperationDisabledExt(OP_MINT);
    }

    function isWithdrawDisabled() public returns (bool) {
        return isOperationDisabledExt(OP_WITHDRAW);
    }

    function isRedeemDisabled() public returns (bool) {
        return isOperationDisabledExt(OP_REDEEM);
    }

    function isSkimDisabled() public returns (bool) {
        return isOperationDisabledExt(OP_SKIM);
    }


    //--------------------------------------------------------------------------
    // Modifier checks
    //--------------------------------------------------------------------------

    function reentrancyLockedHarness() external view returns (bool) {
        return vaultStorage.reentrancyLocked;
    }

    function getOwedHarness(address account) external view returns (Owed){
        return Owed.wrap(uint144((PackedUserSlot.unwrap(vaultStorage.users[account].data) & OWED_MASK) >> OWED_OFFSET));
    }


    function getHookTargetHarness() external view returns (address) {
        return vaultStorage.hookTarget;
    }

    function useViewCallerHarness() external pure returns (address) {
        return ProxyUtils.useViewCaller();
    }

    
    function isNotSetCompatibeAssetHarness(Flags self) external pure returns (bool) {
        return self.isNotSet(CFG_EVC_COMPATIBLE_ASSET);
    }

    function isKnownNonOwnerAccountHarness(address account) external view returns (bool) {
        return isKnownNonOwnerAccount(account);
    }


    //--------------------------------------------------------------------------
    // Transformations uint, Owed, Assets
    //--------------------------------------------------------------------------

    ///////////////////////////// TO ASSETS //////////////////////////////////////

    function uintToAssetsHarness(uint256 amount) external pure returns (Assets) {
        return amount.toAssets();
    }
    function uintToAssetsUpHarness(uint256 amount) external pure returns (Assets) {
        Owed owed = Owed.wrap(uint144(amount));
        return owed.toAssetsUp();
    }

    function unitToAssetsHarness(uint256 amount) external pure returns (Assets) {
        if (amount > MAX_SANE_AMOUNT) revert Errors.E_AmountTooLargeToEncode();
        return Assets.wrap(uint112(amount));
    }

    function owedToAssetsUpHarness(Owed amount) external pure returns (Assets) {
        return amount.toAssetsUp();
    }

    function sharesToAssetsDownHarness(Shares amount, VaultCache memory vaultCache) external pure returns (Assets) {
        return amount.toAssetsDown(vaultCache);
    }

    function shareToAssetsUpHarness(Shares amount, VaultCache memory vaultCache) external pure returns (Assets) {
        return amount.toAssetsUp(vaultCache);
    }

    ///////////////////////////// TO OWED //////////////////////////////////////

    function assetsToOwedHarness(Assets self) external pure returns (Owed) {
        unchecked {
            return TypesLib.toOwed(self.toUint() << INTERNAL_DEBT_PRECISION_SHIFT);
        }
    }


    function uintToOwedHarness(uint256 amount) external pure returns (Owed) {
        return Owed.wrap(uint144(amount));
    }

    function subUncheckedHarness(Owed a, Owed b) external pure returns (Owed) {
        return Owed.wrap(uint144(a.toUint() - b.toUint()));
        //i:turn Owed to uint256, substract them, turn back to Owed
    }

    function addUncheckedHarness(Owed a, Owed b) external pure returns (Owed) {
        return Owed.wrap(uint144(a.toUint() + b.toUint()));
        //i:turn Owed to uint256, add them, turn back to Owed 
    }

    ///////////////////////////// TO SHARES //////////////////////////////////////

    function assetsToSharesUpHarness(Assets self, VaultCache memory vaultCache) external pure returns (Shares) {
        return self.toSharesUp(vaultCache);
    }

    function assetsToSharesDownHarness(Assets self, VaultCache memory vaultCache) external pure returns (Shares) {
        return self.toSharesDown(vaultCache);
    }

    function uintToSharesHarness(uint256 amount) external pure returns (Shares) {
        return Shares.wrap(uint112(amount));
    }


    ///////////////////////////// TO UINT //////////////////////////////////////
    function assetsToUintHarness(Assets self) external pure returns (uint256) {
        return self.toUint();
    }

    function sharesToUintHarness(Shares self) external pure returns (uint256) {
        return self.toUint();
    }

    
    ////////////////////// USSER BALANCES ///////////////////////////////
    function getUserSharesHarness(address user) external view returns (Shares) {
        return vaultStorage.users[user].getBalance();
    }

    function getUserDebtHarness(address user) external view returns (Owed) {
        return vaultStorage.users[user].getOwed();
    }

    // function summarizingFunctionHarness(UserStorage storage self) internal view returns (Shares) {
    //     Shares balance = Shares.wrap(0);
    //     return balance;
    // }


    



}