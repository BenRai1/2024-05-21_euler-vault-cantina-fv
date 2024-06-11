// SPDX-License-Identifier: GPL-2.0-or-later

pragma solidity ^0.8.0;

import "../../src/EVault/shared/Base.sol";
import "../../certora/harnesses/AbstractBaseHarness.sol";

// This exists so that Base.LTVConfig and other type declarations 
// are available in CVL and can be used across specs for different modules.
// We need to split this into a concrete contract and an Abstract contract
// so that we can refer to Base.LTVConfig as a type in shared CVL functions
// while also making function definitions sharable among harnesses via
// AbstractBase.
contract BaseHarness is Base, AbstractBaseHarness {
    constructor(Integrations memory integrations) Base(integrations) {
    }

    function updateVaultHarness() external returns (VaultCache memory){
            return updateVault();
    }

    function loadVaultHarness() external view returns (VaultCache memory){
            return loadVault();
    }

    // function initVaultCacheHarness(VaultCache memory vaultCache) external view {
    //         initVaultCache(vaultCache);
    // }

    function totalAssetsInternalHarness(VaultCache memory vaultCache) external view returns (uint256) {
            return totalAssetsInternal(vaultCache);
    }

    function initOperationHarness(uint32 operation, address accountToCheck) external {
            initOperation(operation, accountToCheck);
    }

    function isOperationDisabledHarness(Flags hookedOps, uint32 operation) external view returns (bool) {
            return isOperationDisabled(hookedOps, operation);
    }

    function callHookHarness(Flags hookedOps, uint32 operation, address caller) external {
            callHook(hookedOps, operation, caller);
    }

    function callHookWithLockHarness(Flags hookedOps, uint32 operation, address caller) external {
            callHookWithLock(hookedOps, operation, caller);
    }






}