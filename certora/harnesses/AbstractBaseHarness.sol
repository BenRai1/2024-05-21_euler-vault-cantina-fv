// SPDX-License-Identifier: GPL-2.0-or-later

pragma solidity ^0.8.0;

import {IEVC} from "ethereum-vault-connector/interfaces/IEthereumVaultConnector.sol";
import "../../src/EVault/shared/Base.sol";

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



    function getLTVConfig(address collateral) external view returns (LTVConfig memory) {
        return vaultStorage.ltvLookup[collateral];
    }

    function vaultCacheOracleConfigured() external returns (bool) {
        return address(loadVault().oracle) != address(0);
    }

    function isAccountStatusCheckDeferredExt(address account) external view returns (bool) {
        return isAccountStatusCheckDeferred(account);
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



}