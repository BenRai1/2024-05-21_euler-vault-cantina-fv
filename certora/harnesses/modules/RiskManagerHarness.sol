// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity ^0.8.0;
import "../../../src/interfaces/IPriceOracle.sol";
import {ERC20} from "../../../lib/ethereum-vault-connector/lib/openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";
import "../AbstractBaseHarness.sol";
import "../../../src/EVault/modules/RiskManager.sol";

contract RiskManagerHarness is RiskManager, AbstractBaseHarness {
    constructor(Integrations memory integrations) RiskManager(integrations) {}

    function getCurrentVaultCacheHarness() external returns (VaultCache memory){
        VaultCache memory vaultCache;
        (vaultCache.asset, vaultCache.oracle, vaultCache.unitOfAccount) = ProxyUtils.metadata();
        vaultCache.lastInterestAccumulatorUpdate = vaultStorage.lastInterestAccumulatorUpdate;
        vaultCache.cash = vaultStorage.cash;
        vaultCache.totalBorrows = vaultStorage.totalBorrows;
        vaultCache.totalShares = vaultStorage.totalShares;
        vaultCache.supplyCap = vaultStorage.supplyCap.resolve();
        vaultCache.borrowCap = vaultStorage.borrowCap.resolve();
        vaultCache.hookedOps = vaultStorage.hookedOps;
        vaultCache.snapshotInitialized = vaultStorage.snapshotInitialized;
        vaultCache.accumulatedFees = vaultStorage.accumulatedFees;
        vaultCache.configFlags = vaultStorage.configFlags;
        vaultCache.interestAccumulator = vaultStorage.interestAccumulator;
        return vaultCache;
    }

    function toBytes4Harness(uint32 data) external pure returns (bytes4) {
        return bytes4(data);
    }

    function getLiabilityValueHarness(VaultCache memory vaultCache, address account, Owed owed, bool liquidation) external returns (uint256) {
        return getLiabilityValue(vaultCache, account, owed, liquidation);
    }

    function getCollateralValueHarness(VaultCache memory vaultCache, address account, address[] memory collateral, bool liquidation) external returns (uint256) {
        uint256 collateralValue;
        for (uint256 i; i < collateral.length; ++i) {
            collateralValue += getCollateralValue(vaultCache, account, collateral[i], liquidation);
        }
        return collateralValue;
    }

    function getCollateralValuesHarness(VaultCache memory vaultCache, address account, address[] memory collateral, bool liquidation) external returns (uint256[] memory) {
        uint256[] memory collateralValues = new uint256[](collateral.length);
        for (uint256 i; i < collateral.length; ++i) {
            collateralValues[i] = getCollateralValue(vaultCache, account, collateral[i], liquidation);
        }
        return collateralValues;
    }

    function getSnapshotHarness() external returns (Snapshot memory) {
        Snapshot memory snap = snapshot;
        return snap;
    }

    function toAssetUPHarness(Owed amount) external pure returns (Assets) {
        return amount.toAssetsUp();
    }

    function toUintHarness(Assets amount) external pure returns (uint256) {
        return amount.toUint();
    }

    function totalAssetsHarness(VaultCache memory vaultCache) external returns (uint256) {
        return totalAssetsInternal(vaultCache);
    }

    function calculateInterestRateHarness(uint256 newInterestRate) external returns (uint256 finalInterestRate) {
        if (newInterestRate > MAX_ALLOWED_INTEREST_RATE) finalInterestRate = MAX_ALLOWED_INTEREST_RATE;
        else finalInterestRate = newInterestRate;
    }



}